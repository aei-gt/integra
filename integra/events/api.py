import frappe
from frappe.utils import strip_html_tags
import requests
import pandas as pd
import os
import base64
from frappe.utils.file_manager import get_file_path
from datetime import datetime


def send_new_client_whatsapp_message(doc, method=None):
	doc.is_new_doc = True
	naming_series = doc.name 
	parts = naming_series.split('-')
	if len(parts) == 3:
		year = parts[1][2:] 
		doc_number = parts[2].lstrip('0')
		doc.custom_id_document = f"{year}-{doc_number}"
		doc.save()
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	plain_description = ''
	if doc.description:
		plain_description = strip_html_tags(doc.description)
	current_datetime = datetime.now()
	current_date = current_datetime.strftime("%d-%m-%y")
	current_time = current_datetime.strftime("%H:%M")
	base_url = frappe.utils.get_url()  # This will fetch the base URL of your Frappe site
	doc_name = f"{base_url}/app/issue/{doc.name}"


	# Send message to custom WhatsApp number if available
	if doc.custom_whatsapp_number:
		client_message = settings.client_message
		client_message = client_message.replace("(customer)", str(doc.customer)).replace("(document_id)", str(doc.custom_id_document)).replace("(date)", str(current_date)).replace("(time)", str(current_time)).replace("(description)", str(plain_description))
		send_message("923077773477", client_message, api_key, url)

	# Send message to last employee in custom movement if available
	if doc.custom_movement and len(doc.custom_movement) > 0:
		# emp_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {doc.custom_movement[-1].notes}"
		last_movement = doc.custom_movement[-1]
		if last_movement.empleado:
			employee = frappe.get_doc("Employee", last_movement.empleado)
			emp_message = settings.employee_message
			emp_message = emp_message.replace("(employee_name)", f"{employee.first_name} {employee.last_name}").replace("(document_id)", str(doc.custom_id_document)).replace("(docname)", str(doc.name)).replace("(doc_url)", str(doc_name)).replace("(subject)", str(doc.subject))
			send_message("923327773477", emp_message, api_key, url)

	# Send message to employee linked to issue type, if available
	if doc.issue_type:
		issue_type = frappe.get_doc("Issue Type", doc.issue_type)
		# if issue_type.description:
		# 	manager_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {issue_type.description}"
		# else:
		# 	manager_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {doc.custom_movement[-1].notes}"
		if issue_type.custom_employee:                             
			employee = frappe.get_doc("Employee", issue_type.custom_employee)
			manager_message = settings.manager_message
			manager_message = manager_message.replace("(employee_name)", f"{employee.first_name} {employee.last_name}").replace("(document_id)", str(doc.custom_id_document)).replace("(docname)", str(doc.name)).replace("(doc_url)", str(doc_name)).replace("(subject)", str(doc.subject))
			send_message("923077773477", manager_message, api_key, url)

	
def send_updated_whatsapp_message(doc, method=None):
	if doc.get("is_new_doc"):
		return

	old_doc = doc.get_doc_before_save()
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	plain_description = ''
	if doc.description:
		plain_description = strip_html_tags(doc.description)
	base_url = frappe.utils.get_url()  # This will fetch the base URL of your Frappe site
	doc_name = f"{base_url}/app/issue/{doc.name}"
	current_datetime = datetime.now()
	current_date = current_datetime.strftime("%d-%m-%y")
	current_time = current_datetime.strftime("%H:%M")

	# Send message if there's a new entry in custom movement
	if doc.custom_movement and (len(old_doc.custom_movement) < len(doc.custom_movement)):
		# emp_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {doc.custom_movement[-1].notes}"
		last_movement = doc.custom_movement[-1]
		if last_movement.empleado:
			employee = frappe.get_doc("Employee", last_movement.empleado)
			emp_message = settings.employee_message
			emp_message = emp_message.replace("(employee_name)", f"{employee.first_name} {employee.last_name}").replace("(document_id)", str(doc.custom_id_document)).replace("(docname)", str(doc.name)).replace("(doc_url)", str(doc_name)).replace("(subject)", str(doc.subject))
			send_message(employee.cell_number, emp_message, api_key, url)
	
	# Set manager and send message if issue type has a custom employee
	if doc.issue_type and doc.status != "Closed":
		issue_type = frappe.get_doc("Issue Type", doc.issue_type)
		# if issue_type.description:
		# 	manager_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {issue_type.description}"
		# else:
		# 	manager_message = f"Se le asigno la solicitud con referencia {doc.custom_id_document} this id_document with the full url {doc_name}, asunto & {doc.custom_movement[-1].notes}"
		if issue_type.custom_employee:
			manager = frappe.get_doc("Employee", issue_type.custom_employee)
			manager_message = settings.manager_message
			manager_message = manager_message.replace("(employee_name)", f"{manager.first_name} {manager.last_name}").replace("(document_id)", str(doc.custom_id_document)).replace("(docname)", str(doc.name)).replace("(doc_url)", str(doc_name)).replace("(subject)", str(doc.subject))
			send_message(manager.cell_number, manager_message, api_key, url)
	
	
	if doc.status == "Closed":
		manager_number = None
		if doc.issue_type:
			issue_type = frappe.get_doc("Issue Type", doc.issue_type)
			if issue_type.custom_employee:
				manager = frappe.get_doc("Employee", issue_type.custom_employee)
				manager_number = manager.cell_number
		final_message = settings.final_message
		message = final_message.replace("(document_id)", str(doc.custom_id_document))
		# message = f"Your emergency issue no. {doc.custom_id_document} is Closed."
		if manager_number:
			send_message(manager_number, message, api_key, url)
		if doc.custom_whatsapp_number:
			send_message(doc.custom_whatsapp_number, message, api_key, url)
			file_name = frappe.get_all("File", {"attached_to_name" : doc.name, "attached_to_doctype" : doc.doctype})
			for row in file_name:
				file_doc = frappe.get_doc("File", row.name)
				file_path = frappe.get_site_path(file_doc.file_url.lstrip("/"))
				with open(file_path, "rb") as image_file:
					base64_string = base64.b64encode(image_file.read()).decode('utf-8')
				file_extension = file_doc.file_url.split('.')[-1].lower()
				mediatype = "document" if file_extension in ["pdf", "doc", "docx"] else "image"
				media_url = "https://api2.fraijanes.gt/message/sendMedia/MDF V2 Global"
				api_key = "1A6FEA9F48E3-4386-A050-5B13FE23ECBC"
				media = base64_string
				send_media_message(doc.custom_whatsapp_number, api_key, media_url, media, mediatype, file_doc.file_name)


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


def send_media_message(number, api_key, media_url, media, mediatype, file_name):
	"""Helper function to send WhatsApp message."""

	if mediatype == "document":
		mimetype = "document/pdf"
	else:
		mimetype = "image/jpeg"

	payload = {
        "number": number,
		"mediatype": mediatype,
        "media": media,
		"mimetype": mimetype ,
		"fileName": file_name
	}
	headers = {
		"apikey": api_key,
		"Content-Type": "application/json"
	}
	try:
		response = requests.post(media_url, json=payload, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as e:
		frappe.log_error(message=str(e), title="WhatsApp Message Sending Failed")

