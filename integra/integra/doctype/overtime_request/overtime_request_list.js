frappe.listview_settings['Overtime Request'] = {

    add_fields: ["status"],
    get_indicator: function (doc) {
        if (doc.status == "Approved") {
            return [__("Approved"), "green", "status,=,Approved"];
        } else if (doc.status === "Declined") {
            return [__("Declined"), "orange", "status,=,Declined"];
        }
    },
}