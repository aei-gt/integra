import pyodbc
import frappe
from datetime import datetime
from frappe.utils import today
from frappe.utils import get_datetime
from frappe.utils.background_jobs import enqueue

def fetch_data():
    settings = frappe.get_doc("HikVision Settings", "HikVision Settings")
    host = settings.get("host")
    user = settings.get("user")
    password = settings.get("password")
    database = settings.get("database")
    table = settings.get("table")
    odbc_version = settings.get("odbc_version")

    last_id = settings.get("last_hik_vision_record_id") or 0

    conn_str = (
        f'DRIVER={odbc_version};'
        f'SERVER={host};'
        f'DATABASE={database};'
        f'UID={user};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
        'timeout=2000;'
    )

    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()

    query = f"""
        SELECT 
            ID_Global, 
            EmployeeID,
            AccessDate,
            AccessTime,
            AccessDateTime
        FROM {table}
        WHERE ID_Global > {last_id} -- Only fetch records with ID greater than the last fetched ID
        ORDER BY AccessDateTime
    """

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    if not results:
        print("No new records found in HikVision database.")
        return [], None
    
    last_record = results[-1]
    # print(f"Fetched records: {results}")  # Remove or comment out this line

    return results, last_record

    
  
@frappe.whitelist()
def fetch_hik_vision_records():
    records, last_record = fetch_data()
    
    if not records:
        frappe.msgprint("No new records found.")
        return
    
    for record in records:
        if not frappe.db.exists("Hik Vision Attendance", {"id": record['ID_Global']}):
            doc = frappe.get_doc({
                "doctype": "Hik Vision Attendance",
                "id": record['ID_Global'],
                "employee_id": record['EmployeeID'],
                "access_date_time": record['AccessDateTime'],
                "access_date": record['AccessDate'],
                "access_time": record['AccessTime']
            })
            doc.insert()
            frappe.db.commit()

    settings = frappe.get_doc("HikVision Settings", "HikVision Settings")
    last_id_before_save = settings.last_hik_vision_record_id
    
    if last_record:
        new_last_id = last_record['ID_Global']
        settings.last_hik_vision_record_id = new_last_id
        settings.save()        
        last_id_after_save = settings.last_hik_vision_record_id
    else:
        last_id_after_save = last_id_before_save

    # frappe.msgprint(f"Fetched {len(records)} new records.")
    # frappe.msgprint(f"Last ID before fetch: {last_id_before_save}.")
    # frappe.msgprint(f"Updated last ID: {last_id_after_save}.")

    enqueue_create_attendance(last_id_before_save, last_id_after_save)

@frappe.whitelist()
def enqueue_create_attendance(last_id_before_save, last_id_after_save):
    enqueue(
        create_attendance,
        queue="long",
        now=frappe.conf.developer_mode or frappe.flags.in_test,
        last_id_before_save=last_id_before_save,
        last_id_after_save=last_id_after_save
    )


@frappe.whitelist()
def create_attendance(last_id_before_save, last_id_after_save):
    """
    This function processes attendance records between the IDs provided, marks present employees, 
    and calls the `mark_absent_employees` function to mark absent employees for each attendance date.
    """
    sql_query = """
        SELECT employee_id, access_date, MIN(access_time) AS entry, MAX(access_time) AS exit_time
        FROM `tabHik Vision Attendance`
        WHERE name BETWEEN %s AND %s
        GROUP BY employee_id, access_date
        ORDER BY employee_id, access_date
    """
    
    attendance_records = frappe.db.sql(sql_query, (last_id_before_save, last_id_after_save), as_dict=True)
    # frappe.msgprint(f"Updated last ID: {len(attendance_records)}.")
    if not attendance_records:
        return

    present_employees_by_date = {}
    attendance_dates = set()
    
    employee_ids = [record['employee_id'] for record in attendance_records]
    employees_map = frappe.get_all('Employee',filters={'attendance_device_id': ['in', employee_ids]},fields=['name', 'employee_name', 'attendance_device_id'])
    employees_map = {e['attendance_device_id']: e for e in employees_map}

    for record in attendance_records:
        employee_details = employees_map.get(record['employee_id'])
        attendance_date = get_datetime(record['access_date'])

        if employee_details:
            attendance_dates.add(attendance_date)
            if attendance_date not in present_employees_by_date:
                present_employees_by_date[attendance_date] = set()
            present_employees_by_date[attendance_date].add(record['employee_id'])

            attendance = frappe.db.get_value('Attendance', {
                'employee': employee_details['name'],
                'attendance_date': attendance_date
            }, ['name', 'status'])

            if attendance:
                attendance_name, status = attendance
                if status == 'Absent':
                    doc = frappe.get_doc("Attendance", attendance_name)
                    doc.status = "Present"
                    doc.save()
                    doc.submit()
            else:
                doc = frappe.new_doc("Attendance")
                doc.employee = employee_details['name']
                doc.attendance_date = attendance_date
                doc.status = "Present"
                doc.insert()
                doc.submit()

    for attendance_date in attendance_dates:
        present_employees = present_employees_by_date.get(attendance_date, set())
        mark_absent_employees(present_employees, attendance_date)
    
    frappe.db.commit()


@frappe.whitelist()
def mark_absent_employees(present_employees, attendance_date):
    """
    This function marks employees absent if they are not in the present_employees set for the given attendance date.
    """
    
    list_employee_have_id = frappe.get_all(
        "Employee", 
        filters={'attendance_device_id': ['!=', '']}, 
        fields=['name']
    )

    for employee in list_employee_have_id:
        if employee['name'] not in present_employees:
            attendance_exists = frappe.db.get_value('Attendance', {
                'employee': employee['name'],
                'attendance_date': attendance_date
            }, ['name', 'status'])

            if not attendance_exists:
                attendance = frappe.get_doc({
                    'doctype': 'Attendance',
                    'employee': employee['name'],
                    'attendance_date': attendance_date,
                    'status': 'Absent'
                })
                attendance.insert()
            else:
                attendance_name, status = attendance_exists
                if status == 'Absent':
                    continue

    frappe.db.commit()

@frappe.whitelist()
def delete_records():
    frappe.db.delete("Hik Vision Attendance")

@frappe.whitelist()
def testfunction(filters):
    

    return filters

@frappe.whitelist()
def delete_records_checkin():
    frappe.db.delete("Attendance")
    frappe.db.delete("Employee Checkin")
