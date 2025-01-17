import frappe
import json

def validate_item_types(doc, method):
    if doc.custom__item_type:
        invalid_items = []
        for item in doc.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            if item_doc.custom_item_type != doc.custom__item_type:
                invalid_items.append(f"{item.item_code} ({item_doc.custom_item_type})")
        
        if invalid_items:
            frappe.throw(
                f"The following items have a different type than {doc.custom__item_type}:<br>"
                + "<br>".join(invalid_items)
            )
    pass




@frappe.whitelist()
def get_sales_order_items(sales_orders, item_type):
    if isinstance(sales_orders, str):
        sales_orders = json.loads(sales_orders)
    sale_items = frappe.get_all("Sales Order Item",filters={"parent": ["in", sales_orders]},fields=["item_code", "parent"])

    mismatched_items = []

    for row in sale_items:
        item_doc = frappe.get_value("Item", row.item_code, "custom_item_type")
        if item_doc and item_doc != item_type:
            row["custom_item_type"] = item_doc
            mismatched_items.append(row)

    return mismatched_items

