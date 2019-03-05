frappe.listview_settings['Overtime Request'] = {
	onload: function (listview) {
		var arr=[]
		frappe.call({
			method:"frappe.client.get_list",
			args:{
				doctype:"User Notification",		
				filters: {
					"target_doctype": 'Overtime Request',
					"status": 'Active',
					"user": frappe.user.name
				},
				fields: "target_docname",
			},
			callback: function(r) {
				for(var i=0;i<r.message.length;i++){
					arr.push(r.message[i].target_docname)
				}
				frappe.route_options = {
					"name": ["in", arr]
				};				
			}
		});

	}
};
