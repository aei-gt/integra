frappe.ui.form.on("Salary Slip", {
    before_save:function(frm) {    
        let deduccion = 0.0;
        let pago = 0.0;
        const earnings_rows = frm.doc.earnings || [];
        for (const row of earnings_rows) {
            if (row.salary_component) {
                frappe.db.get_doc('Salary Component', row.salary_component)
                .then(doc => {        
                    if (!doc.custom_not_show_in_print) {                        
                        pago += (row.amount); 
                        frm.set_value('custom_pago_neto', pago);                        
                    }
                })
            }
        }
        frm.set_value('custom_pago_neto', pago);
        const deduction_rows = frm.doc.deductions || [];
        for (const row of deduction_rows) {
            if (row.salary_component) {
                frappe.db.get_doc('Salary Component', row.salary_component)
                .then(doc => {     
                if (!doc.custom_not_show_in_print) {
                    deduccion +=(row.amount); 
                }
                frm.set_value('custom_deduccion_total', deduccion);                    
            })
            }
        }    
        // frm.set_value('custom_deduccion_total', deduccion);
        // frm.set_value('custom_pago_neto', pago);
        // console.log(pago);
    },
});