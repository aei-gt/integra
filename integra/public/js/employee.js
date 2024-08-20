frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        frm.add_custom_button(__('View Hik Attendance Report'), function() {
            frappe.set_route('query-report', 'Employee Attendance', {
                employee: frm.doc.name
            });
        });
    },

    custom_hik_vision_id: function(frm) {
        frappe.call({
            method: 'integra.events.hik_vision.get_data',
            args: {
                name: frm.doc.custom_hik_vision_id,
            },
            callback: (r) => {
                if (r.message) {
                    let data = r.message;
                    console.log(data);
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
