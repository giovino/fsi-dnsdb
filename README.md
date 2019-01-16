# dnsdb

Python client for Farsight Security's [DNSDB API](https://api.dnsdb.info/).

## Features

 * supports all capabilities of [DNSDB API](https://api.dnsdb.info/)
 * sorting of results by last_seen
 * convert epoch to ISO 8601
 * normalize results with regard sensor or zone observation
 * DNSDB API Error codes returned in JSON data structure
 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dnsdb.

```bash
pip install dnsdb
```

## Usage

```python
from dnsdb import Dnsdb

api_key="12345"
dnsdb = Dnsdb(api_key)

results = dnsdb.search(name="fsi.io")
results = dnsdb.search(name="mail.fsi.io", inverse=True)
results = dnsdb.search(ip="104.244.14.108")
results = dnsdb.search(ip="104.244.14.0/24")
results = dnsdb.search(ip="2620:11c:f008::108")
results = dnsdb.search(hexadecimal="36757a35")
quota = dnsdb.quota()
```

## Advanced Usage

```python
from dnsdb import Dnsdb

api_key="12345"
dnsdb = Dnsdb(api_key)

results = dnsdb.search(name="fsi.io", type="A")
results = dnsdb.search(name="farsightsecurity.com", bailiwick="com.")
results = dnsdb.search(name="fsi.io", wildcard_left=True)
results = dnsdb.search(name="fsi", wildcard_right=True)
results = dnsdb.search(name="fsi.io", sort=False)
results = dnsdb.search(name="fsi.io", remote_limit=150000, return_limit=1000)
results = dnsdb.search(name="fsi.io", time_last_after=1514764800)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
