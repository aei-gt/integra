import frappe
from frappe.utils import strip_html_tags
import requests


def send_new_client_whatsapp_message(doc, method=None):
	
	naming_series = doc.name 
	parts = naming_series.split('-')
	if len(parts) == 3:
		year = parts[1][2:] 
		doc_number = parts[2].lstrip('0')
		doc.custom_id_document = f"{year}{doc_number}"
		doc.save()
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	
	plain_description = strip_html_tags(doc.description)
	message = f'Issue no. {doc.name} is created with description "{plain_description}"'
	
	# Send message to custom WhatsApp number if available
	if doc.custom_whatsapp_number:
		send_message(doc.custom_whatsapp_number, message, api_key, url)

	# Send message to employee linked to issue type, if available
	if doc.issue_type:
		issue_type = frappe.get_doc("Issue Type", doc.issue_type)
		if issue_type.custom_employee:                             
			employee = frappe.get_doc("Employee", issue_type.custom_employee)
			send_message(employee.cell_number, message, api_key, url)

	# Send message to last employee in custom movement if available
	if doc.custom_movement and len(doc.custom_movement) > 0:
		last_movement = doc.custom_movement[-1]
		if last_movement.empleado:
			employee = frappe.get_doc("Employee", last_movement.empleado)
			send_message(employee.cell_number, message, api_key, url)
	
def send_updated_whatsapp_message(doc, method=None):
	if doc.creation == doc.modified:
		return
	old_doc = doc.get_doc_before_save()
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	plain_description = strip_html_tags(doc.description)
	message = f'Issue no. {doc.name} is updated with description "{plain_description}"'

	# Send message if there's a new entry in custom movement
	if doc.custom_movement and (len(old_doc.custom_movement) < len(doc.custom_movement)):
		last_movement = doc.custom_movement[-1]
		if last_movement.empleado:
			employee = frappe.get_doc("Employee", last_movement.empleado)
			send_message(employee.cell_number, message, api_key, url)
	
	# Set manager and send message if issue type has a custom employee
	if doc.issue_type and doc.status != "Closed":
		issue_type = frappe.get_doc("Issue Type", doc.issue_type)
		if issue_type.custom_employee:
			manager = frappe.get_doc("Employee", issue_type.custom_employee)
			send_message(manager.cell_number, message, api_key, url)
	
	# Send message if the issue status is closed
	if doc.status == "Closed":
		manager_number = None
		if doc.issue_type:
			issue_type = frappe.get_doc("Issue Type", doc.issue_type)
			if issue_type.custom_employee:
				manager = frappe.get_doc("Employee", issue_type.custom_employee)
				manager_number = manager.cell_number
		message = f"Your emergency issue no. {doc.name} is Closed."
		if manager_number:
			send_message(manager_number, message, api_key, url)
		if doc.custom_whatsapp_number:
			send_message(doc.custom_whatsapp_number, message, api_key, url)


def send_message(number, message, api_key, url):
	"""Helper function to send WhatsApp message."""
	payload = {
		"number": number,
		"text": message
	}
	headers = {
		"apikey": api_key,
		"Content-Type": "application/json"
	}
	try:
		response = requests.post(url, json=payload, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as e:
		frappe.log_error(message=str(e), title="WhatsApp Message Sending Failed")