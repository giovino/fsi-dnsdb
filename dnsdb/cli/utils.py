# -*- coding: utf-8 -*-
"""
Utility functions needed by the DNSDB module
"""

import json
import csv
import sys


def epilog():
    """
    Returns epilog text for CLI help

    :return: string
    """

    epilog_text = """
    Time format options:
    yyyy (2016),
    yyyy-mm (2016-01),
    yyyy-mm-dd (2016-01-01),
    yyyymmdd (20160101),
    yyyymmddThh (20160101T12),
    yyyy-mm-ddThh:mm:ss-hh:mm (2016-01-01T00:00:00-00:00)
    """
    return epilog_text


def get_fieldnames(records):
    """
    Extract fieldnames for CSV headers from list of results

    :param records: list
    :return: list
    """

    fieldnames = []

    ordered_fieldname = (
        "time_last",
        "time_first",
        "source",
        "count",
        "bailiwick",
        "rrname",
        "rrtype",
        "rdata",
    )

    # build a list of unique keys from all returned records
    for record in records:
        keys = list(record.keys())
        for key in keys:
            if key not in fieldnames:
                fieldnames.append(key)

    # sort fieldnames based on order in ordered_fieldname
    fieldnames = sorted(fieldnames, key=lambda x: ordered_fieldname.index(x))

    return fieldnames


def flatten_record(records):
    """
    Flatten record objects by rdata field to support line delimited (CSV) output

    :param records: list
    :return: list
    """

    flattened_records = []

    for record in records:
        for rdata in record["rdata"]:
            r = record
            r["rdata"] = rdata
            flattened_records.append(r)

    return flattened_records


def out_json(records):
    """
    Print results in json to stdout

    :param records: list
    :return: None
    """

    for record in records:
        print(json.dumps(record))


def out_jsonp(records):
    """
    Print results in json (pretty print) to stdout

    :param records: list
    :return: None
    """

    for record in records:
        print(json.dumps(record, indent=4))


def out_csv(records):
    """
    Print results in csv to stdout

    :param records: list
    :return: None
    """

    fieldnames = get_fieldnames(records)
    flat_records = flatten_record(records)

    writer = csv.DictWriter(sys.stdout, fieldnames)
    for record in flat_records:
        writer.writerow(record)


def output(oformat, records):
    """

    :param oformat: string
    :param records: list
    :return:
    """
    if oformat == "json":
        out_json(records)
    elif oformat == "jsonp":
        out_jsonp(records)
    elif oformat == "csv":
        out_csv(records)
