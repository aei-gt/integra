
import frappe

def change_name(doc, method):
    employee_name = doc.first_name + " " + doc.middle_name + "," + doc.last_name + " " + doc.custom_segundo_apellido + " " + "DE" + " " + doc.custom_apellido_de_casada
    if doc.custom_apellido_de_casada:
        doc.db_set("employee_name", employee_name)
        frappe.db.commit()