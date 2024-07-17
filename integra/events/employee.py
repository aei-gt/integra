
import frappe

def change_name(doc, method):
    employee_name = f"""{doc.get('first_name', '')} {doc.get('middle_name', '')}, 
                        {doc.get('last_name', '')} {doc.get('custom_segundo_apellido', '')}"""

    if doc.get('custom_apellido_de_casada'):
        employee_name += f" DE {doc.get('custom_apellido_de_casada')}"
    
    doc.employee_name = employee_name
