# Copyright (c) 2021, Nirali Satapara and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils import get_url, nowdate
from frappe.utils.data import get_absolute_url

class SupportTicket(Document):
	def validate(self):
		if self.is_new():
			project = project_verification()
			support_ticket_reference = get_url()+get_absolute_url(self.doctype,self.name)
			url = "http://8848digital-staging.8848digitalerp.com/api/resource/Issue"
			headers = {'Authorization': 'token ee8e4f8f1330cba:68b959a1a3dc7c3'}
			data = {'subject':self.subject,'description':self.description,'project':project,'support_ticket_reference':support_ticket_reference}
			
			r = requests.request("POST", url, headers=headers, data=json.dumps(data))
			response = r.json()
			self.digital_support_id = response['data']['name']

def project_verification():
	project_url = get_url()

	url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project?fields=["name","support_token","support_start_date","support_end_date"]&filters={"project_url": "' +project_url+ '"}'
	headers = {'Authorization': 'token ee8e4f8f1330cba:68b959a1a3dc7c3'}

	r = requests.request("GET", url, headers=headers)
	response = r.json()
	
	server_support_token =  response['data'][0]['support_token']
	support_end_date = response['data'][0]['support_end_date']
	client_support_token = frappe.db.get_single_value('Support Settings','support_token')
	
	if client_support_token != server_support_token and nowdate() > support_end_date:
		frappe.throw("Your support is expired. Please update support token to continue...")
	return response['data'][0]['name']