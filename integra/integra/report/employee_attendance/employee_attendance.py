# Copyright (c) 2024, AEI and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 300},
        {"fieldname": "full_name", "label": "Employee Name", "fieldtype": "Data", "width": 300},
        {"fieldname": "employee_id", "label": "Hik Vision ID", "fieldtype": "Data", "width": 200},
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 200},
        {"fieldname": "entry", "label": "Entry", "fieldtype": "Time", "width": 200},
        {"fieldname": "exit_time", "label": "Exit", "fieldtype": "Time", "width": 200},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += " AND employee = %(employee)s"
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND access_date BETWEEN %(from_date)s AND %(to_date)s"

    attendance_records = frappe.db.sql("""
		SELECT
			e.name as employee,
			e.employee_name as full_name,
			h.employee_id,
			h.access_date as date,
			MIN(h.access_time) as entry,
			MAX(h.access_time) as exit_time
		FROM
			`tabHik Vision Attendance` h
		JOIN
			`tabEmployee` e
		ON
			h.employee_id = e.attendance_device_id
		WHERE
			1 = 1 {conditions}
		GROUP BY
			h.employee_id, h.access_date
		ORDER BY
			h.employee_id, h.access_date
	""".format(conditions=conditions), filters, as_dict=1)


    return attendance_records
