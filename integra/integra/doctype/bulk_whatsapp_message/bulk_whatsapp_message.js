// Copyright (c) 2024, AEI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Whatsapp Message", {
    refresh: function(frm) {
        if(!frm.is_new()){
            toggle_send_button(frm);
        }
    },
});

function toggle_send_button(frm) {
    if (frm.doc.whatsapp_number && frm.doc.whatsapp_number.length > 0) {
            frm.add_custom_button(__('Send Message'), function() {
                // Call the Python function when the button is clicked
                frappe.call({
                    method: 'integra.integra.doctype.bulk_whatsapp_message.bulk_whatsapp_message.send_messages',
                    args: {
                        self: frm.doc.name
                    },
                    callback: function(response) {
                        if (!response.exc) {
                            frappe.msgprint("Message Delivered successfully!");
                        }
                    }
                });
            });
        }
}