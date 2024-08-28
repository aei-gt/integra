import frappe
from datetime import datetime

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": "Employee",
			"fieldname": "employee",
			"fieldtype": "Data",
			"width": 250
		},
		{
			"label": "Employee Name",
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 250
		},
		{
			"label": "Image",
			"fieldname": "image",
			"fieldtype": "Image",
			"width": 250,
		},
		{
			"label": "Salary",
			"fieldname": "salary",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"label": "Department",
			"fieldname": "department",
			"fieldtype": "data",
			"width": 250
		}
	]
	return columns

def get_data(filters):
		data = []
		emp_filters = {}
		
		if filters.get('employee_name'):
			emp_filters['name'] = filters.get('employee_name')
		if filters.get('department'):
			emp_filters['department'] = filters.get('department')
			
		employee_data = frappe.get_list('Employee', emp_filters, ["*"])
		
		for employee in employee_data:
			salary_docs = frappe.db.get_list("Salary Slip", {'employee': employee.name, "docstatus" : 1}, ["rounded_total"], order_by = "creation desc")
			salary = salary_docs[0].rounded_total if len(salary_docs) > 0 else 0
		
			image_html = '<img src="{0}" style="height: auto; width: 180px !important; margin: 0 25px;">'.format(employee.image) if employee.image else ''

			data.append({
				"employee": employee.name,
				"employee_name": employee.employee_name,
				"image": image_html,
				"salary": salary,
				"department": employee.department
			})

		return data
