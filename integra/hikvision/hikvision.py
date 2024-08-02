import frappe
import mysql.connector

def fetch_data():
    settings = frappe.get_doc("HikVision Settings", "HikVision Settings")

    host = settings.get("host")
    user = settings.get("user")
    password = settings.get("password")
    database = settings.get("database")
    table = settings.get("table")

    # Connect to the database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor(dictionary=True)

    query = f"""
        SELECT 
            ID, 
            EmployeeID,
            AccessDate,
            AccessTime,
            AccessDateTime
        FROM {table}
        GROUP BY EmployeeID, AccessDateTime LIMIT 5
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

@frappe.whitelist()
def fetch_hik_vision_records():
    records = fetch_data()

    for record in records:
        doc = frappe.get_doc({
            "doctype": "Hik Vision Attendance",
            "id": record['ID'],
            "employee_id": record['EmployeeID'],
            "access_date_time": record['AccessDateTime'],
            "access_date": record['AccessDate'],
            "access_time": record['AccessTime']
        })
        doc.insert()
        frappe.db.commit()