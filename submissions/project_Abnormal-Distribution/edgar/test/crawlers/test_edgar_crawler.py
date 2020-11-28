from unittest import TestCase
from mock import patch

from edgar.crawlers.edgar_crawler import edgar_crawler, BASE_URL, DAILY_ARCHIVE_EXTENSION


def mock_requests(*args, **kwargs):

    class MockResponse:
        """Mock SEC daily archive listing"""

        def __init__(self):
            self.text = (
                '<tr><td><a href="not_a_daily_archive.htm">not_a_daily_archive.html</a></td></tr>'
                f'<tr><td><a href="archive0.{DAILY_ARCHIVE_EXTENSION}">archive0</a></td></tr>'
                f'<tr><td><a href="archive1.{DAILY_ARCHIVE_EXTENSION}">archive1</a></td></tr>'
            )

    return MockResponse()


class TestEdgarCrawler(TestCase):

    @patch('edgar.crawlers.edgar_crawler.requests.get', side_effect=mock_requests)
    def test_edgar_crawler(self, mock_request):
        """Test the EDGAR crawler, mocking out requests.get with a mock directory listing"""

        daily_archive_urls = edgar_crawler(year=[2018, 2019], quarter=1)

        # Test that the daily archives in the (mock) GET response are scraped
        for url in [
            f'{BASE_URL}/2018/QTR1/archive0.{DAILY_ARCHIVE_EXTENSION}',
            f'{BASE_URL}/2018/QTR1/archive1.{DAILY_ARCHIVE_EXTENSION}',
            f'{BASE_URL}/2019/QTR1/archive0.{DAILY_ARCHIVE_EXTENSION}',
            f'{BASE_URL}/2019/QTR1/archive1.{DAILY_ARCHIVE_EXTENSION}',
        ]:
            self.assertIn(url, daily_archive_urls)

        # Test that the other URLs in the (mock) GET response are ignored
        for url in [
            f'{BASE_URL}/2018/QTR1/not_a_daily_archive.htm',
            f'{BASE_URL}/2019/QTR1/not_a_daily_archive.htm',
        ]:
            self.assertNotIn(url, daily_archive_urls)
