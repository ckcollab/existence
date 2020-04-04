"""
These are some really weak basic, more integration testing than unit testing -- better than nothing!

These may not work properly on platforms other than Windows

The directory test_data/ is where some of these tests get their data.
"""
from unittest.mock import patch

import existence
import unittest


class ExistenceTest(unittest.TestCase):
    def tearDown(self):
        super(ExistenceTest, self).tearDown()

        existence.URL_CACHE = set()
        existence.BROKEN_URLS = []


class TestGettingURLs(ExistenceTest):

    def test_directory_get_urls_filters_files_that_dont_end_with_html(self):
        urls = [url for url, file_name, line_number in existence.directory_get_urls("test_data")]

        self.assertIn("http://google.com", urls)
        self.assertIn("http://python.org", urls)
        self.assertIn("http://this-domain-name-doesnt-exist-no-way", urls)
        self.assertIn("http://ericcarmichael.com", urls)
        self.assertIn("http://ericcarmichael.com", urls)

        # Data from test3.not_html wasn't scanned!
        self.assertEqual(len(urls), 4)

    def test_parse_html_urls_caches_findings(self):
        with open("test_data/test.html") as f:
            list(existence.parse_html_urls("test.html", f.read()))
        self.assertEqual(len(existence.URL_CACHE), 3)

    def test_parse_html_urls_ignores_urls_hash_or_mailto(self):
        with open("test_data/test.html") as f:
            list(existence.parse_html_urls("test.html", f.read()))

        # Would be more total links if it doesn't ignore these two:
        #     <a href="#">should be ignored</a>
        #     <a href="mailto:eric@email">should be ignored</a>
        self.assertEqual(len(existence.URL_CACHE), 3)

    @patch("existence.platform.system")
    def test_parse_html_urls_cleans_up_local_windows_urls(self, system_mock):
        system_mock.return_value = "Windows"

        # Raw string here for dang windows paths
        windows_link = r'<a href="C:\Users\Eric\Downloads\funny_picture.jpg">a hilarious picture</a>'
        urls = list(existence.parse_html_urls("test.html", windows_link))

        # <a href="C:\Users\Eric\Downloads\funny_picture.jpg">a hilarious picture</a>
        self.assertEqual(urls[0][0], 'file:///C:/Users\\Eric\\Downloads\\funny_picture.jpg')


class TestVerifyingURLsExist(ExistenceTest):
    def test_scan_directory_for_bad_urls_works(self):
        broken_urls = [url for url, file_name, line_number in existence.scan("test_data")]
        self.assertIn('http://this-domain-name-doesnt-exist-no-way', broken_urls)
