import frappe
@frappe.whitelist()
def get_data(name):
    docs = frappe.get_all("Hik Vision Attendance", fields=["*"], filters={"employee_id": name})
    return docs