# Copyright (c) 2025, AEI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OvertimeRequest(Document):
	def on_submit(self):
			if self.status == "Draft":
				frappe.throw("Please Submit the Overtime Request first.")
	