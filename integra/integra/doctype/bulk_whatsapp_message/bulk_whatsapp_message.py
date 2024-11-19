# Copyright (c) 2024, AEI and contributors
# For license information, please see license.txt

import frappe
import requests
import pandas as pd
import os
import base64
from frappe.utils.file_manager import get_file_path
from frappe.model.document import Document

class BulkWhatsappMessage(Document):
    def validate(self):
        if self.attach_file:
            file_path = get_file_path(self.attach_file)
            file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension
            
            # Load the file based on its extension
            if file_extension in ['.xls', '.xlsx']:
                data = pd.read_excel(file_path)  # Read Excel files
            elif file_extension == '.csv':
                data = pd.read_csv(file_path)  # Read CSV files
            else:
                frappe.throw("Unsupported file format. Please upload a .xls, .xlsx, or .csv file.")
            
            # Clear the list to avoid duplicates
            self.whatsapp_number = []
            
            # Iterate through the rows and append to the child table
            for index, row in data.iterrows():
                self.append('whatsapp_number', {
                    'phone_no': row.get('Phone Number', ''),  
                    'property_id': row.get('Property_id', ''),
                    'customer_name': row.get('Name_customer', ''),
                    'message': row.get('Message', ''),
                })    
        # if self.attach_file:
        #     file_path = get_file_path(self.attach_file)
        #     data = pd.read_excel(file_path)
        #     # frappe.msgprint(f"Columns in Excel file: {', '.join(data.columns)}")
        #     self.whatsapp_number = []
        #     for inex, row in data.iterrows():
        #         self.append('whatsapp_number', {
        #             'name1': row['Name 1'],
        #             'phone_no': row['Phone Number']  
        #         })
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
            message = f"hi {row.customer_name} your property {row.property_id} have a limit of (limit_account). Please made payments"
            number = row.phone_no
            media = base64_string

            send_message(number, message, api_key, url)
            if self.image:
                send_media_message(number, api_key, media_url, media, mediatype="image")

def send_media_message(number, api_key, media_url, media, mediatype="image"):
	"""Helper function to send WhatsApp message."""
	payload = {
		"mediatype": "image",
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