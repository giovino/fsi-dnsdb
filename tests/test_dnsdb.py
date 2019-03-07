import pytest
from dnsdb.dnsdb import utils
from dnsdb import __version__

RECORDS = [
    {
        "count": 57,
        "time_first": 1381267249,
        "time_last": 1417729108,
        "rrname": "www.fsi.io.",
        "rrtype": "A",
        "bailiwick": "fsi.io.",
        "rdata": ["66.160.140.76"],
    },
    {
        "count": 4838,
        "time_first": 1433657594,
        "time_last": 1538006017,
        "rrname": "www.fsi.io.",
        "rrtype": "A",
        "bailiwick": "fsi.io.",
        "rdata": ["104.244.13.104"],
    },
]
STATUS_CODE = 200
ERROR = None
QUOTA = {
    "reset": "1551830400",
    "results_max": None,
    "expires": None,
    "limit": "1000000",
    "remaining": "999967",
}


class Result:
    """
    A object to store the results of a DNSDB Search and related meta data.
    """

    def __init__(self, records=None, status_code=None, error=None, quota=None):

        self.status_code = status_code
        self.records = records
        self.error = error
        self.quota = quota


def test_version():
    assert __version__ == "0.2.0"


def get_options():

    options = dict()

    options["name"] = None
    options["ip"] = None
    options["hex"] = None
    options["type"] = "ANY"
    options["bailiwick"] = None
    options["wildcard_left"] = None
    options["wildcard_right"] = None
    options["inverse"] = False
    options["sort"] = True
    options["return_limit"] = 10000
    options["remote_limit"] = 50000
    options["epoch"] = False
    options["time_first_before"] = None
    options["time_first_after"] = None
    options["time_last_before"] = None
    options["time_last_after"] = None
    options["api_key"] = "12345"
    options["server"] = "https://api.dnsdb.info"

    return options


def test_wildcard_left_right_true():

    options = get_options()
    options["name"] = "fsi.io"
    options["wildcard_left"] = True
    options["wildcard_right"] = True

    with pytest.raises(Exception):
        utils.validate_options(options)


def test_validate_options_wildcard_left_true_bare():

    options = get_options()
    options["name"] = "fsi.io"
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    assert options["name"] == "*.fsi.io"


def test_validate_options_wildcard_left_true_dot():

    options = get_options()
    options["name"] = ".fsi.io"
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    assert options["name"] == "*.fsi.io"


def test_validate_options_wildcard_left_true_star_dot():

    options = get_options()
    options["name"] = "*.fsi.io"
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    assert options["name"] == "*.fsi.io"


def test_validate_options_wildcard_right_true_bare():

    options = get_options()
    options["name"] = "fsi"
    options["wildcard_right"] = True

    options = utils.validate_options(options)
    assert options["name"] == "fsi.*"


def test_validate_options_wildcard_right_true_dot():

    options = get_options()
    options["name"] = "fsi."
    options["wildcard_right"] = True

    options = utils.validate_options(options)
    assert options["name"] == "fsi.*"


def test_validate_options_wildcard_right_true_dot_star():

    options = get_options()
    options["name"] = "fsi.*"
    options["wildcard_right"] = True

    options = utils.validate_options(options)
    assert options["name"] == "fsi.*"


def test_build_uri_name():

    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_ip():

    valid = "https://api.dnsdb.info/lookup/rdata/ip/104.244.14.108?limit=50000"

    options = get_options()
    options["ip"] = "104.244.14.108"

    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_hex():

    valid = "https://api.dnsdb.info/lookup/rdata/raw/36757a35?limit=50000"

    options = get_options()
    options["hex"] = "36757a35"

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_type():

    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.io/A?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["type"] = "A"

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_bailiwick():
    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY/io.?limit" "=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["bailiwick"] = "io."

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_type_bailiwick():

    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.io/NS/io.?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["type"] = "NS"
    options["bailiwick"] = "io."

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_wildcard_left():

    valid = "https://api.dnsdb.info/lookup/rrset/name/*.fsi.io/ANY?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_wildcard_right():

    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.*/ANY?limit=50000"

    options = get_options()
    options["name"] = "fsi"
    options["wildcard_right"] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_inverse():

    valid = "https://api.dnsdb.info/lookup/rdata/name/fsi.io/ANY?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["inverse"] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_inverse_wildcard_left():

    valid = "https://api.dnsdb.info/lookup/rdata/name/*.fsi.io/ANY?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["inverse"] = True
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_type_inverse_wildcard_left():

    valid = "https://api.dnsdb.info/lookup/rdata/name/*.fsi.io/MX?limit=50000"

    options = get_options()
    options["name"] = "fsi.io"
    options["type"] = "MX"
    options["inverse"] = True
    options["wildcard_left"] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_remote_limit():

    valid = "https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=25000"

    options = get_options()
    options["name"] = "fsi.io"
    options["remote_limit"] = 25000

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_time_first_before():
    valid = (
        "https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000"
        "&time_first_before=1540864340"
    )

    options = get_options()
    options["name"] = "fsi.io"
    options["time_first_before"] = 1540864340

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_build_uri_name_time_all():
    valid = (
        "https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000"
        "&time_first_before=1540864340&time_first_after=1374093289"
        "&time_last_before=1540864340&time_last_after=1374093289"
    )

    options = get_options()
    options["name"] = "fsi.io"
    options["time_first_before"] = 1540864340
    options["time_first_after"] = 1374093289
    options["time_last_before"] = 1540864340
    options["time_last_after"] = 1374093289

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == valid


