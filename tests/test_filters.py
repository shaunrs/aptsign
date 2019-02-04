class TestFilter:
    def test_string_method_site(self, fixture_filter_site):
        assert str(fixture_filter_site) == "site: testrepo.org"

    def test_string_method_match_all(self, fixture_filter_multi_no_match):
        filter_string = str(fixture_filter_multi_no_match)
        expected_string = "Component: contrib; archive: stable; origin: Other; " \
                          "label: other; site: otherrepo.org"

        assert filter_string == expected_string

    def test_match_site_attribute(self, fixture_filter_site, fixture_package):
        assert fixture_filter_site.is_match(fixture_package) is True
        assert fixture_filter_site.app == 'debsig-verify -d'

    def test_match_all_attributes(self, fixture_filter_multi_match, fixture_package):
        assert fixture_filter_multi_match.is_match(fixture_package)

    def test_does_not_match(self, fixture_filter_multi_no_match, fixture_package):
        assert not fixture_filter_multi_no_match.is_match(fixture_package)


class TestFilters:
    def test_add_new_filter(self, fixture_filters_populated, fixture_package):
        match = fixture_filters_populated.is_match(fixture_package)

        assert str(match) == "site: testrepo.org"

    def test_no_filter_matched(self, fixture_filters_populated, fixture_package_not_matched):
        match = fixture_filters_populated.is_match(fixture_package_not_matched)

        assert match is False
