from __future__ import unicode_literals
import frappe
import requests
import json
from frappe.utils import get_url
from frappe.utils import nowdate

def execute():
	project_url = get_url()
	
	support_settings = frappe.get_single("Support Settings")
	server_api_key = support_settings.server_api_key
	server_api_secret = support_settings.get_password('server_api_secret')
	
	url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project?fields=["support_token"]&filters={"project_url": "' +project_url+ '"}'
	headers = {'Authorization':'token ' + server_api_key + ':' +  server_api_secret }
	
	try:
		r = requests.request("GET", url, headers=headers)
	except Exception as e:
		frappe.throw(str(e))
	response = r.json()
	support_token =  response['data'][0]['support_token']

	doc = frappe.get_doc("Support Settings")
	doc.support_token = support_token
	doc.save(ignore_permissions=True)
	frappe.db.commit()