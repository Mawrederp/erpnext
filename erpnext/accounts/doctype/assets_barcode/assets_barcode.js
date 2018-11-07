// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assets Barcode', {
	refresh: function(frm) {

	},
	get_assets:function(frm){
		// frappe.get_list("Asset",{"asset_category":frm.doc.asset_category})
		// frm.set_value("assets_barcode_details",[]);
	}
});

frappe.ui.form.on("Assets Barcode Details", "asset_name", function(frm, doctype, name) {
	console.log("Generate barcode")
	console.log(frm.doc.name)
	console.log(doctype)
	console.log(name)
	let asset_barcode_details = frappe.get_doc(doctype,name);
	let asset_name = asset_barcode_details.asset_name;
	console.log(asset_name)
	let asset = frappe.get_doc("Asset",asset_name);
	console.log(asset)
	frappe.call({
		method:"frappe.client.get_value",
		args: {
			doctype:"Asset",
			filters: {
				name:asset_name
			},
			fieldname:["barcode_img", "name"]
		}, 
		callback: function(r) { 
			console.log(r);
			if(r.message){
				frappe.model.set_value(doctype,name,"barcode_img",r.message.barcode_img)
				frm.save()

			}
		}
	})
	
})
