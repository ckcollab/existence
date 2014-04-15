'''
These are some really weak basic, more integration testing than unit testing -- better than nothing!

These may not work properly on platforms other than Windows

The directory test_data/ is where some of these tests get their data.
'''
import existence
import unittest


class ExistenceTest(unittest.TestCase):
    def tearDown(self):
        super(ExistenceTest, self).tearDown()

        existence.URL_CACHE = []
        existence.BROKEN_URLS = []


class TestGettingURLs(ExistenceTest):

    def test_directory_get_urls_filters_files_that_dont_end_with_html(self):
        urls = existence.directory_get_urls("test_data")

        self.assertEquals("http://google.com", urls[0][0])
        self.assertEquals("http://python.org", urls[1][0])
        self.assertEquals("http://this-domain-name-doesnt-exist-no-way", urls[2][0])
        self.assertEquals("http://ericcarmichael.com", urls[3][0])
        self.assertEquals("http://ericcarmichael.com", urls[3][0])
        # Data from test3.not_html wasn't scanned!
        self.assertEquals(len(urls), 4)

    def test_parse_html_urls_caches_findings(self):
        existence.parse_html_urls("test.html", open("test_data/test.html").read())

        self.assertEquals(len(existence.URL_CACHE), 3)

    def test_parse_html_urls_ignores_urls_hash_or_mailto(self):
        existence.parse_html_urls("test.html", open("test_data/test.html").read())

        # Would be more total links if it doesn't ignore these two:
        #     <a href="#">should be ignored</a>
        #     <a href="mailto:eric@email">should be ignored</a>
        self.assertEquals(len(existence.URL_CACHE), 3)

    def test_parse_html_urls_cleans_up_local_windows_urls(self):
        windows_link = '<a href="C:\Users\Eric\Downloads\\funny_picture.jpg">a hilarious picture</a>';
        urls = existence.parse_html_urls("test.html", windows_link)

        # <a href="C:\Users\Eric\Downloads\funny_picture.jpg">a hilarious picture</a>
        self.assertEquals(urls[0][0], 'file:///C:/Users\\Eric\\Downloads\\funny_picture.jpg')


class TestVerifyingURLsExist(ExistenceTest):
    def test_scan_directory_for_bad_urls_works(self):
        broken_urls = existence.scan_directory_for_bad_urls("test_data")

        self.assertEquals(broken_urls[0][0], 'http://this-domain-name-doesnt-exist-no-way')
