frappe.ui.form.on('Issue', {
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
            frappe.db.get_value("Employee", row.empleado, "department")
                .then(r => {
                    if (r && r.message) {
                        let department = r.message.department;
                        frappe.model.set_value(cdt, cdn, "departamento", department);
                    }
                });
        }
    }



});

