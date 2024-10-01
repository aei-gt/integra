import pyodbc
import frappe
from datetime import datetime, timedelta
from frappe.utils import get_datetime

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
        'timeout=30;'
    )

    try:
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
            return [], None  # Handle no results gracefully

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
    
    process_records()

    settings = frappe.get_doc("HikVision Settings", "HikVision Settings")
    if last_record:
        settings.last_hik_vision_record_id = last_record['ID_Global']
        settings.save()
        frappe.db.commit()

def process_records():
    records = frappe.get_all(
        "Hik Vision Attendance",
        fields=["employee_id", "access_date_time"]
    )
    employee_ids = set(record['employee_id'] for record in records)
    for employee_id in employee_ids:
        employee_records = [frappe.utils.get_datetime(record['access_date_time']) for record in records if record['employee_id'] == employee_id]
        employee_records.sort()
        record_groups = []
        if employee_records:
            start_time = employee_records[0]
            end_time = start_time + timedelta(hours=24)
            current_window = []
            for record in employee_records:
                if record < end_time:
                    current_window.append(record)
                else:
                    record_groups.append({
                        'window_start': start_time,
                        'window_end': end_time,
                        'records': current_window
                    })
                    start_time = record
                    end_time = start_time + timedelta(hours=24)
                    current_window = [record]
            if current_window:
                record_groups.append({
                    'window_start': start_time,
                    'window_end': end_time,
                    'records': current_window
                })
        for group in record_groups:
            process_record_group(employee_id, group)

def process_record_group(employee_id, record_group):
    records = record_group['records']
    if records:
        create_checkin_checkout_entries(employee_id, records[0], "IN")
        create_checkin_checkout_entries(employee_id, records[-1], "OUT")
        create_attendance()

def create_checkin_checkout_entries(employee_id, access_datetime, log_type):
    doc = frappe.new_doc("Employee Checkin")
    employee_record = frappe.get_all("Employee", filters={"attendance_device_id": employee_id}, fields=["name"])
    
    if employee_record:
        employee_id = employee_record[0].name
        employee_doc = frappe.get_doc("Employee", employee_id)
    else:
        frappe.log_warning(f"No employee found for ID: {employee_id}", "Checkin Entry Warning")
        return  # Exit if no employee found

    if employee_doc:
        doc.employee = employee_doc.name
        doc.time = access_datetime.strftime('%Y-%m-%d %H:%M:%S')
        doc.device_id = access_datetime
        doc.log_type = log_type
        doc.insert()
        frappe.db.commit()

@frappe.whitelist()
def create_attendance():
    try:
        attendance_records = frappe.db.sql("""
            SELECT
                e.name as employee,
                e.employee_name as full_name,
                h.employee_id,
                h.access_date as date,
                MIN(h.access_time) as entry,
                MAX(h.access_time) as exit_time
            FROM
                `tabHik Vision Attendance` h
            JOIN
                `tabEmployee` e
            ON
                h.employee_id = e.attendance_device_id
            GROUP BY
                h.employee_id, h.access_date
            ORDER BY
                h.employee_id, h.access_date
        """, as_dict=True)

        created_count = 0
        for record in attendance_records:
            entry_time = record.get('entry')
            exit_time = record.get('exit_time')
            time_diff = get_datetime(exit_time) - get_datetime(entry_time)
            hours_worked = time_diff.total_seconds() / 3600.0

            if hours_worked >= 7:
                status = "Present"
            elif hours_worked >= 4:
                status = "Half Day"
            else:
                status = "Absent"
            doc = frappe.new_doc("Attendance")
            doc.employee = record.get('employee')
            doc.attendance_date = get_datetime(record.get('date'))
            doc.status = status
            doc.save()
            doc.submit()
            created_count += 1  # Increment the created count

        frappe.db.commit()
        return frappe.msgprint(f"Successfully created {created_count} attendance records")

    except frappe.exceptions.QueryTimeoutError as e:
        frappe.log_error(f"Lock wait timeout exceeded: {str(e)}", "Error in create_attendance")
        return frappe.msgprint("Unable to create attendance due to a lock wait timeout. Please try again later.")
    except Exception as e:
        frappe.log_error(f"An error occurred: {str(e)}", "Error in create_attendance")
        return frappe.msgprint("An unexpected error occurred. Please try again later.")

@frappe.whitelist()
def delete_records():
    frappe.db.delete("Hik Vision Attendance")

@frappe.whitelist()
def delete_records_checkin():
    frappe.db.delete("Attendance")
