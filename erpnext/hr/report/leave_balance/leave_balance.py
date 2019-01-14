# encoding: utf-8
# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import formatdate, getdate, flt, add_days
from datetime import datetime
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_years, add_months, add_days, nowdate
from erpnext.hr.doctype.leave_application.leave_application import get_monthly_accumulated_leave
import datetime
# import operator
import re
from datetime import date
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
    comma_or, get_fullname, add_years, add_months, add_days, nowdate

from dateutil.relativedelta import relativedelta
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee



def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
	return [
		_("Employee ID") + ":Link/Employee:150",
		_("Employee Name") + "::150",
		_("Department") + "::150",
		_("Date of Joining") + ":Date:150",

		_("Annual Leave - اجازة اعتيادية(Yearly)") + "::200",
		_("Annual Leave - اجازة اعتيادية(Daily)") + "::200",
		_("Sick Leave - مرضية") + "::150",
		_("Emergency -اضطرارية") + "::150",
		_("Educational - تعليمية") + "::150"

		]



# def get_conditions(filters):
# 	conditions = ""

# 	if filters.get("asset_category"): conditions += " and asset_category= '{0}' ".format(filters.get("asset_category"))

# 	# if filters.get("employee"): conditions += " and employee = %(employee)s"

# 	# if filters.get("from_date"): conditions += " and date_of_joining>=%(from_date)s"
# 	# if filters.get("to_date"): conditions += " and date_of_joining<=%(to_date)s"

# 	return conditions


def get_data(filters):
	data =[]
	# conditions = get_conditions(filters)
	li_list=frappe.db.sql(""" select name,employee_name,department,date_of_joining from `tabEmployee` order by name asc""",as_dict=1)

	for emp in li_list:
		
		annual_leave=frappe.db.sql("select from_date from `tabLeave Allocation` where employee='{0}' and leave_type='Annual Leave - اجازة اعتيادية' order by creation desc limit 1".format(emp.name))
		if annual_leave:
			remain_annual = frappe.db.sql(""" select (select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Annual Leave - اجازة اعتيادية' and docstatus =1 order by creation desc limit 1 ) - ( select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Annual Leave - اجازة اعتيادية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' )""".format(emp.name,annual_leave[0][0],filters.get("date")))
			max_annual = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Annual Leave - اجازة اعتيادية' and docstatus =1 order by creation desc limit 1 """.format(emp.name))
			used_annual = frappe.db.sql(""" select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Annual Leave - اجازة اعتيادية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' """.format(emp.name,annual_leave[0][0],filters.get("date")))


		sick_leave=frappe.db.sql("select from_date from `tabLeave Allocation` where employee='{0}' and leave_type='Sick Leave - مرضية' order by creation desc limit 1".format(emp.name))
		if sick_leave:
			remain_sick = frappe.db.sql(""" select (select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Sick Leave - مرضية' and docstatus =1 order by creation desc limit 1 ) - ( select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Sick Leave - مرضية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' )""".format(emp.name,sick_leave[0][0],filters.get("date")))
			max_sick = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Sick Leave - مرضية' and docstatus =1 order by creation desc limit 1 """.format(emp.name))
			used_sick = frappe.db.sql(""" select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Sick Leave - مرضية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' """.format(emp.name,sick_leave[0][0],filters.get("date")))


		emergency_leave=frappe.db.sql("select from_date from `tabLeave Allocation` where employee='{0}' and leave_type='emergency -اضطرارية' order by creation desc limit 1".format(emp.name))
		if emergency_leave:
			remain_emergency = frappe.db.sql(""" select (select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'emergency -اضطرارية' and docstatus =1 order by creation desc limit 1 ) - ( select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='emergency -اضطرارية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' )""".format(emp.name,emergency_leave[0][0],filters.get("date")))
			max_emergency = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'emergency -اضطرارية' and docstatus =1 order by creation desc limit 1 """.format(emp.name))
			used_emergency = frappe.db.sql(""" select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='emergency -اضطرارية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' """.format(emp.name,emergency_leave[0][0],filters.get("date")))


		educational_leave=frappe.db.sql("select from_date from `tabLeave Allocation` where employee='{0}' and leave_type='Educational - تعليمية' order by creation desc limit 1".format(emp.name))
		if educational_leave:
			remain_educational = frappe.db.sql(""" select (select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Educational - تعليمية' and docstatus =1 order by creation desc limit 1 ) - ( select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Educational - تعليمية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' )""".format(emp.name,educational_leave[0][0],filters.get("date")))
			max_educational = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation` where employee='{0}' and leave_type = 'Educational - تعليمية' and docstatus =1 order by creation desc limit 1 """.format(emp.name))
			used_educational = frappe.db.sql(""" select SUM(total_leave_days) from `tabLeave Application` where employee='{0}' and leave_type='Educational - تعليمية' and docstatus=1 and from_date >= '{1}' and to_date <= '{2}' """.format(emp.name,educational_leave[0][0],filters.get("date")))

		try:
			if used_annual[0][0] and annual_leave[0][0]:
				annual_leave_balance = remain_annual[0][0]
			elif max_annual[0][0]:
				annual_leave_balance = max_annual[0][0]
		except:
			annual_leave_balance = 0


		try:
			if used_sick[0][0] and sick_leave[0][0]:
				sick_leave_balance = remain_sick[0][0]
			elif max_sick[0][0]:
				sick_leave_balance = max_sick[0][0]
		except:
			sick_leave_balance = 0



		try:
			if used_emergency[0][0] and emergency_leave[0][0]:
				emergency_leave_balance = remain_emergency[0][0]
			elif max_sick[0][0]:
				emergency_leave_balance = max_emergency[0][0]
		except:
			emergency_leave_balance = 0



		try:
			if used_educational[0][0] and educational_leave[0][0]:
				educational_leave_balance = remain_educational[0][0]
			elif max_sick[0][0]:
				educational_leave_balance = max_educational[0][0]
		except:
			educational_leave_balance = 0

			


		row = [
		emp.name,
		emp.employee_name,
		emp.department,
		emp.date_of_joining,

		annual_leave_balance,
		get_monthly_accumulated_leave(filters.get("date"),filters.get("date"),'Annual Leave - اجازة اعتيادية',emp.name),
		sick_leave_balance,
		emergency_leave_balance,
		educational_leave_balance,
		
    	]
		data.append(row)
		

	return data




