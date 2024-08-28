// Copyright (c) 2024, AEI and contributors
// For license information, please see license.txt

frappe.query_reports["Data of Employee Cronos"] = {
	"filters": [
		{
            fieldname: 'employee_name',
            label: __('Employee Name'),
			fieldtype: 'Link',
            options: 'Employee',
		
           
        },
		{
            fieldname: 'department',
            label: __('Department'),
            fieldtype: 'Link',
            options: 'Department',
		
           
        },
	],
    get_datatable_options(options) {
		return Object.assign(options, {
			cellHeight: 150
		});
	},
};
