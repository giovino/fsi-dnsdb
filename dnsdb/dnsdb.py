# -*- coding: utf-8 -*-
""" Python client for Farsight Security's DNSDB API

Farsight Security DNSDB is a database that stores and indexes both the
passive DNS data available via Farsight Security's Security Information
Exchange as well as the authoritative DNS data that various zone operators
make available. DNSDB makes it easy to search for individual DNS RRsets and
provides additional metadata for search results such as first seen and last
seen timestamps as well as the DNS bailiwick associated with an RRset.
DNSDB also has the ability to perform inverse or rdata searches

Farsight DNSDB API Documentation
https://api.dnsdb.info/

INITIALIZE EXAMPLE::

from dnsdb import Dnsdb

api_key="12345"
dnsdb = Dnsdb(api_key)

SIMPLE USAGE EXAMPLES:::

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
result = dnsdb.search(name="fsi.io", time_last_after=1514764800)
result = dnsdb.search(name="fsi.io", epoch=True)
result = dnsdb.search(name="fsi.io", cache=True)
result = dnsdb.search(name="fsi.io", cache=True, cache_timeout=900)
result = dnsdb.search(name="fsi.io",
                      cache=True,
                      cache_location="/tmp/dnsdb-cache")
result = dnsdb.quota()

print(result.records)
print(result.status_code)
print(result.error)
print(result.quota)
print(result.cached)
"""

import json
import gzip
import requests
from diskcache import Cache
from dnsdb import utils


class Dnsdb:
    """
    A dnsdb object for the Farsight Security DNSDB API
    """

    def __init__(
        self,
        api_key=None,
        server="https://api.dnsdb.info",
        cache=False,
        cache_location="/tmp/dnsdb-cache",
        cache_timeout=900,
    ):
        """
        :param api_key: string (required)
        :param server: string (optional: default='https://api.dnsdb.info')
        :param cache: boolean (optional)
            enable caching of dnsdb results to disk
        :param cache_location: string (optional: default='/tmp/dnsdb-cache')
            directory to store cached results
        :param cache_timeout: integer (optional: default=900)
            seconds until the cached result expires
        :return: object

        EXAMPLE USAGE:::

        client = dnsdb.Client(api_key)
        """

        self.api_key = api_key
        self.server = server
        self.cache = cache
        self.cache_location = cache_location
        self.cache_timeout = cache_timeout

        if api_key is None:
            raise Exception("You must supply a DNSDB API key.")

    def search(
        self,
        name=None,
        ip=None,
        hexadecimal=None,
        type="ANY",
        bailiwick=None,
        wildcard_left=None,
        wildcard_right=None,
        inverse=False,
        sort=True,
        return_limit=10000,
        remote_limit=50000,
        epoch=False,
        time_first_before=None,
        time_first_after=None,
        time_last_before=None,
        time_last_after=None,
    ):
        """
        A method of the DNSDB Class to search the DNSDB API.

        :param name: string (required)
            fully qualified domain name
        :param ip: string
            IPv4 or IPv6 address, CIDR notation is valid
        :param hexadecimal: string
            hexadecimal digits specifying a raw octet string
        :param type: string (optional: default="ANY")
            dns resource record types (ANY, A, MX, SIG, etc)
        :param bailiwick: string (optional: default=None)
            a label in a fqdn, not valid for inverse queries
        :param wildcard_left: Boolean (optional: default=None)
            wildcard search to the left of a dot in a domain name
        :param wildcard_right: Boolean (optional: default=None)
            wildcard search to the right of a dot in a domain name
        :param inverse: boolean (optional: default=False)
            search for names resolving to names (e.g. MX, NS, CNAME, etc)
            only valid when used with name
        :param sort: boolean (optional: default=True)
        :param return_limit: integer (optional: default=10000)
        :param remote_limit: integer (optional: default=50000)
        :param epoch: boolean (optional: default=False)
        :param time_first_before:
        :param time_first_after:
        :param time_last_before:
        :param time_last_after:

        :return: Object
        """

        options = dict()

        options["name"] = name
        options["ip"] = ip
        options["hex"] = hexadecimal
        options["type"] = type
        options["bailiwick"] = bailiwick
        options["wildcard_left"] = wildcard_left
        options["wildcard_right"] = wildcard_right
        options["inverse"] = inverse
        options["sort"] = sort
        options["return_limit"] = return_limit
        options["remote_limit"] = remote_limit
        options["epoch"] = epoch
        options["time_first_before"] = time_first_before
        options["time_first_after"] = time_first_after
        options["time_last_before"] = time_last_before
        options["time_last_after"] = time_last_after
        options["api_key"] = self.api_key
        options["server"] = self.server
        options["cache"] = self.cache
        options["cache_location"] = self.cache_location
        options["cache_timeout"] = self.cache_timeout

        options = utils.pre_process(options)

        uri = utils.build_uri(options)

        if options["cache"] is True:
            cache = Cache(options["cache_location"])

            cached_result = cache.get(uri)

            if cached_result:
                data = json.loads(gzip.decompress(cached_result).decode("utf-8"))
                results = Result(
                    records=data["records"],
                    status_code=data["status_code"],
                    error=data["error"],
                    quota=data["quota"],
                    cached=True,
                )
            else:
                results = _query(options, uri)
                if results.status_code == 200 or results.status_code == 404:
                    compressed = Result.to_compressed(results)
                    cache.set(uri, compressed, expire=options["cache_timeout"])
        else:
            results = _query(options, uri)

        if results.status_code == 200:
            results = utils.post_process(options, results)
            return results

        return results

    def quota(self):
        """
        Query DNSDB API for the current quota of the given API key

        :return: object
        """

        options = dict()
        options["api_key"] = self.api_key
        options["server"] = self.server

        path = "/lookup/rate_limit"

        uri_parts = (options["server"], path)

        uri = "".join(uri_parts)

        results = _query(options, uri, quota=True)

        return results


