from dnsdb import Dnsdb
from dnsdb.dnsdb import utils

api_key = ''

dnsdb = Dnsdb(api_key)

results = dnsdb.search(name="fsi.io")

utils.debug(results, limit=2)
