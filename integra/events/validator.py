
import frappe
@frappe.whitelist()
def validator(doc,method=None):
    nit = nit_validator(doc.custom_nit)
    dpi = dpi_validator(doc.custom_cui)
    if not nit:
        frappe.msgprint(f"NIT value is not in the correct format. Please provide the value in this format: 'xxxxxxxx-x'")
    if not dpi:
        frappe.msgprint(f"CUI/DPI value is not in the correct format. Please provide the value in this format: 'xxxxxxxxxxxxx'")


      
    change_name(doc,method=None)


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





import re


def dpi_validator(dpi):
    """
    Validador de DPI Guatemala

    Args:
        dpi (str): DPI

    Returns:
        bool: True/False
    """
    try:
        dpi = str(dpi).strip()
        if not dpi:
            return False

        # Expresion regular, para validar si aplica el patron
        dpi_reg_exp = re.compile('^[0-9]{4}\s?[0-9]{5}\s?[0-9]{4}$')
        if not dpi_reg_exp.match(dpi):
            return False

        dpi = dpi.replace('\s', '').replace(' ', '')

        departamento = int(dpi[10])
        municipio = int(dpi[11:13])
        numero = str(dpi[0:8])
        verificador = int(dpi[8:9])

        municipios_por_depto = [
            17, # 01 - Guatemala tiene: 17 municipios.
            8,  # 02 - El Progreso tiene: 8 municipios.
            16, # 03 - Sacatepéquez tiene: 16 municipios.
            16, # 04 - Chimaltenango tiene: 16 municipios.
            13, # 05 - Escuintla tiene: 13 municipios.
            14, # 06 - Santa Rosa tiene: 14 municipios.
            19, # 07 - Sololá tiene: 19 # municipios.
            8,  # 08 - Totonicapán tiene: 8 municipios.
            24, # 09 - Quetzaltenango tiene: 24 municipios.
            21, # 10 - Suchitepéquez tiene: 21 municipios.
            9,  # 11 - Retalhuleu tiene: 9 municipios.
            30, # 12 - San Marcos tiene: 30 municipios.
            32, # 13 - Huehuetenango tiene: 32 municipios.
            21, # 14 - Quiché tiene: 21 municipios.
            8,  # 15 - Baja Verapaz tiene: 8 municipios.
            17, # 16 - Alta Verapaz tiene: 17 municipios.
            14, # 17 - Petén tiene: 14 municipios.
            5,  # 18 - Izabal tiene: 5 municipios.
            11, # 19 - Zacapa tiene: 11 municipios.
            11, # 20 - Chiquimula tiene: 11 municipios.
            7,  # 21 - Jalapa tiene: 7 municipios.
            17, # 22 - Jutiapa tiene: 17 municipios.
        ]

        if departamento == 0 or municipio == 0: return False
        if departamento > len(municipios_por_depto): return False
        if municipio > municipios_por_depto[departamento-1]: return False

        # Se verifica el correlativo co base en el algoritmo del complemento 11
        total = 0
        numero = [int(x) for x in str(numero)]

        for i in range(0, len(numero)):
            total += numero[i] * (i+2)

        modulo = total % 11

        return modulo == verificador

    except:
        return False
    

def nit_validator(nit):
    """
    Validador de NIT Guatemala

    Args:
        nit (str): NIT

    Returns:
        bool: True/False
    """
    try:
        nit = str(nit)
        if not nit:
            return False

        # Expresion regular, para validar si aplica el patron
        nit_reg_exp = re.compile('^[0-9]+(-?[0-9kK])?$')
        if not nit_reg_exp.match(nit):
            return False

        # Elimacion guiones
        nit = nit.replace('-', '')
        # Digito verificador
        last_position = nit[-1]
        # Digitos excluyendo el ultimo
        dig_nit = nit[0:-1]
        # Conversion digito verificados a str y minuscula (en caso aplique)
        checker = str(last_position).lower()

        factor_nit = len(dig_nit) + 1
        total = 0

        for i in range(0, len(dig_nit)):
            digit_nit = int(dig_nit[i])
            total += digit_nit * factor_nit
            factor_nit = factor_nit - 1

        modulus = (11 - (total % 11)) % 11
        computed_checker = "k" if modulus == 10 else str(modulus)

        if checker == computed_checker:
            return True
        else:
            return False

    except:
        return False