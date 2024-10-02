import pyodbc
import frappe
from datetime import datetime, timedelta
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

    conn_str = (
        f'DRIVER={odbc_version};'
        f'SERVER={host};'
        f'DATABASE={database};'
        f'UID={user};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
        'timeout=1000;'
    )

    try:
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        # query = f"""
        #     SELECT TOP 10
        #         ID_Global, 
        #         EmployeeID,
        #         AccessDate,
        #         AccessTime,
        #         AccessDateTime
        #     FROM {table}
        #     GROUP BY ID_Global, EmployeeID, AccessDate, AccessTime, AccessDateTime 
        #     ORDER BY AccessDateTime
        # """
        query = f"""
            SELECT 
                ID_Global, 
                EmployeeID,
                AccessDate,
                AccessTime,
                AccessDateTime
            FROM {table}
            GROUP BY ID_Global, EmployeeID, AccessDate, AccessTime, AccessDateTime 
            ORDER BY AccessDateTime
        """

        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        if not results:
            frappe.log_error("No records found in HikVision database.", "Fetch Data Error")
            return [], None

        last_record = results[-1]
        return results, last_record

    except pyodbc.Error as e:
        frappe.throw(f"Database connection failed: {e}")

@frappe.whitelist()
def fetch_hik_vision_records():
    records, last_record = fetch_data()
    if not records:
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

    enqueue_create_attendance()

@frappe.whitelist()
def create_attendance():
    attendance_records = frappe.get_all('Hik Vision Attendance',
        fields=['employee_id', 'access_date', 'MIN(access_time) as entry', 'MAX(access_time) as exit_time'],
        group_by='employee_id, access_date',
        order_by='employee_id, access_date')

    result = []
    for record in attendance_records:
        employee_details = frappe.get_value('Employee', {'attendance_device_id': record['employee_id']}, ['name', 'employee_name'], as_dict=True)
        
        if employee_details:
            result.append({
                'employee': employee_details['name'],
                'full_name': employee_details['employee_name'],
                'employee_id': record['employee_id'],
                'date': record['access_date'],
                'entry': record['entry'],
                'exit_time': record['exit_time']
            })

    for record in result:
        entry_time = record.get('entry')
        exit_time = record.get('exit_time')

        time_diff = get_datetime(exit_time) - get_datetime(entry_time)
        hours_worked = time_diff.total_seconds() / 3600.0
        
        if hours_worked >= 8:
            status = "Present"
        elif hours_worked >= 4:
            status = "Half Day"
        else:
            status = "Absent"

        if not frappe.db.exists('Attendance', {'employee': record['employee'], 'attendance_date': record['date']}):
            doc = frappe.new_doc("Attendance")
            doc.employee = record.get('employee')
            doc.attendance_date = get_datetime(record.get('date'))
            doc.status = status
            doc.submit()

    frappe.db.commit()
@frappe.whitelist()
def enqueue_create_attendance():
    enqueue(
        create_attendance,
        queue="long",
        now=frappe.conf.developer_mode or frappe.flags.in_test,
    )




    # create_attendance()

    # settings = frappe.get_doc("HikVision Settings", "HikVision Settings")
    # if last_record:
    #     settings.last_hik_vision_record_id = last_record['ID_Global']
    #     settings.save()
        # frappe.db.commit()
# def process_records():
#     records = frappe.get_all(
#         "Hik Vision Attendance",
#         fields=["employee_id", "access_date_time"]
#     )
#     employee_ids = set(record['employee_id'] for record in records)
#     for employee_id in employee_ids:
#         employee_records = [frappe.utils.get_datetime(record['access_date_time']) for record in records if record['employee_id'] == employee_id]
#         employee_records.sort()
#         record_groups = []
#         if employee_records:
#             start_time = employee_records[0]
#             end_time = start_time + timedelta(hours=24)
#             current_window = []
#             for record in employee_records:
#                 if record < end_time:
#                     current_window.append(record)
#                 else:
#                     record_groups.append({
#                         'window_start': start_time,
#                         'window_end': end_time,
#                         'records': current_window
#                     })
#                     start_time = record
#                     end_time = start_time + timedelta(hours=24)
#                     current_window = [record]
#             if current_window:
#                 record_groups.append({
#                     'window_start': start_time,
#                     'window_end': end_time,
#                     'records': current_window
#                 })
#         for group in record_groups:
#             process_record_group(employee_id, group)

# def process_record_group(employee_id, record_group):
#     records = record_group['records']
#     if records:
#         create_checkin_checkout_entries(employee_id, records[0], "IN")
#         create_checkin_checkout_entries(employee_id, records[-1], "OUT")
#         enqueue_create_attendance()

# def create_checkin_checkout_entries(employee_id, access_datetime, log_type):
#     doc = frappe.new_doc("Employee Checkin")
    # employee_record = frappe.get_all("Employee", filters={"attendance_device_id": employee_id}, fields=["name"])
    
    # if employee_record:
    #     employee_id = employee_record[0].name
    #     employee_doc = frappe.get_doc("Employee", employee_id)
    # else:
    #     frappe.log_warning(f"No employee found for ID: {employee_id}", "Checkin Entry Warning")
    #     return
        # if employee_doc:
    # doc.employee = employee_id
    # doc.time = access_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # doc.device_id = access_datetime
    # doc.log_type = log_type
    # doc.insert()
    # frappe.db.commit()


@frappe.whitelist()
def delete_records():
    frappe.db.delete("Hik Vision Attendance")

@frappe.whitelist()
def delete_records_checkin():
    frappe.db.delete("Attendance")
    frappe.db.delete("Employee Checkin")
