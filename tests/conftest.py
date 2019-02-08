import sys
from copy import deepcopy

import yaml

import mock
import pytest

# pylint: disable=redefined-outer-name


try:
    from aptsign import Filter, Filters, Package
except ImportError:
    sys.modules['apt'] = mock.MagicMock()
    from aptsign import Filter, Filters, Package


@pytest.fixture
def mock_apt_origin_remote():
    mock_origin = mock.MagicMock()

    mock_origin.component = 'main'
    mock_origin.archive = 'testing'
    mock_origin.origin = 'Debian'
    mock_origin.label = 'Debian'
    mock_origin.site = 'testrepo.org'
    mock_origin.isTrusted = True

    return mock_origin


@pytest.fixture
def mock_apt_origin_local():
    mock_origin = mock.MagicMock()

    mock_origin.component = 'now'
    mock_origin.archive = 'now'
    mock_origin.origins = ''
    mock_origin.label = ''
    mock_origin.site = ''
    mock_origin.isTrusted = False

    return mock_origin


@pytest.fixture
def mock_apt_origin_no_match():
    mock_origin = mock.MagicMock()

    mock_origin.component = 'contrib'
    mock_origin.archive = 'stable'
    mock_origin.origins = 'Other'
    mock_origin.label = 'Other'
    mock_origin.site = 'someotherrepo.org'
    mock_origin.isTrusted = True

    return mock_origin


@pytest.fixture
def mock_apt_package(mock_apt_origin_local, mock_apt_origin_remote):
    package = mock.MagicMock(name='apt_package')

    package.sha256 = "82ca6040a94d2788c93919289ae052b703aaa164f9591bb74197a19431aaefad"
    package.uri = "http://testrepo.org/something"
    package.package.name = "mypackage"
    package.version = '1.0.1'
    package.arch = 'amd64'

    package.origins = [
        mock_apt_origin_local, mock_apt_origin_remote
    ]

    package.versions = {
        '1.0.1': package
    }

    package.candidate = package

    return package


@pytest.fixture
def mock_apt_package_encoded(mock_apt_package):
    package = deepcopy(mock_apt_package)

    package.package.name = 'encodedpackage'
    package.version = '3:6.03+dfsg-14.1+deb9u1'

    package.versions = {
        '3:6.03+dfsg-14.1+deb9u1': package
    }

    return package


@pytest.fixture
def mock_apt_cache(mock_apt_package, mock_apt_package_encoded):
    cache = {
        'mypackage': mock_apt_package,
        'encodedpackage': mock_apt_package_encoded
    }

    return cache


@pytest.fixture
def fixture_configuration():
    with open('tests/fixtures/aptsign_config.yml') as _file:
        config = yaml.load(_file)

    return config


@pytest.fixture
def mock_apt():
    return mock.MagicMock()


@pytest.fixture
def fixture_filter_site(fixture_configuration):
    filter_yaml = fixture_configuration['repositories']['testfilter_site']['filter']
    filter_app = fixture_configuration['repositories']['testfilter_site']['app']

    return Filter(filter_yaml, filter_app)


@pytest.fixture
def fixture_filter_multi_match(fixture_configuration):
    filter_yaml = fixture_configuration['repositories']['testfilter_multi_match']['filter']

    return Filter(filter_yaml)


@pytest.fixture
def fixture_filter_multi_no_match(fixture_configuration):
    filter_yaml = fixture_configuration['repositories']['testfilter_multi_nomatch']['filter']

    return Filter(filter_yaml)


@pytest.fixture
def fixture_package(mock_apt_cache):
    package = Package(mock_apt_cache)

    package.by_name('mypackage')

    return package


@pytest.fixture
def fixture_package_not_matched(mock_apt_cache, mock_apt_origin_no_match):
    mock_apt_cache['mypackage'].origins = [
        mock_apt_origin_no_match
    ]

    package = Package(mock_apt_cache)

    package.by_name('mypackage')

    return package


@pytest.fixture
def fixture_package_no_origin(mock_apt_cache):
    mock_apt_cache['mypackage'].origins = []

    package = Package(mock_apt_cache)

    package.by_name('mypackage')

    return package


@pytest.fixture
def fixture_filters():
    return Filters()


@pytest.fixture
def fixture_filters_populated(fixture_configuration):
    filters = Filters()

    for _, repo in fixture_configuration['repositories'].items():
        filters.new(repo['filter'], repo['app'])

    return filters
