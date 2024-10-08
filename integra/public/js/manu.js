let modules = ['Projects', 'Quality','CRM','Manufacturing','Support','Users','Website','Payroll','Tools','ERPNext Settings','Integrations','ERPNext Integrations','Build']
for(let row of modules){
    frappe.db.get_value('Workspace', row, 'parent_page')
    .then(r => {
        if (r.message && r.message.parent_page != "HR") {
            frappe.db.set_value('Workspace', row, 'parent_page', 'HR')
                .then(r => {
                let doc = r.message;
                doc.save()
                console.log(doc);
            })
    
        }
    });
}
