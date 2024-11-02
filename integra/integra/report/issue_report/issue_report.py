# Copyright (c) 2024, AEI and contributors
# For license information, please see license.txt

import frappe

# Define columns
columns = [
    {"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "Issue", "width": 150},
    {"label": "ID Document", "fieldname": "custom_id_document", "fieldtype": "Data", "width": 100},
    {"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "width": 150},
    {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
    {"label": "WhatsApp", "fieldname": "custom_whatsapp_number", "fieldtype": "Data", "width": 120},
    {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
    {"label": "Issue Type", "fieldname": "issue_type", "fieldtype": "Data", "width": 120},
    {"label": "Details", "fieldname": "description", "fieldtype": "Text", "width": 200},
    {"label": "Movements", "fieldname": "movements", "fieldtype": "Text", "width": 300}
]

# Fetch data with filters
def execute(filters=None):
    data = []

    # Build filter conditions based on user input
    conditions = {}
    if filters.get("custom_id_document"):
        conditions["custom_id_document"] = filters["custom_id_document"]
    if filters.get("name"):
        conditions["name"] = filters["name"]
    if filters.get("customer"):
        conditions["customer"] = filters["customer"]

    # Query Issues with specified conditions
    issues = frappe.get_all("Issue", 
                            filters=conditions,
                            fields=["name", "custom_id_document", "subject", "customer", "custom_whatsapp_number",
                                    "status", "priority", "issue_type", "description"])

    for issue in issues:
        # Get all rows from the Issue Movement child table for this issue
        movements = frappe.get_all("Issue Movement",
                                   filters={"parent": issue.name},
                                   fields=["empleado", "departamento", "notas"])

        # Format each movement as a detailed list for the report
        movement_details = "\n".join(
            [f"Employee: {m.empleado}, Department: {m.departamento}, Notes: {m.notas}" for m in movements]
        )

        # Append issue data with movement details
        data.append({
            "name": issue.name,
            "custom_id_document": issue.custom_id_document,
            "subject": issue.subject,
            "customer": issue.customer,
            "custom_whatsapp_number": issue.custom_whatsapp_number,
            "status": issue.status,
            "priority": issue.priority,
            "issue_type": issue.issue_type,
            "description": issue.description,
            "movements": movement_details  # all rows in formatted text
        })

    return columns, data
