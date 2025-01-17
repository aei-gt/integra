frappe.ui.form.on('Sales Invoice', {
    custom__item_type: function (frm) {
        if (frm.doc.custom__item_type) {
            frm.set_query('item_code', 'items', () => {
                return {
                    filters: {
                        custom_item_type: frm.doc.custom__item_type,
                    },
                };
            });
            const sales_orders = [...new Set(frm.doc.items
                .filter(item => item.sales_order) 
                .map(item => ({
                    sales_order: item.sales_order,
                    item_code: item.item_code
                })))];

            if (sales_orders.length > 0) {
                frappe.call({
                    method: 'integra.events.custom_si.get_sales_order_items',
                    args: {
                        sales_orders: sales_orders.map(so => so.sales_order),
                        item_type: frm.doc.custom__item_type,
                        filtered_items: sales_orders.map(so => so.item_code),
                    },
                    callback: function (response) {
                        if (response.message) {
                            const mismatched_items = response.message;
                            const message = `The following items from linked Sales Orders have a different type:
                                <ul>${mismatched_items.map(item => `<li>${item.item_code} (${item.custom_item_type}) in ${item.parent}</li>`).join('')}</ul>`;

                            frappe.msgprint({
                                title: 'Mismatched Item Types Found',
                                message: message,
                                indicator: 'purple',
                            });
                        }
                    },
                });
            }
        }
    },
});

