


import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"fieldname": "full_name", "label": "Employee Name", "fieldtype": "Data", "width": 250},
        {"fieldname": "employee_id", "label": "Hik Vision ID", "fieldtype": "Data", "width": 150},
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 140},
        {"fieldname": "entry", "label": "Entry", "fieldtype": "Time", "width": 120},
        {"fieldname": "exit_time", "label": "Exit", "fieldtype": "Time", "width": 120},
        {"fieldname": "entry_issue", "label": "Entry Issue", "fieldtype": "Data", "width": 80},
        {"fieldname": "exit_issue", "label": "Exit Issue", "fieldtype": "Data", "width": 80},
        {"fieldname": "extra_time", "label": "Extra Time", "fieldtype": "Data", "width": 140},
        {"fieldname": "late_time", "label": "Late Time", "fieldtype": "Data", "width": 140},
    #    {
    #         "fieldname": "total_work_time", 
    #         "label": "Total Working Hours", 
    #         "fieldtype": "Data", 
    #         "width": 180,
    #         "indicator": "Green",  # You can specify an indicator here or change based on criteria
    #     }
    ]

def get_data(filters):
    if filters.get("to_date"):
        to_date = datetime.strptime(filters["to_date"], "%Y-%m-%d")
        filters["to_date"] = (to_date + timedelta(days=1)).strftime("%Y-%m-%d")

    conditions = ""
    if filters.get("employee"):
        conditions += " AND employee = %(employee)s"
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND access_date_time BETWEEN %(from_date)s AND %(to_date)s"
        
    attendance_records = frappe.db.sql("""
        SELECT
            e.name as employee,
            e.employee_name as full_name,
            h.employee_id,
            h.access_date_time as date,
            MIN(h.access_time) as entry,
            MAX(h.access_time) as exit_time,
            s.start_time,
            s.end_time 
        FROM
            `tabHik Vision Attendance` h
        JOIN
            `tabEmployee` e
        ON
            h.employee_id = e.attendance_device_id
        JOIN
            `tabShift Type` s 
        ON 
            e.default_shift = s.name
        WHERE
            1 = 1 {conditions}
        GROUP BY
            h.employee_id, h.access_date_time
        ORDER BY
            h.employee_id, h.access_date_time
    """.format(conditions=conditions), filters, as_dict=1)

    processed_records = []
    filter_applied = filters.get("show_late_entries") or filters.get("show_early_exits")
    total_extra_time = timedelta(0)
    total_late_time = timedelta(0)
    total_work_time = timedelta(0)

    for record in attendance_records:
        entry_issue = ''
        exit_issue = ''
        extra_time = timedelta(0)
        late_time = timedelta(0)

        if record.entry and record.start_time:
            entry_time = datetime.strptime(record.entry, "%H:%M:%S")
            shift_start_time = datetime.strptime(str(record.start_time), "%H:%M:%S")
            entry_issue = "<span style='color:red'>ET</span>"
            if entry_time < shift_start_time:
                entry_issue = "<span style='color:green'>OK</span>"

        if record.exit_time and record.end_time:
            exit_time = datetime.strptime(record.exit_time, "%H:%M:%S")
            shift_end_time = datetime.strptime(str(record.end_time), "%H:%M:%S")
            exit_issue = "<span style='color:red'>SA</span>"
            if exit_time > shift_end_time:
                exit_issue = "<span style='color:green'>OK</span>"

        if record.entry and record.exit_time:
            worked_hours = datetime.strptime(record.exit_time, "%H:%M:%S") - datetime.strptime(record.entry, "%H:%M:%S")
            shift_duration = shift_end_time - shift_start_time
            if worked_hours > shift_duration:
                extra_time = worked_hours - shift_duration
                total_extra_time += extra_time

            if worked_hours < shift_duration:
                exact_late_time = shift_duration - worked_hours
                late_time = exact_late_time
                total_late_time += late_time

            if worked_hours < shift_duration and record.entry == record.exit_time:
                late_time = timedelta(hours=0)  # Attendance issue, no late time.

        # Update record with issues and times
        record.entry_issue = entry_issue
        record.exit_issue = exit_issue
        record.extra_time = str(extra_time)
        record.late_time = str(late_time)

        # Add to total worked time
        # total_work_time =total_extra_time - total_late_time

        # Apply filters if required
        if filter_applied:
            if filters.get("show_late_entries") and "ET" in entry_issue:
                processed_records.append(record)
            elif filters.get("show_early_exits") and "SA" in exit_issue:
                processed_records.append(record)
        else:
            processed_records.append(record)

    # Add total work time to the last row
    processed_records.append({
        "employee": "Total",
        "full_name": "",
        "employee_id": "",
        "date": "",
        "entry": "",
        "exit_time": "",
        "entry_issue": "",
        "exit_issue": "",
        "extra_time": str(total_extra_time),
        "late_time": str(total_late_time),
        # "total_work_time": str(total_work_time)
    })

    return processed_records