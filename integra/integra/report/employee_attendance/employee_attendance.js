// Copyright (c) 2024, AEI and contributors
// For license information, please see license.txt
// employee_attendance_report.js

frappe.query_reports["Employee Attendance"] = {
  filters: [
    {
      fieldname: "employee",
      label: __("Employee"),
      fieldtype: "Link",
      options: "Employee",
      reqd: 0,
    },
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      default: frappe.datetime.add_days(frappe.datetime.nowdate(), -7),
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      default: frappe.datetime.nowdate(),
      reqd: 1,
    },
  ],
};
