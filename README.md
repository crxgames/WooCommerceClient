Python WooCommerce REST API Client
===================================

A Python wrapper for the WooCommerce 2.1+ REST API. This library currently supports all read-only methods and a handful
of write methods. Further development coming soon on all write access methods. As always, feel free to add, remove, customize, and 
make a pull request.

## Rockin out with WooCommerce and Python
You will first need to generate API credentials from the user profile page in Wordpress admin.

### Initialize the wrapper
```python
	from WooCommerceClient import WooCommerceClient
	import pprint

	wc_client = WooCommerceClient('ck_5e5692af317c09ca4581be6bc5596714', 'cs_3115cf0868e4ae29117257e13cec6248', 'http://wpdev/')
```

### Fetch the goods
```python
	pprint.pprint(wc_client.get_products())
```

**Methods return json.loads()'d responses, not raw JSON**

## Methods

### Index
- `get_index()`

### Coupon
- `get_coupons()`
- `get_coupon( id )`
- `get_coupon_from_code( coupon_code )`
- `get_coupons_count()`

### Order
- `get_orders()`
- `get_orders( { 'status' : 'completed' } )`
- `get_order( id )`
- `get_orders_count()`
- `get_order_notes( id )`
- `get_order_note( id, note_id )`
- `get_order_statuses()`
- `get_order_refunds( id )`
- `get_order_refund(id, refund_id)`
- `update_order( id, { 'status' : 'processing' } )`
- `delete_order( id )`

### Customer
- `get_customers()`
- `get_customers( { 'filter[created_at_min]' : '2013-12-01' } )`
- `get_customer( id )`
- `get_customer_from_email( email )`
- `get_customers_count()`
- `get_customer_orders( id )`
- `get_customer_downloads( id )`

### Product
- `get_products()`
- `get_products( { 'filter[created_at_min]' : '2013-12-01' } )`
- `get_product( id )`
- `get_products_count()`
- `get_product_reviews( id )`
- `get_product_categories()`
- `get_product_category( id )`

### Report
- `get_reports()`
- `get_report_sales( { 'filter[start_date]' : '2011-12-01', 'filter[end_date]' : '2011-12-29' } )`
- `get_report_top_sellers( { 'filter[limit]' = '10' } )`

### Webhook
- `get_webhooks()`
- `get_webhooks( { 'filter[status]' : 'active' })`
- `get_webhooks_count()`
- `get_webhook_deliveries( id )`
- `get_webhook_delivery( id, delivery_id )`

### Custom 
- `endpoint_call( endpoint, params = {} , method = 'GET' )`

## License

Copyright (c) 2014 - [Cody Mays](http://www.codymays.net/)
License: [MIT license](http://opensource.org/licenses/MIT)
