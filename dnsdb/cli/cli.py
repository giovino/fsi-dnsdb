#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line client for Python DNSDB module
"""

import argparse
import configparser
import os
import sys
from dnsdb import __version__
# from dnsdb import Dnsdb


DEFAULT_CONFIG_FILE = os.path.expanduser("~/.dnsdb.ini")


def main():

    epilog_text = """
    Time format options:
    yyyy (2016),
    yyyy-mm (2016-01),
    yyyy-mm-dd (2016-01-01),
    yyyymmdd (20160101),
    yyyymmddThh (20160101T12),
    yyyy-mm-ddThh:mm:ss-hh:mm (2016-01-01T00:00:00-00:00)
    """

    parser = argparse.ArgumentParser(
        description="CLI client for DNSDB", epilog=epilog_text
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="Path to config file",
        default=DEFAULT_CONFIG_FILE
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__)
    )

    parser.parse_args()
    args = parser.parse_args()

    print(args)

    sys.exit(0)


if __name__ == "__main__":
    main()
