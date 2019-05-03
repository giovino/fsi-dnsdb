#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line client for Python DNSDB module
"""

import argparse
import configparser
import logging
import os
import sys
from dnsdb import __version__
from dnsdb.cli import utils
from dnsdb import Dnsdb

DEFAULT_CONFIG_FILE = os.path.expanduser("~/.dnsdb.ini")


def main():
    """
    Main function
    :return: Shell exit code (0 or 1)
    """

    dnsdb_param = dict(api_key=None)
    dnsdb_search_param = dict()
    epilog_text = utils.epilog()

    parser = argparse.ArgumentParser(
        description="CLI client for DNSDB", epilog=epilog_text
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--name", dest="name", help="fully qualified domain mame")
    group.add_argument(
        "-i", "--ip", dest="ip", help="IPv4 or IPv6 address, CIDR notation is valid"
    )
    group.add_argument(
        "--hex",
        dest="hexadecimal",
        help="hexadecimal digits specifying a raw octet string",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        help="dns resource record types (ANY, A, MX, SIG, etc)",
    )
    parser.add_argument(
        "-b",
        "--bailiwick",
        dest="bailiwick",
        help="a label in a fqdn, not valid for inverse queries",
    )
    parser.add_argument(
        "-r",
        "--inverse",
        action="store_true",
        default=False,
        help="search for names resolving to names (e.g. MX, NS, CNAME, etc)",
    )
    parser.add_argument(
        "--wildcard-left",
        action="store_true",
        default=False,
        help="wildcard search to the left of a dot in a domain name",
    )
    parser.add_argument(
        "--wildcard-right",
        action="store_true",
        default=False,
        help="wildcard search to the right of a dot in a domain name",
    )
    parser.add_argument(
        "--sort", action="store_true", default=True, help="sort results by time last"
    )
    parser.add_argument(
        "--epoch", action="store_true", default=False, help="return timestamps in epoch"
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="oformat",
        choices=["csv", "json", "jsonp"],
        default="json",
        help="output formats",
    )
    parser.add_argument(
        "--return-limit",
        dest="return_limit",
        type=int,
        help="number of client side results returned",
    )
    parser.add_argument(
        "--remote-limit",
        dest="remote_limit",
        type=int,
        help="number of server side results returned",
    )
    parser.add_argument(
        "--first-before",
        dest="time_first_before",
        help="server side filter for time first before",
    )
    parser.add_argument(
        "--first-after",
        dest="time_first_after",
        help="server side filter for time first after",
    )
    parser.add_argument(
        "--last-before",
        dest="time_last_before",
        help="server side filter for time last before",
    )
    parser.add_argument(
        "--last_after",
        dest="time_last_after",
        help="server side filter for time last after",
    )
    parser.add_argument(
        "--cache", action="store_true", default=False, help="Use cached results"
    )
    parser.add_argument("--cache-location", dest="cache_location", help="Path to cache")
    parser.add_argument(
        "--cache-timeout", dest="cache_timeout", type=int, help="Timeout in seconds"
    )
    parser.add_argument("--apikey", dest="api_key", help="DNSDB API key")
    parser.add_argument("--server", dest="server", help="Server URL")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Set the verbosity level"
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="Path to config file",
        default=DEFAULT_CONFIG_FILE,
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    parser.parse_args()
    args = parser.parse_args()

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(len(log_levels) - 1, args.verbose)]

    logging.basicConfig(level=log_level, format="%(message)s")
    logger = logging.getLogger()

    logger.debug("args: %s", vars(args))

    if os.path.isfile(args.config):
        config = configparser.ConfigParser()
        config.read(args.config)

        if config["api.dnsdb.info"].get("api_key"):
            dnsdb_param["api_key"] = config["api.dnsdb.info"].get("api_key")
        if config["api.dnsdb.info"].get("server"):
            dnsdb_param["server"] = config["api.dnsdb.info"].get("server")
        if config["api.dnsdb.info"].getboolean("cache"):
            dnsdb_param["cache"] = config["api.dnsdb.info"].getboolean("cache")
        if config["api.dnsdb.info"].get("cache_location"):
            dnsdb_param["cache_location"] = config["api.dnsdb.info"].get(
                "cache_location"
            )
        if config["api.dnsdb.info"].get("cache_timeout"):
            dnsdb_param["cache_timeout"] = config["api.dnsdb.info"].getint(
                "cache_timeout"
            )
        logger.debug("config: %s", dnsdb_param)
    else:
        logger.debug("Config file not found: %s", args.config)

    # command line arguments take precedent over values specified in conf file
    valid_dnsdb_parameters = [
        "api_key",
        "server",
        "cache",
        "cache_location",
        "cache_timeout",
    ]

    for dnsdb_parameter in valid_dnsdb_parameters:
        if getattr(args, dnsdb_parameter):
            dnsdb_param[dnsdb_parameter] = getattr(args, dnsdb_parameter)

    valid_dnsdb_search_param = [
        "name",
        "ip",
        "hexadecimal",
        "type",
        "bailiwick",
        "inverse",
        "wildcard_left",
        "wildcard_right",
        "sort",
        "epoch",
        "return_limit",
        "remote_limit",
        "time_first_before",
        "time_first_after",
        "time_last_before",
        "time_last_after",
    ]

    for dnsdb_search_parameter in valid_dnsdb_search_param:
        if getattr(args, dnsdb_search_parameter):
            dnsdb_search_param[dnsdb_search_parameter] = getattr(
                args, dnsdb_search_parameter
            )

    if dnsdb_param["api_key"] is not None:
        dnsdb = Dnsdb(**dnsdb_param)
        result = dnsdb.search(**dnsdb_search_param)
        logger.debug("status_code: %s", result.status_code)
        logger.debug("error: %s", result.error)
        logger.debug("cached: %s", result.cached)
        logger.debug("quota: %s", result.quota)
    else:
        logger.critical("Error: API key not specified")
        sys.exit(1)

    if result.status_code == 403:
        logger.critical("Invalid API key")
        sys.exit(1)

    if result.records:
        utils.output(args.oformat, result.records)
    else:
        logger.info("No records found")

    sys.exit(0)


if __name__ == "__main__":
    main()
