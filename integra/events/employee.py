import frappe

def change_name(doc, method):
    first_name = doc.get('first_name', '').strip()
    middle_name = doc.get('middle_name', '').strip()
    last_name = doc.get('last_name', '').strip()
    segundo_apellido = doc.get('custom_segundo_apellido', '').strip()
    apellido_de_casada = doc.get('custom_apellido_de_casada', '').strip()

    name_parts = [first_name]
    if middle_name:
        name_parts.append(middle_name)
    name_parts.append(last_name)
    if segundo_apellido:
        name_parts.append(segundo_apellido)
    employee_name = ' '.join(name_parts)
    if apellido_de_casada:
        employee_name += f" DE {apellido_de_casada}"
    doc.employee_name = employee_name
