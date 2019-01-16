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

results = dnsdb.search(name="fsi.io")
results = dnsdb.search(name="mail.fsi.io", inverse=True)
results = dnsdb.search(ip="104.244.14.108")
results = dnsdb.search(ip="104.244.14.0/24")
results = dnsdb.search(ip="2620:11c:f008::108")
results = dnsdb.search(hexadecimal="36757a35")
quota = dnsdb.quota()
"""

import json
import requests
from dnsdb import utils


class Dnsdb:
    """
    A dnsdb object for the Farsight Security DNSDB API
    """
    def __init__(self, api_key=None, server='https://api.dnsdb.info'):
        """
        :param api_key: string (required)
        :param server: string (optional: default=https://api.dnsdb.info)
        :return: object

        EXAMPLE USAGE:::

        client = dnsdb.Client(api_key)
        """

        self.api_key = api_key
        self.server = server

        if api_key is None:
            raise Exception("You must supply a DNSDB API key.")

    def search(self,
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
               time_last_after=None):
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
        :param inverse: Boolean (optional: default=False)
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

        :return: List of dictionaries
        """

        options = dict()

        options['name'] = name
        options['ip'] = ip
        options['hex'] = hexadecimal
        options['type'] = type
        options['bailiwick'] = bailiwick
        options['wildcard_left'] = wildcard_left
        options['wildcard_right'] = wildcard_right
        options['inverse'] = inverse
        options['sort'] = sort
        options['return_limit'] = return_limit
        options['remote_limit'] = remote_limit
        options['epoch'] = epoch
        options['time_first_before'] = time_first_before
        options['time_first_after'] = time_first_after
        options['time_last_before'] = time_last_before
        options['time_last_after'] = time_last_after
        options['api_key'] = self.api_key
        options['server'] = self.server

        options = utils.validate_options(options)

        uri = utils.build_uri(options)

        results = _query(options, uri)

        if 'error' in results[0]:
            return results

        results = utils.post_process(options, results)
        return results

    def quota(self):
        """
        Query DNSDB API for the current quota of the given API key

        :return: List
        """

        options = dict()
        options['api_key'] = self.api_key
        options['server'] = self.server

        path = '/lookup/rate_limit'

        uri_parts = (options['server'], path)

        uri = ''.join(uri_parts)

        results = _query(options, uri, quota=True)

        return results


def _query(options, uri, quota=False):
    """
    An internal HTTP function to query DNSDB API

    :param uri: string
    :param quota: boolean (default: False)
    :return: List
    """

    results = []
    error = {'error': {'code': None,
                       'message': ''}}

    headers = {
        'Accept': 'application/json',
        'X-API-Key': options['api_key']
    }

    resp = requests.get(uri, headers=headers, stream=True)

    if resp.status_code == 200:

        if quota is True:
            results.append(resp.json())
            return resp.status_code, results

        for line in resp.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                results.append(json.loads(decoded_line))
    else:
        error['error']['code'] = resp.status_code
        if resp.content:
            error['error']['message'] = resp.content.decode('utf-8').rstrip()
        else:
            error['error']['message'] = 'Unavailable'
        results.append(error)

    return results
