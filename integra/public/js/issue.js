frappe.ui.form.on('Issue', {
    // validate: function(frm) {
    //     // Check if the field has a value selected
    //     if (frm.doc.priority) {
    //         frm.set_value('custom_custom_priority', frm.doc.priority);
    //     }
    // }
    
//     onload: function(frm) {
//         // Set query on the child table field based on another field within the same row
//         frm.fields_dict['custom_movement'].grid.get_field('departamento').get_query = function(doc, cdt, cdn) {
//             // Get the current child table row
//             let row = locals[cdt][cdn];
            
//             return {
//                 filters: {
//                     // Use the value of `item_group` as a filter for `item_code`
//                     'department': row.departamento
//                 }
//             };
//         };
//     },
//     departamento: function(frm, cdt, cdn) {
//         let row = locals[cdt][cdn]
//         frm.set_query('empleado', () => {
//             return {
//                 filters: {
//                     department: row.departamento
//                 }
//             }
//         })
//     },
// });
// frm.set_query("colour", "equipment_basket", function (doc, cdt, cdn) {
//     let d = locals[cdt][cdn];
//     return {
//         filters: {
//             model: d.model,
//             discontinued:0,
//         },
//     };
});
frappe.ui.form.on("Issue Movement", {
    empleado: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; 
        if (row.empleado) {
            frappe.db.get_value("Employee", row.empleado, ["first_name", "last_name", "department"])
            .then(r => {
                if (r && r.message) {
                    let { first_name, last_name, department } = r.message;

                    // Set department
                    frappe.model.set_value(cdt, cdn, "departamento", department);

                    // Set full name in "empleado_name" field
                    frappe.model.set_value(cdt, cdn, "empleado_name", `${first_name || ''} ${last_name || ''}`.trim());
                }
            });
        }
    }



});

