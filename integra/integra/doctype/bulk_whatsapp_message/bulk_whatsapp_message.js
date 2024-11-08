// Copyright (c) 2024, AEI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Whatsapp Message", {
    refresh: function(frm) {
        // Initially check if there are rows in 'whatsapp_number' when the form loads
        toggle_send_button(frm);
    },

    whatsapp_number: function(frm) {
        // Whenever the 'whatsapp_number' child table is updated, check if button should be shown or not
        toggle_send_button(frm);
    }
});

function toggle_send_button(frm) {
    if (frm.doc.whatsapp_number && frm.doc.whatsapp_number.length > 0) {
        // Add the custom button if not already added
        if (!frm.custom_buttons['Send Action']) {
            frm.add_custom_button(__('Send Action'), function() {
                // Call the Python function when the button is clicked
                frappe.call({
                    method: 'integra.integra.doctype.bulk_whatsapp_message.bulk_whatsapp_message.send_messages',
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(response) {
                        if (!response.exc) {
                            frappe.msgprint("Message Delivered successfully!");
                        }
                    }
                });
            });
        }
    } else {
        // Remove the custom button if 'whatsapp_number' has no rows
        frm.remove_custom_button('Send Action');
    }
}