// let modules = ['Projects', 'Quality','CRM','Manufacturing','Support','Users','Website','Payroll','Tools','ERPNext Settings','Integrations','ERPNext Integrations','Build']
// for(let row of modules){
//     frappe.db.get_value('Workspace', row, 'parent_page')
//     .then(r => {
//         if (r.message && r.message.parent_page != "HR") {
//             frappe.db.set_value('Workspace', row, 'parent_page', '')
//                 .then(r => {
//                 let doc = r.message;
//                 doc.save()
//                 console.log(doc);
//             })
    
//         }
//     });
// }
// frappe.db.set_value("Workspace", "Projects", "parent_page", "");
// frappe.db.set_value("Workspace", "Quality", "parent_page", "");
// frappe.db.set_value("Workspace", "CRM", "parent_page", "");
// frappe.db.set_value("Workspace", "Manufacturing", "parent_page", "");
// frappe.db.set_value("Workspace", "Support", "parent_page", "");
// frappe.db.set_value("Workspace", "Users", "parent_page", "");
// frappe.db.set_value("Workspace", "Website", "parent_page", "");
// frappe.db.set_value("Workspace", "Payroll", "parent_page", "");
// frappe.db.set_value("Workspace", "Tools", "parent_page", "");
// frappe.db.set_value("Workspace", "ERPNext Settings", "parent_page", "");
// frappe.db.set_value("Workspace", "Integrations", "parent_page", "");
// frappe.db.set_value("Workspace", "ERPNext Integrations", "parent_page", "");
// frappe.db.set_value("Workspace", "Build", "parent_page", "");
