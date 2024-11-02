// Copyright (c) 2024, AEI and contributors
// For license information, please see license.txt

frappe.query_reports["Issue Report"] = {
	"filters": [
		{
			"fieldname": "name",
            "label": __("ID"),
            "fieldtype": "Link",
            "options": "Issue",
            "placeholder": __("Enter Issue ID"),
            "width": "80"
        },
        {
			"fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "placeholder": __("Select Customer"),
            "width": "80"
        },
		{
			"fieldname": "custom_id_document",
			"label": __("ID Document Short"),
		   "fieldtype": "Link",
			"options": "Issue",
			"placeholder": __("Enter Document ID"),
			"width": "80"
		},
    ]
};
