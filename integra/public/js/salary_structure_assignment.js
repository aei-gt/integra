frappe.ui.form.on("Salary Structure Assignment", {
    base: function(frm, dt, dn) {
        var base_value = frm.doc.base;
        var reserva_b14 = base_value * 0.08333;
        var reserva_aguinaldo = base_value * 0.08333;
        var reserva_liquidacion = base_value  * 0.08333;
        var reserva_vacaciones = base_value  * 0.04167;
        var reserva_cuota_patronal = base_value  * 0.1267;
        
        frappe.model.set_value(dt, dn , 'custom_reserva_b14', reserva_b14);
        frappe.model.set_value(dt, dn, 'custom_reserva_aguinaldo', reserva_aguinaldo);
        frappe.model.set_value(dt, dn , 'custom_reserva_liquidacion', reserva_liquidacion);
        frappe.model.set_value(dt, dn, 'custom_reserva_vacaciones', reserva_vacaciones);
        frappe.model.set_value(dt, dn , 'custom_reserva_cuota_patronal', reserva_cuota_patronal);
        
    }
});