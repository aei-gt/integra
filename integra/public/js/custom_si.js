frappe.ui.form.on('Sales Invoice', {
    custom__item_type: function(frm) {
        if (frm.doc.item_type_filter) {
            frm.fields_dict.items.grid.get_field('item_code').get_query = function() {
                return {
                    filters: {
                        item_type: frm.doc.custom__item_type
                    }
                };
            };

            if (frm.doc.references && frm.doc.references.length > 0) {
                let sales_orders = frm.doc.references
                    .filter(ref => ref.reference_doctype === 'Sales Order')
                    .map(ref => ref.reference_name);
                    console.log(sales_orders);
                    
                if (sales_orders.length > 0) {
                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Sales Order Item',
                            filters: {
                                parent: ['in', sales_orders],
                                item_type: ['!=', frm.doc.custom__item_type]
                            },
                            fields: ['item_code', 'item_type', 'parent']
                        },
                        callback: function(response) {
                            if (response.message && response.message.length > 0) {
                                console.log(response.message);
                                
                                const other_items = response.message;
                                const message = `The following items from linked Sales Orders have a different type:
                                    <ul>${other_items.map(item => `<li>${item.item_code} (${item.item_type}) in ${item.parent}</li>`).join('')}</ul>`;
                                frappe.msgprint({
                                    title: 'Different Item Types Found',
                                    message: message,
                                    indicator: 'orange'
                                });
                            }
                        }
                    });
                }
            }
        }
    }
});
