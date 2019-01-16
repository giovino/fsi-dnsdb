# -*- coding: utf-8 -*-
"""
Utility functions needed by the DNSDB module
"""


def build_uri(options):
    """
    Build URI for DNSDB API query

    :param options: Dictionary
    :return: String
    """

    path = build_path(options)
    uri = build_parameters(options, path)

    return uri


def build_path(options):
    """
    Build the URI path needed to query the DNSDB API

    :param options: Dictionary
    :return: string
    """
    if options['name']:
        if options['inverse']:
            path = '/lookup/rdata/name/{}/{}'.format(options['name'],
                                                     options['type'])
            return path
        else:
            path = '/lookup/rrset/name/{}/{}'.format(options['name'],
                                                     options['type'])

            if options['bailiwick']:
                path += '/{}'.format(options['bailiwick'])
                return path
            return path
    elif options['ip']:
        options['ip'] = options['ip'].replace('/', ',')
        path = '/lookup/rdata/ip/{}'.format(options['ip'])
        return path
    elif options['hex']:
        path = '/lookup/rdata/raw/{}'.format(options['hex'])
        return path
    else:
        raise LookupError('name, ip, or hex was not specified')


def build_parameters(options, path):
    """
    Build the URI parameters needed to query the DNSDB API

    :param options: Dictionary
    :param path: String
    :return: String
    """

    time_filters = {'time_first_before': options['time_first_before'],
                    'time_first_after': options['time_first_after'],
                    'time_last_before': options['time_last_before'],
                    'time_last_after': options['time_last_after']}

    server_limit = '?limit={}'.format(options['remote_limit'])
    uri_parts = [options['server'], path, server_limit]

    for key, value in time_filters.items():
        if value:
            uri_parts.append('&{}={}'.format(key, value))

    uri = ''.join(uri_parts)

    return uri


def post_process(options, records):
    """
    Post processing of records; supports:
      1. converting epoch to 8601
      2. sorting of records by last seen
      3. Limiting the number of results returned

    :param options: Dictionary
    :param records: List (of dictionaries)
    :return: list (of dictionaries)
    """

    records = normalize(records)
    return_limit = options['return_limit']

    if options['sort']:
        records = sort(records)

    if not options['epoch']:
        records = epoch_to_timestamp(records)

    return records[0:return_limit]


def normalize(records):
    """
    Normalize result by removing the zone_time_first and zone_time_last keys
    and adding a source [sensor or zone] key pair.

    :param records: List (of dictionaries)
    :return: List (of dictionaries)
    """

    normalized = []

    for record in records:
        normalized_record = dict()
        normalized_record['source'] = 'sensor'

        keys = record.keys()
        for key in keys:
            if key == 'zone_time_first':
                normalized_record['time_first'] = record[key]
                normalized_record['source'] = 'zone'
            elif key == 'zone_time_last':
                normalized_record['time_last'] = record[key]
                normalized_record['source'] = 'zone'
            else:
                normalized_record[key] = record[key]
        normalized.append(normalized_record)

    return normalized


def sort(records):
    """
    Function to sort records by time_last

    :param records: List (of dictionaries)
    :return: List (of dictionaries)
    """

    from operator import itemgetter

    sorted_results = sorted(records, key=itemgetter('time_last'), reverse=True)
    return sorted_results


def epoch_to_timestamp(records):
    """
    Convert epoch timestamps to ISO 8601 (2015-01-04T09:30:21Z)

    :param records: List (of dictionaries)
    :return: List (of dictionaries)
    """

    from datetime import datetime

    for record in records:
        timestamp_keys = ['time_first', 'time_last']
        for key in timestamp_keys:
            if key in record:
                record[key] = datetime.fromtimestamp(record[key]).isoformat() \
                              + 'Z'
    return records


def validate_options(options):
    """
    Validate wildcard options

    :param options: Dictionary
    :return: Dictionary
    """

    name = options['name']
    wildecard_left = options['wildcard_left']
    wildcard_right = options['wildcard_right']

    if wildecard_left and wildcard_right:
        raise Exception("wildcard_left and wildcard_right cannot be used "
                        "simultaneously")
    if name:
        if wildecard_left or wildcard_right:
            name = validate_wildcard(name, wildecard_left, wildcard_right)
            options['name'] = name

    return options


def validate_wildcard(name, wildcard_left, wildcard_right):
    """
    A function to initiate the validation of wildcard_left or wildcard_right
    queries

    :param name: String
    :param wildcard_left: Boolean
    :param wildcard_right: Boolean
    :return: String
    """

    if wildcard_left:
        return validate_wildcard_left(name)
    if wildcard_right:
        return validate_wildcard_right(name)
    return name


def validate_wildcard_left(name):
    """
    Validate a name query using the wildcard_left option and add the correct
    wildcard syntax if needed

    :param name: String
    :return: String
    """

    if name[-1] == "*":
        raise Exception("Wildcard left lookup cannot end with an asterisk on "
                        "the right side")

    # Correct wildcard syntax, do nothing
    if name[0] == "*" and name[1] == ".":
        return name
    # Missing asterisk, add
    if name[0] == ".":
        return "*" + name
    # Missing asterisk and dot, add
    return "*." + name


def validate_wildcard_right(name):
    """
    Validate a name query using the wildcard_right option and add the correct
    wildcard syntax if needed

    :param name: String
    :return: String
    """

    if name[0] == "*":
        raise Exception("Wildcard right lookup cannot start with an asterisk "
                        "on the left side")

    # Correct wildcard syntax, do nothing
    if name[-1] == "*" and name[-2] == ".":
        return name
    # Missing asterisk, add
    if name[-1] == ".":
        return name + "*"
    # Missing asterisk and dot, add
    return name + ".*"


def debug(results, limit=1):
    """
    Debug function to print data structure info to stdout, used for development

    :param results: List
    :param limit: Int
    :return: None
    """
    from pprint import pprint
    print("Number of results: {}".format(len(results)))
    pprint(results[0:limit])

    return None
