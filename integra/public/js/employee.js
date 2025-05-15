frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        frm.add_custom_button(__('View Hik Vision Attendance Report'), function() {
                    frappe.set_route('query-report', 'Hik Vision Attendance Report', {
                        'employee': frm.doc.name
                    });
                });
    },
    attendance_device_id: function(frm) {
        frm.clear_table('custom_records');
        frappe.call({
            method: 'integra.events.hik_vision.get_data',
            args: {
                name: frm.doc.attendance_device_id,
            },
            callback: (r) => {
                if (r.message) {
                    let data = r.message;
                    for (let row of data) {
                        frm.add_child('custom_records', {
                            id: row.name,
                            employee_id: row.employee_id,
                            access_date_time: row.access_date_time,
                            access_time: row.access_time,
                            access_date: row.access_date,
                        });
                    }
                    frm.refresh_field('custom_records');
                }
            }
        });
    }
});
