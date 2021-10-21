import frappe
import requests
import json
from frappe.utils import nowdate

def validate_and_get_project():
	support_settings = frappe.get_single("Support Settings")
	support_token = support_settings.support_token
	server_api_key = support_settings.server_api_key
	server_api_secret = support_settings.get_password('server_api_secret')

	if not server_api_key or not server_api_secret:
		frappe.throw("Please update API key and Secret from support settings")
	
	url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project?fields=["name","support_token","support_start_date","support_end_date"]&filters={"support_token": "' +support_token+ '"}'
	headers = {'Authorization':'token ' + server_api_key + ':' +  server_api_secret }


	r = requests.request("GET", url, headers=headers)
	response = r.json()
	
	client_support_token_on_server =  response['data'][0]['support_token']
	support_end_date = response['data'][0]['support_end_date']
	client_support_token = frappe.db.get_single_value('Support Settings','support_token')

	if client_support_token != client_support_token_on_server or  nowdate() > support_end_date:
		frappe.throw("Your support is expired. Please update support token to continue...")

	return response['data'][0]['name']

def update_client_key_secret(api_key,api_secret):

	project_name =  validate_and_get_project()
	
	put_url = 'http://8848digital-staging.8848digitalerp.com/api/resource/Project/'+project_name
	
	data = {'client_api_key': api_key, 'client_api_secret': api_secret}
	try:
		r = requests.request("PUT", put_url, headers=headers, data = json.dumps(data))
	except Exception as e:
		frappe.throw(str(e))


		
@frappe.whitelist(allow_guest=True)
def get_credential():
	support_settings = frappe.get_single("Support Settings")
	support_token = support_settings.support_token
	server_api_key = support_settings.server_api_key
	server_api_secret = support_settings.get_password('server_api_secret')

	return support_token, server_api_key, server_api_secret
