// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

cur_frm.add_fetch('employee', 'department', 'department');

frappe.ui.form.on('Correspondence Request', {
	refresh: function(frm) {

	}
});
