# Copyright (c) 2024, AEI and contributors
# For license information, please see license.txt

import frappe
import requests
import pandas as pd
import base64
from frappe.utils.file_manager import get_file_path
from frappe.model.document import Document

class BulkWhatsappMessage(Document):
    def validate(self):    
        if self.attach_file:
            file_path = get_file_path(self.attach_file)
            data = pd.read_excel(file_path)
            # frappe.msgprint(f"Columns in Excel file: {', '.join(data.columns)}")
            self.whatsapp_number = []
            for inex, row in data.iterrows():
                self.append('whatsapp_number', {
                    'name1': row['Name 1'],
                    'phone_no': row['Phone Number']  
                })
            # frappe.msgprint("Successfully added numbers to the table.")
 
@frappe.whitelist()
def send_messages(self):
    if isinstance(self, str):
        self = frappe.get_doc("Bulk Whatsapp Message", self)
        image_path = frappe.db.get_value(self.doctype, self.name, "image")
        file_name = frappe.get_all("File", {"file_url" : image_path})
        file_doc = frappe.get_doc("File", file_name[0].name)
        file_path = frappe.get_site_path("private" if file_doc.is_private else "public", file_doc.file_url.lstrip("/"))

        with open(file_path, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        settings = frappe.get_doc("Evolution Api Settings")    
        url = settings.url
        for row in self.whatsapp_number:
            url = "https://api2.fraijanes.gt/message/sendText/MDF V2 Global"
            media_url = "https://api2.fraijanes.gt/message/sendMedia/MDF%20V2%20Global"
            api_key = "1A6FEA9F48E3-4386-A050-5B13FE23ECBC"
            message = "hello"
            number = row.phone_no
            media = base64_string

            send_message(number, message, api_key, url)
            send_media_message(number, api_key, media_url, media, mediatype="image")

def send_media_message(number, api_key, media_url, media, mediatype="image"):
	"""Helper function to send WhatsApp message."""
	payload = {
		"mediatype": "image",
        "media": "./alquimia.local/public/files/WhatsApp Image 2024-08-27 at 5.51.48 PM (1).jpeg",
        "media": media,
        "number": number
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