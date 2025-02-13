# Copyright (c) 2025, AEI and contributors
# For license information, please see license.txt
import frappe
import requests
import json
from frappe.model.document import Document


class OvertimeRequest(Document):
	def on_submit(self):		
		if self.overtime_approver and self.overtime_hours and self.status == "Approved":
			url = "https://api2.fraijanes.gt/message/sendText/MDF V2 Global"
			api_key = "1A6FEA9F48E3-4386-A050-5B13FE23ECBC"
			approver_mob=frappe.get_doc("User",self.overtime_approver)		
			number = self.approver_mobile
			message = f"Hi {approver_mob.full_name}, an overtime request for {self.employee}:{self.full_name} has been Requested for Overtime {self.overtime_hours} hours. Please review and approve it."
			send_whatsapp_message(number, message, api_key, url)
		else:
			frappe.throw("Please Submit the Overtime Request first.")




	

def send_whatsapp_message(number, message, api_key, url):
	"""Helper function to send WhatsApp message."""
	payload = {
		"number": "+923077773477",
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
		


