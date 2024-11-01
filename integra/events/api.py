import frappe
from frappe.utils import strip_html_tags
import requests

def send_new_client_whatsapp_message(doc, method= None):
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	number = doc.custom_whatsapp_number
	plain_description = strip_html_tags(doc.description)
	message = f'Issue no. {doc.name} is created with description "{plain_description}"'
	payload = {
		"number": number,
		"text": message
	}
	headers = {
		"apikey": api_key,
		"Content-Type": "application/json"
	}
	response = requests.post(url, json=payload, headers=headers)
	response.raise_for_status()
	
def send_updated_whatsapp_message(doc, method= None):
	settings = frappe.get_doc("Evolution Api Settings", "Evolution Api Settings")
	url = settings.url
	api_key = settings.api_key
	number = ""
	if doc.issue_type:
		issue_type = frappe.get_doc("Issue Type", doc.issue_type)
		if issue_type.custom_employee:
			employee = frappe.get_doc("Employee", issue_type.custom_employee)
			number = employee.cell_number
	plain_description = strip_html_tags(doc.description)
	message = f'Issue no. {doc.name} is created with description "{plain_description}"'
	# url = "https://api2.fraijanes.gt/message/sendText/MDF V2 Global"
	payload = {
		"number": number,
		"text": message
	}
	headers = {
		"apikey": api_key,
		"Content-Type": "application/json"
	}
	response = requests.post(url, json=payload, headers=headers)
	response.raise_for_status()


	if doc.status == "Closed":
		payload = {
		"number": doc.custom_whatsapp_number,
		"text": f"Your emergency issue no. {doc.name} is Closed."
		}
		headers = {
			"apikey": api_key,
			"Content-Type": "application/json"
		}
		response = requests.post(url, json=payload, headers=headers)
		response.raise_for_status()

