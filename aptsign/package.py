import os.path
import urllib.parse

from typing import Optional  # noqa

import apt


class PackageNotFound(Exception):
    pass


class UnknownSource(Exception):
    pass


class Package:
    def __init__(self, cache) -> None:
        self._cache = cache  # type: apt.cache.Cache

        self.filename = None  # type: Optional[str]
        self._package = None  # type: Optional[apt.package.Version]
        self.version = ''  # type: str
        self.arch = ''  # type: str

    def by_name(self, name) -> None:
        """ Select the package by name, selecting the install candidate by default """
        package = self._get_package_from_cache(name)  # type apt.package.Package

        self._package = package.candidate
        self.version = self._package.version
        self.arch = self._package.arch

    def by_filename(self, filename) -> apt.package.Version:
        """ Select the package from filename, using name and version """
        self.filename = filename

        filename = os.path.basename(filename)
        filename, _ = os.path.splitext(filename)

        name, version, arch = filename.split('_')

        package = self._get_package_from_cache(name)  # type apt.package.Package

        self.version = urllib.parse.unquote(version)
        self.arch = arch

        try:
            self._package = package.versions[self.version]
        except KeyError:
            raise PackageNotFound("Package {} {} not found in apt cache".format(name, version))

    @property
    def name(self):
        return self._package.package.name

    @property
    def sha256(self):
        return self._package.sha256

    @property
    def uri(self):
        return self._package.uri

    @property
    def repo(self):
        origins = self._package.origins

        # Skip installed package origin
        for origin in origins:
            if origin.archive != 'now':
                return origin

        raise UnknownSource("Unable to locate origin for package: {}".format(self.name))

    def __str__(self):
        return "{}-{}".format(self.name, self.version)

    def _get_package_from_cache(self, package) -> apt.package.Package:
        try:
            return self._cache[package]
        except KeyError:
            raise PackageNotFound("Package {} not found in apt cache".format(package))
