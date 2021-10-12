from __future__ import unicode_literals
import frappe
import requests
import json
from frappe.utils import get_url
from frappe.utils import nowdate

def execute():
	project_url = get_url()
	url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project?fields=["support_token"]&filters={"project_url": "' +project_url+ '"}'

	headers = {'Authorization': 'token ee8e4f8f1330cba:68b959a1a3dc7c3'}

	r = requests.request("GET", url, headers=headers)
	response = r.json()
	server_side_support_token =  response['data'][0]['support_token']

	doc = frappe.get_doc("Support Settings")
	doc.support_token = server_side_support_token
	doc.save(ignore_permissions=True)
	frappe.db.commit()