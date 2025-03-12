// Copyright (c) 2025, AEI and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Attendance Report"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "reqd": 1,
            "default": frappe.datetime.add_days(frappe.datetime.nowdate(), -7)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "reqd": 1,
            "default": frappe.datetime.nowdate()
        },
        {
            "fieldname": "custom_renglon",
            "label": __("Renglon"),
            "fieldtype": "Select",
            "options": ["","011", "022", "029", "055"],  // Match the options from your Employee Doctype
        },
        {
			"fieldname": "designation",
			"label": __("Puesto"),
			"fieldtype": "Link",
			"options": "Designation",
		},
        {
			"fieldname": "department",
			"label": __("Main Department"),
			"fieldtype": "Link",
			"options": "Department",
		},
        {
            "fieldname": "show_late_entries",
            "label": __("Show Entries Late"),
            "fieldtype": "Check",
            "default": 0
        },
        {
            "fieldname": "show_early_exits",
            "label": __("Show Leave Before"),
            "fieldtype": "Check",
            "default": 0
        },

        // {
        //     "fieldname": "show_attendance_issues",
        //     "label": __("Show Attendance Issues"),
        //     "fieldtype": "Check",
        //     "default": 0
        // },
    ]
};
