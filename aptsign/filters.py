from typing import Union


class Filter:
    def __init__(self, _filter_yaml, app=None) -> None:
        self.app = app  # type: str

        self.component = _filter_yaml.get('component')  # type: str
        self.archive = _filter_yaml.get('archive')  # type: str
        self.origin = _filter_yaml.get('origin')  # type: str
        self.label = _filter_yaml.get('label')  # type: str
        self.site = _filter_yaml.get('site')  # type: str

    def is_match(self, package) -> bool:
        match = True  # type: bool

        # All attributes specified must match, unspecified attributes not counted
        if self.component and not self._match_attribute('component', package.repo.component):
            match = False

        if self.archive and not self._match_attribute('archive', package.repo.archive):
            match = False

        if self.origin and not self._match_attribute('origin', package.repo.origin):
            match = False

        if self.label and not self._match_attribute('label', package.repo.label):
            match = False

        if self.site and not self._match_attribute('site', package.repo.site):
            match = False

        return match

    def _match_attribute(self, attribute, attribute_value) -> bool:
        attr = getattr(self, attribute)

        if attr == attribute_value:
            return True

        return False

    def __str__(self) -> str:
        output = []

        if self.component:
            output.append("Component: {}".format(self.component))

        if self.archive:
            output.append("archive: {}".format(self.archive))

        if self.origin:
            output.append("origin: {}".format(self.origin))

        if self.label:
            output.append("label: {}".format(self.label))

        if self.site:
            output.append("site: {}".format(self.site))

        return "; ".join(output)


class Filters:
    def __init__(self) -> None:
        self._filters = []  # type: list

    def is_match(self, package) -> Union[bool, list]:
        # All attributes specified must match
        # We will only ever have a single Filter match for a given package
        for _filter in self._filters:
            if _filter.is_match(package):
                return _filter

        return False

    def new(self, filter_dict, app=None) -> Filter:
        _filter = Filter(filter_dict, app)
        self._filters.append(_filter)

        return _filter
