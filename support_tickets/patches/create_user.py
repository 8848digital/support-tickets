import frappe
from frappe.utils import get_url
from support_tickets.api import update_client_key_secret

def execute():
	if not frappe.db.exists("Role","Support API"):
		role = frappe.new_doc("Role")
		role.role_name = "Support API"
		role.save()

	user = frappe.new_doc("User")
	user.email = "test@ascratech.com"
	user.first_name = "Support API"
	user.send_welcome_email = 0
	user.append("roles",{
		'role': "Support API"
	})
	user.save(ignore_permissions=True)
	api_secret = frappe.generate_hash(length=15)
	# if api key is not set generate api key
	if not user.api_key:
		api_key = frappe.generate_hash(length=15)
		user.api_key = api_key
	user.api_secret = api_secret
	user.save(ignore_permissions=True)

	update_client_key_secret(user.api_key,user.api_secret)
	
	if not frappe.db.exists("Role",{'parent':'Support Ticket','role':"Support API"}):
		perm_doc = frappe.new_doc("Custom DocPerm")
		perm_doc.parent = "Support Ticket"
		perm_doc.role = "Support API"
		perm_doc.select = 1
		perm_doc.read = 1
		perm_doc.write = 1
		perm_doc.create = 1
		perm_doc.save(ignore_permissions=True)