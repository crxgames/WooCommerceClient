#
# WooCommerceClient.py
#
# A WooCommerce 2.1+ API client
# Copyright (C) 2014 Cody Mays
# License: MIT License (http://opensource.org/licenses/MIT)
# https://github.com/crxgames
#
from urllib2 import HTTPError, Request, urlopen
import time
import json
import math
import hashlib
import urllib
import hmac
import hashlib
import random

class HTTP401Error(Exception):
	pass

class HTTP403Error(Exception):
	pass

class HTTP404Error(Exception):
	pass

class WooAuthError(Exception):
	pass

class WooCommerceClient(object):
	def __init__(self, consumer_key, consumer_secret, store_url):
		self.ConsumerKey = consumer_key
		self.ConsumerSecret = consumer_secret

		# Make sure there is a trailing slash
		if store_url[-1] != '/':
			store_url += '/'

		self.StoreURL = store_url + 'wc-api/v2/'

	# get_index
	# This hits the main api route, no auth needed
	def get_index(self):
		return self._do_request('')

##########################
#
# COUPON methods
#
##########################
	def get_coupons(self):
		return self._do_request('coupons');

	def get_coupon(self, id):
		return self._do_request('coupons/' + str(id))

	def get_coupon_from_code(self, code):
		return self._do_request('coupons/code/' + str(code))

	def get_coupons_count(self):
		return self._do_request('coupons/count')

##########################
#
# ORDER methods
#
##########################
	def get_orders(self, params = {}):
		return self._do_request('orders', params)

	def get_order(self, id):
		return self._do_request('order/' + str(id))

	def get_orders_count(self):
		return self._do_request('orders/count')

	def get_order_notes(self, id):
		return self._do_request('orders/' + str(id) + '/notes')

	def get_order_note(self, id, note_id):
		return self._do_request('orders/' + str(id) + '/notes/' + str(note_id))

	def get_order_statuses(self):
		return self._do_request('orders/statuses')

	def get_order_refunds(self, id):
		return self._do_request('orders/' + str(id) + '/refunds')

	def get_order_refund(self, id, refund_id):
		return self._do_request('orders/' + str(id) + '/refunds/' + str(refund_id))

	def update_order(self, id, data):
		return self._do_request('orders/' + str(id), data, 'POST')

	def delete_order(self, id):
		return self._do_request('orders/' + str(id), {}, 'DELETE')

##########################
#
# CUSTOMER methods
#
##########################
	def get_customers(self, params = {}):
		return self._do_request('customers', params);

	def get_customer(self, id):
		return self._do_request('customers/' + str(id))

	def get_customer_from_email(self, email):
		return self._do_request('customers/email' + email)

	def get_customers_count(self):
		return self._do_request('customers/count')

	def get_customer_orders(self, id):
		return self._do_request('customers/' + str(id) + '/orders')

	def get_customer_downloads(self, id):
		return self._do_request('customers/' + str(id) + '/downloads')

##########################
#
# PRODUCT methods
#
##########################
	def get_products(self, params = {}):
		return self._do_request('products', params)

	def get_product(self, id):
		return self._do_request('products/' + str(id))

	def get_products_count(self):
		return self._do_request('products/count')

	def get_product_reviews(self, id):
		return self._do_request('products/' + str(id) + '/reviews')

	def get_products_categories(self):
		return self._do_request('products/categories')

	def get_product_category(self, id):
		return self._do_request('product/categories/' + str(id))

###########################
#
# REPORT methods
#
###########################
	def get_reports(self, params = {}):
		return self._do_request('reports', params)

	def get_report_sales(self, params = {}):
		return self._do_request('reports/sales', params)

	def get_report_top_sellers(self, params = {}):
		return self._do_request('reports/top_sellers', params)

##########################
#
# WEBHOOK methods
#
##########################
	def get_webhooks(self, params = {}):
		return self._do_request('webhooks', params)

	def get_webhook(self, id):
		return self._do_request('webhooks/' + str(id))

	def get_webhooks_count(self):
		return self._do_request('webhooks/count')

	def get_webhook_deliveries(self, id):
		return self._do_request('webhooks/' + str(id) + '/deliveries')

	def get_webhook_delivery(self, id, delivery_id):
		return self._do_request('webhooks/' + str(id) + '/deliveries/' + str(delivery_id))

##########################
#
# CUSTOM method
#
##########################
	def endpoint_call(self, endpoint, params = {}, method = 'GET'):
		return self._do_request(endpoint, params, method)


##########################
#
# Utility methods
#
##########################
	def _do_request(self, endpoint, params = {}, method = 'GET'):
		parameters = params
		parameter_string = ''

		# TODO: If wanting to support HTTP Auth, do it here, skip OAuth stuff

		parameters['oauth_consumer_key'] = self.ConsumerKey
		parameters['oauth_timestamp'] = int(time.time())
		parameters['oauth_nonce'] = ''.join([str(random.randint(0, 9)) for i in range(8)])
		parameters['oauth_signature_method'] = 'HMAC-SHA256'
		parameters['oauth_signature'] = self.generate_oauth_sig(parameters, method, endpoint)

		if len(parameters) > 0:
			parameter_string = '?' + urllib.urlencode(parameters)

		if method == "POST":
			print('POST METHOD NOT IMPLEMENTED YET')
		elif method == "DELETE":
			print('DELETE METHOD NOT IMPLEMENTED YET')
		else: # GET
			try:
				request = Request(self.StoreURL + endpoint + parameter_string)
				response_body = urlopen(request).read()
				return json.loads(response_body)

			except HTTPError as e:
				self.handle_http_error(e)

	def generate_oauth_sig(self, params, method, endpoint):
		parameters = params

		if 'oauth_signature' in parameters.keys():
			del parameters['oauth_signature']

		base_url = urllib.quote(self.StoreURL + endpoint).replace('+','%20').replace('/', '%2F')

		# Build out a normalized (for OAuth spec) list of parameters that are sorted in byte-order
		parameters = self.normalize_parameters(parameters)
		parameters = [(k, parameters[k]) for k in sorted(parameters.keys(), cmp=cmp)]

		# Build up query string with equal signs and %26's
		query_string = ''
		query_vals = []

		for name, value in parameters:
			query_vals.append(name + '%3D' + value)

		query_string = '%26'.join(query_vals).replace('%5B', '%255B').replace('%5D', '%255D')

		_hash = hmac.new(self.ConsumerSecret, method + '&' + base_url + '&' + query_string, hashlib.sha256).digest()
		signature = _hash.encode('base64').rstrip('\n') # random python thing to work around
		return str(signature)

	def normalize_parameters(self, parameters):
		norm_params = {}
		for k in parameters.iterkeys():
			key = None
			val = None

			try:
				key = urllib.unquote(k)
			except:
				pass

			try:
				val = urllib.unquote(str(parameters[k]))
			except:
				pass

			if not key:
				key = str(k)

			if not val:
				val = str(parameters[k])

			norm_params[urllib.quote(key)] = urllib.quote(val)

		return norm_params

	def handle_http_error(self, error):
		response = error.read()
		response_json = None

		# Try to break down the errors out of the API
		try:
			response_json = json.loads(response)
		except:
			pass

		if response_json and response_json['errors'][0]['code'] == 'woocommerce_api_authentication_error':
			raise WooAuthError(response_json['errors'][0]['message'])
			return

		if error.code == 404:
			raise HTTP404Error(response)
		elif error.code == 403:
			raise HTTP403Error(response)
		elif error.code == 401:
			raise HTTP401Error(response)
		else:
			raise Exception(response)
