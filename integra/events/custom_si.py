import frappe

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