class Result:
    """
    A object to store the results of a DNSDB Search and related meta data.
    """

    def __init__(
        self, records=None, status_code=None, error=None, quota=None, cached=None
    ):
        """
        :param records: list of dictionaries
        :param status_code: integer
            DNSDB status code
        :param error: dictionary
            DNSDB error message
        :param quota: dictionary
            DNSDB quota information
        :param cached: boolean
        """
        self.status_code = status_code
        self.records = records
        self.error = error
        self.quota = quota
        self.cached = cached

    def to_dict(self):
        """
        Return the object as a dictionary

        :return: dictionary
        """
        data = dict(
            status_code=self.status_code,
            records=self.records,
            error=self.error,
            quota=self.quota,
            cached=self.cached,
        )
        return data

    def to_json(self):
        """
        Return the object as a JSON string

        :return: string
        """
        data = Result.to_dict(self)
        return json.dumps(data)

    def to_compressed(self):
        """
        Return the object as a gzipped JSON string

        :return: bytes
        """
        encoded = Result.to_json(self).encode("utf-8")
        compressed = gzip.compress(bytes(encoded))
        return compressed


def _query(options, uri, quota=False):
    """
    An internal HTTP function to query DNSDB API

    :param uri: string
    :param quota: boolean (default: False)
    :return: object
    """

    results = Result()
    error = dict()
    error.update({"code": None, "message": None})

    headers = {"Accept": "application/json", "X-API-Key": options["api_key"]}

    resp = requests.get(uri, headers=headers, stream=True)
    results.status_code = resp.status_code
    results.quota = utils.get_quota(response_headers=resp.headers)
    results.cached = False

    if resp.status_code == 200:
        records = []

        if quota is True:
            response = resp.json()
            results.quota = utils.get_quota(rate_limit=response["rate"])
            return results

        for line in resp.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                records.append(json.loads(decoded_line))
        results.records = records
    else:
        error["code"] = resp.status_code

        if resp.content:
            error["message"] = resp.content.decode("utf-8").rstrip()
        else:
            error["message"] = "Unavailable"

        results.error = error

    return results