@frappe.whitelist()
def get_monthly_accumulated_leave(from_date, to_date, leave_type, employee, for_report=True):
    allocation_records = get_leave_allocation_records(from_date, employee, leave_type)
    if allocation_records:
        applied_days = get_approved_leaves_for_period(employee, leave_type, allocation_records[employee][leave_type].from_date, to_date)


        if for_report:
            total_leave_days=0
        else:
            total_leave_days = get_number_of_leave_days(employee, leave_type, from_date, to_date)           

        date_dif = date_diff(to_date, allocation_records[employee][leave_type].from_date)
        balance = ""
        if leave_type == "Annual Leave - اجازة اعتيادية":
            # al_from_date_month = getdate(allocation_records[employee][leave_type].from_date).month
            # al_to_date_month = getdate(allocation_records[employee][leave_type].to_date).month
            # frappe.throw(str(date_dif))

            prev_year_date = frappe.utils.data.add_years(from_date, -1)
            prev_year_allocation_records = get_leave_allocation_records(prev_year_date, employee, "Annual Leave - اجازة اعتيادية")
            if prev_year_allocation_records:
                from_date = prev_year_allocation_records[employee]["Annual Leave - اجازة اعتيادية"].from_date
                to_date = prev_year_allocation_records[employee]["Annual Leave - اجازة اعتيادية"].to_date
                prev_year_total_leaves_allocated = prev_year_allocation_records[employee]["Annual Leave - اجازة اعتيادية"].total_leaves_allocated
                prev_year_applied_days = get_approved_leaves_for_period(employee, "Annual Leave - اجازة اعتيادية", from_date, to_date)
                prev_year_remain_balance = prev_year_total_leaves_allocated - prev_year_applied_days
                # if prev_year_remain_balance >= 11:
                #     prev_year_remain_balance = 11
            else:
                prev_year_remain_balance = 0
            # frappe.throw(str((date_dif) * (22/360)))

            period_balance = ((date_dif) * (0.061111111)) + prev_year_remain_balance
            # if period_balance > 33:
            #   period_balance=33

            balance = period_balance - applied_days - total_leave_days
            # getdate(to_date).month

        elif leave_type == "Compensatory off - تعويضية":
            al_from_date = getdate(allocation_records[employee][leave_type].from_date)
            first_of_month = 1 if al_from_date.day == 1 else 0
            
            if al_from_date.year == getdate(to_date).year:
                period_balance = (getdate(to_date).month - al_from_date.month + first_of_month)*10
                balance = period_balance - applied_days - total_leave_days

            elif al_from_date.year < getdate(to_date).year:
                period_balance = (12 - al_from_date.month + getdate(to_date).month + first_of_month)*10
                balance = period_balance - applied_days - total_leave_days
            else:
                frappe.throw(_("Invalid Dates"))

        return str(round(balance,2))





