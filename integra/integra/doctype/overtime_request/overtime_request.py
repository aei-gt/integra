# Copyright (c) 2025, AEI and contributors
# For license information, please see license.txt
import frappe
import requests
# import json
from datetime import datetime, timedelta
from frappe.model.document import Document


class OvertimeRequest(Document):
	def on_submit(self):		
		if self.overtime_approver and self.overtime_hours and self.status == "Approved":
			doc = frappe.get_doc("Employee", self.employee)
			existing_entry = None
			for entry in doc.custom_over_time_details:
				if entry.overtime_request == self.name:
					existing_entry = entry
					break
			if existing_entry:
				# If values are same, do nothing
				if (
					existing_entry.overtime_request == self.name and
					existing_entry.over_time == self.overtime_hours and
					existing_entry.date == self.date
				):
					return

				existing_entry.overtime_request = self.name
				existing_entry.over_time = self.overtime_hours
				existing_entry.date = self.date
			else:
				doc.append("custom_over_time_details", {
					"overtime_request": self.name,
					"over_time": self.overtime_hours,
					"date": self.date
				})
			overtime_hours=add_time_fields(self.overtime_hours,doc.custom_total_overtime)
			doc.custom_total_overtime = overtime_hours
			doc.save(ignore_permissions=True)
			doc.reload()
			frappe.db.commit()
			# frappe.msgprint(f"{overtime_hours}")





			# Send WhatsApp message to the approver
			doc_set=frappe.get_single("Evolution Api Settings")
			url = doc_set.url
			api_key = doc_set.api_key
			approver_mob=frappe.get_doc("User",self.overtime_approver)		
			number = self.approver_mobile
			message = f"Hi {approver_mob.full_name}, an overtime request for {self.employee}:{self.full_name} has been Requested for Overtime {self.overtime_hours} hours. Please review and approve it."
			send_whatsapp_message(number, message, api_key, url)
		else:
			frappe.throw(" Chnage the Status to Approved")

	

def send_whatsapp_message(number, message, api_key, url):
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
		


def add_time_fields(time1, time2):
    fmt = "%H:%M:%S"

    # If time2 is None, assume it as "00:00:00"
    time1 = str(time1) if time1 else "00:00:00"
    time2 = str(time2) if time2 else "00:00:00"

    # Convert string time fields to datetime objects
    t1 = datetime.strptime(time1, fmt)
    t2 = datetime.strptime(time2, fmt)

    # Sum the timedelta values
    total_seconds = (t1 - datetime(1900, 1, 1)).total_seconds() + (t2 - datetime(1900, 1, 1)).total_seconds()
    
    # Convert total seconds back to time format
    total_time = str(timedelta(seconds=total_seconds))
    
    return total_time