def test_get_quota_one():
    response_headers = {
        "Server": "nginx/1.10.3",
        "Date": "Tue, 05 Mar 2019 18:58:04 GMT",
        "Content-Type": "application/json",
        "Transfer-Encoding": "chunked",
        "Connection": "keep-alive",
        "Vary": "Accept-Encoding",
        "X-RateLimit-Limit": "1000000",
        "X-RateLimit-Remaining": "999954",
        "X-RateLimit-Reset": "1551830400",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Expose-Headers": "X-RateLimit-Limit, "
        "X-RateLimit-Remaining, X-RateLimit-Reset",
        "Access-Control-Max-Age": "86400",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET, POST",
        "Access-Control-Allow-Headers": "Accept, "
        "Cache-Control, "
        "Pragma, Origin, "
        "Authorization, "
        "Cookie, "
        "Content-Type, "
        "X-API-Key",
        "Strict-Transport-Security": "max-age=15768000",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Encoding": "gzip",
    }

    quota = utils.get_quota(response_headers=response_headers)
    assert quota["remaining"] == "999954"


def test_get_quota_two():
    rate_limit = {
        "rate": {
            "reset": 1551830400,
            "results_max": 1000000,
            "limit": 1000000,
            "remaining": 999953,
        }
    }

    quota = utils.get_quota(rate_limit=rate_limit["rate"])
    assert quota["remaining"] == 999953


def test_normalize_rate():
    rate_limit = {
        "rate": {
            "reset": "n/a",
            "results_max": 1000000,
            "expires": 1569888000,
            "limit": 25000,
            "remaining": 24783,
        }
    }

    rate = utils.get_quota(rate_limit=rate_limit["rate"])
    quota = utils.normalize_rate(rate)
    assert quota["reset"] is None


def test_post_process_name_sort():

    options = get_options()
    result = Result(RECORDS, STATUS_CODE, ERROR, QUOTA)
    options["name"] = "fsi.io"
    options["sort"] = True
    options["epoch"] = True

    result = utils.post_process(options, result)
    records = result.records
    assert records[0]["time_last"] == 1538006017


def test_post_process_name_epoch():

    options = get_options()
    result = Result(RECORDS, STATUS_CODE, ERROR, QUOTA)
    options["name"] = "fsi.io"
    options["sort"] = True
    options["epoch"] = False

    result = utils.post_process(options, result)
    records = result.records
    assert records[0]["time_last"] == "2018-09-26T23:53:37Z"


def test_post_process_name_return_limit():

    options = get_options()
    result = Result(RECORDS, STATUS_CODE, ERROR, QUOTA)
    options["name"] = "fsi.io"
    options["return_limit"] = 1

    result = utils.post_process(options, result)
    records = result.records
    assert len(records) == 1


def test_epoch_timestamp():

    timestamp = 1546300800

    options = get_options()
    options["time_last_after"] = timestamp
    options["epoch"] = True

    options = utils.pre_process(options)
    assert options["time_last_after"] == 1546300800


def test_human_date_one():

    date = "2019-01-01"

    options = get_options()
    options["time_last_after"] = date
    options["epoch"] = False

    options = utils.pre_process(options)
    assert options["time_last_after"] == 1546300800


def test_human_date_two():

    date = "2018-06-13T02:05:36Z"

    options = get_options()
    options["time_last_after"] = date
    options["epoch"] = False

    options = utils.pre_process(options)
    assert options["time_last_after"] == 1528855536
