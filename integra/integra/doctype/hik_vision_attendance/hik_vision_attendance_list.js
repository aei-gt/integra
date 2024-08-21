frappe.listview_settings['Hik Vision Attendance'] = {
    onload: function (listview) {
        // listview.page.add_button(__('Fetch Hik Vision Records'), function () {
        //     frappe.call({
        //         method: 'integra.hikvision.hikvision.fetch_hik_vision_records',
        //         callback: function (response) {
        //             if (response) {
        //                 frappe.show_alert(__('Records have been fetched and processed.'));
        //                 listview.refresh();
        //             }
        //         }
        //     });
        // });

        listview.page.add_button(__('Delete Records'), function () {
            frappe.call({
                method: 'integra.hikvision.hikvision.delete_records',
                callback: function (response) {
                    if (response) {
                        frappe.show_alert(__('Records have been Deleted.'));
                        listview.refresh();
                    }
                }
            });
        });
        
        
        listview.page.add_button(__('Fetch Last Records'), function () {
            frappe.call({
                method: 'integra.hikvision.checkin.fetch_hik_vision_records',
                callback: function (response) {
                    if (response) {
                        frappe.show_alert(__('Records have been fetched and processed'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};
