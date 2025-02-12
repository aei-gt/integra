// Copyright (c) 2025, AEI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Overtime Request", {
    till_time: function(frm) {
        if (frm.doc.from_time && frm.doc.till_time) {
            let start = moment(frm.doc.from_time, "HH:mm:ss");
            let end = moment(frm.doc.till_time, "HH:mm:ss");
            let duration = moment.duration(end.diff(start));
            let formatted_time = moment.utc(duration.asMilliseconds()).format("HH:mm:ss");
            frm.set_value('overtime_hours', formatted_time);
        }
    },
});
