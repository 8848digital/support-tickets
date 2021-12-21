# Copyright (c) 2021, Nirali Satapara and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from support_tickets.api import validate_and_get_project
from frappe.utils import get_url, nowdate
from frappe.utils.data import get_absolute_url

class SupportTicket(Document):
	def validate(self):
		if self.is_new():
			project = validate_and_get_project()

			support_settings = frappe.get_single("Support Settings")
			server_api_key = support_settings.server_api_key
			server_api_secret = support_settings.get_password('server_api_secret')
			headers = {'Authorization':'token ' + server_api_key + ':' +  server_api_secret,'Content-Type': 'application/json',
		'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image=' }

			self.create_issue(headers,project)

		#self.update_issue()

	@frappe.whitelist()
	def update_issue(self):
		project = validate_and_get_project()

		support_settings = frappe.get_single("Support Settings")
		server_api_key = support_settings.server_api_key
		server_api_secret = support_settings.get_password('server_api_secret')
		server_url = support_settings.server_url

		headers = {'Authorization':'token ' + server_api_key + ':' +  server_api_secret }
	
		if self.is_new():
			self.create_issue(headers,project)
		
		if self.partner_support_id and self.updates:
			url = server_url + '/api/resource/Issue/'+self.partner_support_id
		
			r = requests.request("GET", url, headers=headers)
			response = r.json()
			issue_updates = response['message']['issue_updates']
			support_ticket_update =[]
			if not issue_updates:
				for d in self.updates:
					if not d.issue_update_id:
						support_ticket_update.append({"description": d.description,"support_ticket_update_id": d.name})
			else:
				support_ticket_reference_list = [d.get("support_ticket_update_id") for d in issue_updates]
				for d in self.updates:
					if d.name not in support_ticket_reference_list and not d.issue_update_id:
						support_ticket_update.append({"description": d.description,"support_ticket_update_id": d.name})

			data = {"issue_updates": issue_updates + support_ticket_update}
			try:
				r_put = requests.request("PUT", url, headers=headers, data = json.dumps(data))
				response_put = r_put.json()
				if r_put.status_code == 200:
					frappe.msgprint(f"Issue {self.partner_support_id} updated.")
			except Exception as e:
				frappe.throw(str(e))

	def create_issue(self, headers, project):
		support_ticket_reference = get_url() + get_absolute_url(self.doctype,self.name)
		server_url = frappe.db.get_single_value('Support Settings','server_url')

		url = server_url + "/api/resource/Issue"
		data = {'subject':self.subject,'description':self.description,'project':project,'support_ticket_reference':support_ticket_reference}
		try:
			r = requests.request("POST", url, headers=headers, data=json.dumps(data))
		except Exception as e:
			frappe.throw(str(e))
		response = r.json()
		self.partner_support_id = response['message']['name']