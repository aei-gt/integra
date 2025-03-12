import frappe
from frappe.model.naming import make_autoname


def autoname(doc, method):
    if doc.naming_series:
        doc.name = make_autoname(doc.naming_series)  