import pyodbc
import frappe
from datetime import datetime, timedelta
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

        last_record = results[-1] if results else None
        return results, last_record

    except pyodbc.Error as e:
        frappe.throw(f"Database connection failed: {e}")

@frappe.whitelist()
def fetch_hik_vision_records():
    records, last_record = fetch_data()

    # frappe.msgprint(f"{records}")
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

def create_checkin_checkout_entries(employee_id, access_datetime, log_type):
    doc = frappe.new_doc("Employee Checkin")
    doc.employee = employee_id
    doc.time = access_datetime.strftime('%Y-%m-%d %H:%M:%S')
    doc.device_id = access_datetime
    doc.log_type = log_type
    doc.insert()
    frappe.db.commit()

@frappe.whitelist()
def delete_records():
    frappe.db.delete("Hik Vision Attendance")
