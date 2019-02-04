import sys
import mock

import pytest

try:
    from aptsign import Package, PackageNotFound, UnknownSource
except ImportError:
    sys.modules['apt'] = mock.MagicMock()
    from aptsign import Package, PackageNotFound, UnknownSource


class TestPackage:
    def assert_package(self, package):
        assert package.name == 'mypackage'
        assert package.version == '1.0.1'
        assert package.sha256 == "82ca6040a94d2788c93919289ae052b703aaa164f9591bb74197a19431aaefad"
        assert package.uri == "http://testrepo.org/something"
        assert package.name == "mypackage"
        assert package.version == '1.0.1'
        assert package.arch == 'amd64'

    def test_by_name(self, mock_apt_cache):
        package = Package(mock_apt_cache)

        package.by_name('mypackage')

        self.assert_package(package)

    def test_by_filename(self, mock_apt_cache):
        package = Package(mock_apt_cache)

        package.by_filename('/var/cache/apt/archive/mypackage_1.0.1_amd64.deb')

        self.assert_package(package)

    def test_invalid_package_by_name(self, mock_apt_cache):
        package = Package(mock_apt_cache)

        with pytest.raises(PackageNotFound):
            package.by_name("other-package")

    def test_invalid_package_by_filename(self, mock_apt_cache):
        package = Package(mock_apt_cache)

        with pytest.raises(PackageNotFound):
            package.by_filename("mypackage_1.2.1_amd64.deb")

    def test_unknown_origin_source(self, fixture_package_no_origin):
        with pytest.raises(UnknownSource):
            assert fixture_package_no_origin.repo.label

    def test_string_method(self, fixture_package):
        assert str(fixture_package) == "mypackage-1.0.1"
