# Copyright (c) 2021, Nirali Satapara and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils import get_url

class SupportTicket(Document):
	def validate(self):
		if self.is_new():
			verify_token()

			url = "http://8848digital-staging.8848digitalerp.com/api/resource/Issue"

			data = {'subject':self.subject,'description':self.description}
			headers = {
				'Authorization': 'token ee8e4f8f1330cba:68b959a1a3dc7c3',
				'Content-Type': 'text/plain',
				'Cookie': 'full_name=Guest; sid=Guest; system_user=no; user_id=Guest; user_image='
			}
			
			r = requests.request("POST", url, headers=headers, data=json.dumps(data))
			response = r.json()
			self.digital_support_id = response['data']['name']

def verify_token():
	project_url = get_url()
	url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project?fields=["support_token"]&filters={"project_url": "' +project_url+ '"}'

	headers = {'Authorization': 'token ee8e4f8f1330cba:68b959a1a3dc7c3'}

	r = requests.request("GET", url, headers=headers)
	response = r.json()
	server_support_token =  response['data'][0]['support_token']
	client_support_token = frappe.db.get_single_value('Support Settings','support_token')
	
	if client_support_token != server_support_token:
		frappe.throw("Your support is expired. Please update support token to continue...")

		
