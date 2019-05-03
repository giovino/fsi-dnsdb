# dnsdb

Python client for Farsight Security's [DNSDB API](https://api.dnsdb.info/).

## Features

 * supports all capabilities of [DNSDB API](https://api.dnsdb.info/)
 * sorting of results by last_seen
 * convert epoch to ISO 8601
 * normalize results with regard sensor or zone observation
 * supports the caching of DNSDB API results
 * returns an object with the following attributes:
    * records
    * status code
    * error
    * quota
    * cache
 * CLI named `dnsdb`

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [dnsdb](https://pypi.org/project/dnsdb/).

```bash
pip install dnsdb
```

## Usage

### Setup
```text
>>> from dnsdb import Dnsdb

>>> api_key="12345"
>>> dnsdb = Dnsdb(api_key)
```

### Example 1
```text
>>> result = dnsdb.search(name="www.example.com")

>>> pprint(result.status_code)
200

>>> pprint(result.error)
None

>>> pprint(result.records[0])
{'bailiwick': 'example.com.',
 'count': 4213726,
 'rdata': ['93.184.216.34'],
 'rrname': 'www.example.com.',
 'rrtype': 'A',
 'source': 'sensor',
 'time_first': '2014-12-10T00:19:18Z',
 'time_last': '2019-03-05T14:37:31Z'}
 
>>> pprint(result.quota)
{'expires': None,
 'limit': '1000000',
 'remaining': '999970',
 'reset': '1551830400',
 'results_max': None}
```

### Example 2
```text
>>> result = dnsdb.search(name="hello.example.com")

>>> pprint(result.status_code)
404

>>> pprint(result.error)
{'code': 404, 'message': 'Error: no results found for query.'}

>>> pprint(result.records)
None

>>> pprint(result.quota)
{'expires': None,
 'limit': '1000000',
 'remaining': '999969',
 'reset': '1551830400',
 'results_max': None}
```

## More Usage
```text
from dnsdb import Dnsdb

api_key="12345"
dnsdb = Dnsdb(api_key)
dnsdb = Dnsdb(api_key, cache=True)
dnsdb = Dnsdb(api_key, cache=True, cache_timeout=900)
dnsdb = Dnsdb(api_key, cache=True, cache_location="/tmp/dnsdb-cache")

result = dnsdb.search(name="fsi.io")
result = dnsdb.search(name="mail.fsi.io", inverse=True)
result = dnsdb.search(ip="104.244.14.108")
result = dnsdb.search(ip="104.244.14.0/24")
result = dnsdb.search(ip="2620:11c:f008::108")
result = dnsdb.search(hexadecimal="36757a35")
result = dnsdb.search(name="fsi.io", type="A")
result = dnsdb.search(name="farsightsecurity.com", bailiwick="com.")
result = dnsdb.search(name="fsi.io", wildcard_left=True)
result = dnsdb.search(name="fsi", wildcard_right=True)
result = dnsdb.search(name="fsi.io", sort=False)
result = dnsdb.search(name="fsi.io", remote_limit=150000, return_limit=1000)
result = dnsdb.search(name="fsi.io", time_last_after="2019-01-01")
result = dnsdb.search(name="fsi.io", time_last_after="2019-01-01T00:00:00Z")
result = dnsdb.search(name="fsi.io", epoch=True, time_last_after=1546300800)
result = dnsdb.search(name="fsi.io", epoch=True)
result = dnsdb.quota()
```

## CLI

The `dnsdb` module includes CLI client

## Help

```test
$ dnsdb -h
usage: dnsdb [-h] (-n NAME | -i IP | --hex HEXADECIMAL) [-t TYPE]
             [-b BAILIWICK] [-r] [--wildcard-left] [--wildcard-right] [--sort]
             [--epoch] [-f {csv,json,jsonp}] [--return-limit RETURN_LIMIT]
             [--remote-limit REMOTE_LIMIT] [--first-before TIME_FIRST_BEFORE]
             [--first-after TIME_FIRST_AFTER] [--last-before TIME_LAST_BEFORE]
             [--last_after TIME_LAST_AFTER] [--cache]
             [--cache-location CACHE_LOCATION] [--cache-timeout CACHE_TIMEOUT]
             [--apikey API_KEY] [--server SERVER] [-v] [-c CONFIG] [--version]

CLI client for DNSDB

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  fully qualified domain mame
  -i IP, --ip IP        IPv4 or IPv6 address, CIDR notation is valid
  --hex HEXADECIMAL     hexadecimal digits specifying a raw octet string
  -t TYPE, --type TYPE  dns resource record types (ANY, A, MX, SIG, etc)
  -b BAILIWICK, --bailiwick BAILIWICK
                        a label in a fqdn, not valid for inverse queries
  -r, --inverse         search for names resolving to names (e.g. MX, NS,
                        CNAME, etc)
  --wildcard-left       wildcard search to the left of a dot in a domain name
  --wildcard-right      wildcard search to the right of a dot in a domain name
  --sort                sort results by time last
  --epoch               return timestamps in epoch
  -f {csv,json,jsonp}, --format {csv,json,jsonp}
                        output formats
  --return-limit RETURN_LIMIT
                        number of client side results returned
  --remote-limit REMOTE_LIMIT
                        number of server side results returned
  --first-before TIME_FIRST_BEFORE
                        server side filter for time first before
  --first-after TIME_FIRST_AFTER
                        server side filter for time first after
  --last-before TIME_LAST_BEFORE
                        server side filter for time last before
  --last_after TIME_LAST_AFTER
                        server side filter for time last after
  --cache               Use cached results
  --cache-location CACHE_LOCATION
                        Path to cache
  --cache-timeout CACHE_TIMEOUT
                        Timeout in seconds
  --apikey API_KEY      DNSDB API key
  --server SERVER       Server URL
  -v, --verbose         Set the verbosity level
  -c CONFIG, --config CONFIG
                        Path to config file
  --version             show program's version number and exit

Time format options: yyyy (2016), yyyy-mm (2016-01), yyyy-mm-dd (2016-01-01),
yyyymmdd (20160101), yyyymmddThh (20160101T12), yyyy-mm-ddThh:mm:ss-hh:mm
(2016-01-01T00:00:00-00:00)
```

### Configuration file

### Minimal
```text
$ vim ~/.dnsdb.ini

[api.dnsdb.info]
api_key=12345
```

### Full

```text
$ vim ~/.dnsdb.ini

[api.dnsdb.info]
api_key=12345
server=https://api.dnsdb.info
cache=True
cache_location=/tmp/dnsdb-cache
cache_timeout=900
```

### Usage

```text
$ dnsdb -n www.fsi.io
$ dnsdb -i 104.244.14.108 -f csv
```

## Contributing
Pull requests are welcome; for major changes, please open an issue first to discuss what you would like to change.

Please make sure to create and update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
