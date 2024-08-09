frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        frm.add_custom_button(__('View Hik Attendance Report'), function() {
            frappe.set_route('query-report', 'Employee Attendance', {
                employee: frm.doc.name
            });
        });
    }
});