def get_leave_allocation_records(date, employee=None, leave_type=None):
    conditions = (" and employee='%s'" % employee) if employee else ""
    conditions += (" and leave_type='%s'" % leave_type) if leave_type else ""
    leave_allocation_records = frappe.db.sql("""
        select employee, leave_type, total_leaves_allocated, from_date, to_date
        from `tabLeave Allocation`
        where %s between from_date and to_date and docstatus=1 {0}""".format(conditions), (date), as_dict=1)

    allocated_leaves = frappe._dict()
    for d in leave_allocation_records:
        allocated_leaves.setdefault(d.employee, frappe._dict()).setdefault(d.leave_type, frappe._dict({
            "from_date": d.from_date,
            "to_date": d.to_date,
            "total_leaves_allocated": d.total_leaves_allocated
        }))

    return allocated_leaves






def get_approved_leaves_for_period(employee, leave_type, from_date, to_date):
    #"
    leave_applications = frappe.db.sql("""
        select name,employee, leave_type, from_date, to_date, total_leave_days
        from `tabLeave Application`
        where employee=%(employee)s and leave_type=%(leave_type)s
            and docstatus=1 and status='Approved'
            and (from_date between %(from_date)s and %(to_date)s
                or to_date between %(from_date)s and %(to_date)s
                or (from_date < %(from_date)s and to_date > %(to_date)s))
    """, {
        "from_date": from_date,
        "to_date": to_date,
        "employee": employee,
        "leave_type": leave_type
    }, as_dict=1)

    leave_days = 0
    for leave_app in leave_applications:
        leave_days += leave_app.total_leave_days
        # if leave_app.from_date >= getdate(from_date) and leave_app.to_date <= getdate(to_date):
        #     return_from_leave = frappe.db.sql(""" select name,from_date,return_date from `tabReturn From Leave Statement` where leave_application='{0}' and docstatus=1""".format(leave_app.name), as_dict=1)
        #     if return_from_leave and len(return_from_leave) > 0:
        #         leave_days += date_diff(return_from_leave[0].return_date,return_from_leave[0].from_date) + 1
        #     else:
        #         leave_days += leave_app.total_leave_days
        # else:
        #     if leave_app.from_date < getdate(from_date):
        #         leave_app.from_date = from_date
        #     if leave_app.to_date > getdate(to_date):
        #         leave_app.to_date = to_date
        #     return_from_leave = frappe.db.sql(""" select name,from_date,return_date from `tabReturn From Leave Statement` where leave_application='{0}' and docstatus=1""".format(leave_app.name), as_dict=1)
        #     if return_from_leave and len(return_from_leave) > 0:
        #         leave_days += date_diff(return_from_leave[0].return_date,return_from_leave[0].from_date) + 1
        #     else:
        #         leave_days += get_number_of_leave_days(employee, leave_type,
        #             leave_app.from_date, leave_app.to_date)

    return leave_days




@frappe.whitelist()
def get_number_of_leave_days(employee, leave_type, from_date, to_date, half_day=None):
    if half_day==1:
        return 
    number_of_days = date_diff(to_date, from_date) + 1
    if not frappe.db.get_value("Leave Type", leave_type, "include_holiday"):
        number_of_days = flt(number_of_days) - flt(get_holidays(employee, from_date, to_date))

    return number_of_days




@frappe.whitelist()
def get_holidays(employee, from_date, to_date):
    '''get holidays between two dates for the given employee'''
    holiday_list = get_holiday_list_for_employee(employee)

    holidays = frappe.db.sql("""select count(distinct holiday_date) from `tabHoliday` h1, `tabHoliday List` h2
        where h1.parent = h2.name and h1.holiday_date between %s and %s
        and h2.name = %s""", (from_date, to_date, holiday_list))[0][0]

    return holidays