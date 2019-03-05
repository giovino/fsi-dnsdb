from dnsdb import Dnsdb
from dnsdb.dnsdb import utils

api_key = ''

dnsdb = Dnsdb(api_key)

result = dnsdb.search(name="fsi.io")

utils.debug(result.records, limit=2)
