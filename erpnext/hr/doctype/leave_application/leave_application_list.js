// frappe.listview_settings['Leave Application'] = {
// 	add_fields: ["status", "from_date", "to_date","leave_type", "employee", "employee_name", "total_leave_days"],
// 	filters:[["status","!=", "Rejected"]],
// 	get_indicator: function(doc) {
// 		return [__(doc.status),frappe.utils.guess_colour(doc.status),
// 			"status,=," + doc.status];
// 	}
// 	}
frappe.listview_settings['Leave Application'] = {
	colwidths: {"employee_name": 1,"leave_type": 1,"status": 1,"from_date": 1,"employee_name": 1},
	add_fields: ["status", "from_date", "to_date","leave_type", "employee_name"],
	filters:[["status","!=", "Rejected"]],
	get_indicator: function(doc) {
		return [__(doc.status),frappe.utils.guess_colour(doc.status),
			"status,=," + doc.status];
	},
	onload: function (listview) {
		var arr=[]
		frappe.route_options = {
			
		};

		frappe.call({
			method:"frappe.client.get_list",
			args:{
				doctype:"User Notification",		
				filters: {
					"target_doctype": 'Leave Application',
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
}
