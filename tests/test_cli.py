import subprocess
import pytest

from aptsign import cli, PackageNotFound


class TestCli:

    PACKAGE_FILENAME_VALID = '/var/cache/apt/archive/mypackage_1.0.1_amd64.deb'
    PACKAGE_FILENAME_INVALID = '/var/cache/apt/archive/nonexistant_1.0.1_amd64.deb'

    def test_valid_package_filename(self, fixture_configuration, mock_apt_cache, mocker):
        mock_subprocess = mocker.patch('subprocess.check_output')

        cli.process_package(fixture_configuration, self.PACKAGE_FILENAME_VALID, mock_apt_cache)

        mock_subprocess.assert_called_once_with(
            ['debsig-verify', '-d', self.PACKAGE_FILENAME_VALID],
            stderr=mocker.ANY
        )

    def test_invalid_package_filename(self, fixture_configuration, mock_apt_cache, mocker):
        mock_subprocess = mocker.patch('subprocess.check_output')

        with pytest.raises(PackageNotFound):
            cli.process_package(
                fixture_configuration, self.PACKAGE_FILENAME_INVALID, mock_apt_cache
            )

        mock_subprocess.assert_not_called()

    def test_signature_verification_failed(self, fixture_configuration, mock_apt_cache, mocker):
        mock_subprocess = mocker.patch('subprocess.check_output')

        mock_subprocess.side_effect = subprocess.CalledProcessError(2, 'test')
        mock_subprocess.side_effect.return_code = 2

        with pytest.raises(SystemExit) as exit_exception:
            cli.process_package(
                fixture_configuration, self.PACKAGE_FILENAME_VALID, mock_apt_cache
            )

        assert exit_exception.value.code == 2

    def test_no_package_filter(self, mock_apt_cache, mocker):
        mock_subprocess = mocker.patch('subprocess.check_output')

        config = {
            'repositories': {}
        }

        cli.process_package(config, self.PACKAGE_FILENAME_VALID, mock_apt_cache)

        mock_subprocess.assert_not_called()
