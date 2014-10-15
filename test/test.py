import sys
sys.path.append('..')
from WooCommerceClient import WooCommerceClient
import pprint

wc_client = WooCommerceClient('ck_5e5692af317c09ca4581be6bc5596714', 'cs_3115cf0868e4ae29117257e13cec6248', 'http://wpdev/')
pprint.pprint(wc_client.get_products())