import pytest
from dnsdb.dnsdb import utils
from dnsdb import __version__


def test_version():
    assert __version__ == '0.1.1'


def get_options():

    options = dict()

    options['name'] = None
    options['ip'] = None
    options['hex'] = None
    options['type'] = "ANY"
    options['bailiwick'] = None
    options['wildcard_left'] = None
    options['wildcard_right'] = None
    options['inverse'] = False
    options['sort'] = True
    options['return_limit'] = 10000
    options['remote_limit'] = 50000
    options['epoch'] = False
    options['time_first_before'] = None
    options['time_first_after'] = None
    options['time_last_before'] = None
    options['time_last_after'] = None
    options['api_key'] = "12345"
    options['server'] = "https://api.dnsdb.info"

    return options


def get_results():

    results =[{"count" : 57,
               "time_first":1381267249,
               "time_last":1417729108,
               "rrname":"www.fsi.io.",
               "rrtype":"A",
               "bailiwick":"fsi.io.",
               "rdata":["66.160.140.76"]},
              {"count":4838,
               "time_first":1433657594,
               "time_last":1538006017,
               "rrname":"www.fsi.io.",
               "rrtype":"A",
               "bailiwick":"fsi.io.",
               "rdata":["104.244.13.104"]}]

    return results


def test_wildcard_left_right_true():

    options = get_options()
    options['name'] = "fsi.io"
    options['wildcard_left'] = True
    options['wildcard_right'] = True

    with pytest.raises(Exception):
        utils.validate_options(options)


def test_validate_options_wildcard_left_true_bare():

    options = get_options()
    options['name'] = "fsi.io"
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    assert options['name'] == '*.fsi.io'


def test_validate_options_wildcard_left_true_dot():

    options = get_options()
    options['name'] = ".fsi.io"
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    assert options['name'] == '*.fsi.io'


def test_validate_options_wildcard_left_true_star_dot():

    options = get_options()
    options['name'] = "*.fsi.io"
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    assert options['name'] == '*.fsi.io'


def test_validate_options_wildcard_right_true_bare():

    options = get_options()
    options['name'] = "fsi"
    options['wildcard_right'] = True

    options = utils.validate_options(options)
    assert options['name'] == 'fsi.*'


def test_validate_options_wildcard_right_true_dot():

    options = get_options()
    options['name'] = "fsi."
    options['wildcard_right'] = True

    options = utils.validate_options(options)
    assert options['name'] == 'fsi.*'


def test_validate_options_wildcard_right_true_dot_star():

    options = get_options()
    options['name'] = "fsi.*"
    options['wildcard_right'] = True

    options = utils.validate_options(options)
    assert options['name'] == 'fsi.*'


def test_build_uri_name():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_ip():

    VALID = 'https://api.dnsdb.info/lookup/rdata/ip/104.244.14.108?limit=50000'

    options = get_options()
    options['ip'] = '104.244.14.108'

    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_hex():

    VALID = 'https://api.dnsdb.info/lookup/rdata/raw/36757a35?limit=50000'

    options = get_options()
    options['hex'] = '36757a35'

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_type():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/A?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['type'] = 'A'

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_bailiwick():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY/io.?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['bailiwick'] = 'io.'

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_type_bailiwick():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/NS/io.?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['type'] = 'NS'
    options['bailiwick'] = 'io.'

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_wildcard_left():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/*.fsi.io/ANY?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_wildcard_right():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.*/ANY?limit=50000'

    options = get_options()
    options['name'] = 'fsi'
    options['wildcard_right'] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_inverse():

    VALID = 'https://api.dnsdb.info/lookup/rdata/name/fsi.io/ANY?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['inverse'] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_inverse_wildcard_left():

    VALID = 'https://api.dnsdb.info/lookup/rdata/name/*.fsi.io/ANY?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['inverse'] = True
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_type_inverse_wildcard_left():

    VALID = 'https://api.dnsdb.info/lookup/rdata/name/*.fsi.io/MX?limit=50000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['type'] = 'MX'
    options['inverse'] = True
    options['wildcard_left'] = True

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_remote_limit():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=25000'

    options = get_options()
    options['name'] = 'fsi.io'
    options['remote_limit'] = 25000

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_time_first_before():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000&time_first_before=1540864340'

    options = get_options()
    options['name'] = 'fsi.io'
    options['time_first_before'] = 1540864340

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_build_uri_name_time_all():

    VALID = 'https://api.dnsdb.info/lookup/rrset/name/fsi.io/ANY?limit=50000&time_first_before=1540864340&time_first_after=1374093289&time_last_before=1540864340&time_last_after=1374093289'

    options = get_options()
    options['name'] = 'fsi.io'
    options['time_first_before'] = 1540864340
    options['time_first_after'] = 1374093289
    options['time_last_before'] = 1540864340
    options['time_last_after'] = 1374093289

    options = utils.validate_options(options)
    uri = utils.build_uri(options)
    assert uri == VALID


def test_post_process_name_sort():

    VALID = 'test'

    options = get_options()
    results = get_results()
    options['name'] = 'fsi.io'
    options['sort'] = True
    options['epoch'] = True

    results = utils.post_process(options, results)
    assert results[0]['time_last'] == 1538006017


def test_post_process_name_epoch():

    VALID = 'test'

    options = get_options()
    results = get_results()
    options['name'] = 'fsi.io'
    options['sort'] = True
    options['epoch'] = False

    results = utils.post_process(options, results)
    assert results[0]['time_last'] == "2018-09-26T23:53:37Z"


def test_post_process_name_return_limit():

    VALID = 'test'

    options = get_options()
    results = get_results()
    options['name'] = 'fsi.io'
    options['return_limit'] = 1

    results = utils.post_process(options, results)
    assert len(results) == 1
