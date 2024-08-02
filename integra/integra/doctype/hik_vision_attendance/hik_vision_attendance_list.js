frappe.listview_settings['Hik Vision Attendance'] = {
    onload: function (listview) {
        listview.page.add_button(__('Fetch Hik Vision Records'), function () {
            frappe.call({
                method: 'integra.hikvision.hikvision.fetch_hik_vision_records',
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint(__('Records have been fetched and processed.'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
