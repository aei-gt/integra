import frappe

def change_name(doc, method):
    def safe_get(doc, key):
        value = doc.get(key, '')
        return value.strip() if value else ''
    
    first_name = safe_get(doc, 'first_name')
    middle_name = safe_get(doc, 'middle_name')
    last_name = safe_get(doc, 'last_name')
    segundo_apellido = safe_get(doc, 'custom_segundo_apellido')
    apellido_de_casada = safe_get(doc, 'custom_apellido_de_casada')

    name_parts = []
    if first_name:
        name_parts.append(first_name)
    if middle_name:
        name_parts.append(middle_name)
    if last_name:
        name_parts.append(last_name)
    if segundo_apellido:
        name_parts.append(segundo_apellido)

    employee_name = ' '.join(name_parts)

    if apellido_de_casada:
        employee_name += f" DE {apellido_de_casada}"

    doc.employee_name = employee_name
