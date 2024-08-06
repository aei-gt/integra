import frappe
import pyodbc

def fetch_data():
    settings = frappe.get_doc("HikVision Settings", "HikVision Settings")

    host = settings.get("host")
    user = settings.get("user")
    password = settings.get("password")
    database = settings.get("database")
    table = settings.get("table")

    # Define the connection string
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={host};'
        f'DATABASE={database};'
        f'UID={user};'
        f'PWD={password}'
    )

    # Connect to the database
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

    return results

@frappe.whitelist()
def fetch_hik_vision_records():
    records = fetch_data()

    for record in records:
        if frappe.db.exists("Hik Vision Attendance", { "id": record['ID_Global'] }):
            continue

        doc = frappe.get_doc({
            "doctype": "Hik Vision Attendance",
            "id": record['ID_Global'],
            "employee_id": record['EmployeeID'],
            "access_date_time": record['AccessDate'],
            "access_date": record['AccessDateTime'],
            "access_time": record['AccessTime']
        })
        doc.insert()
        frappe.db.commit()

@frappe.whitelist()
def delete_records():
    frappe.db.delete("Hik Vision Attendance")
