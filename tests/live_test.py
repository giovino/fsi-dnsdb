from dnsdb import Dnsdb
from dnsdb.dnsdb import utils

api_key = ''

dnsdb = Dnsdb(api_key)

result = dnsdb.search(name="fsi.io")

print(result.rescords[0])
