import unittest
import feedparser
from news import URL_1, URL_2, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9, URL_10, URL_11

class TestNewsFeedURLs(unittest.TestCase):
    def setUp(self):
        self.urls = [
            URL_1, URL_2, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9, URL_10, URL_11
        ]

    def test_feeds_return_valid_xml(self):
        for url in self.urls:
            with self.subTest(url=url):
                feed = feedparser.parse(url)
                self.assertEqual(feed.bozo, 0, f"Feed at {url} is not valid XML or could not be parsed.")
                self.assertTrue(
                    hasattr(feed, 'entries') and len(feed.entries) > 0,
                    f"Feed at {url} returned no entries."
                )

if __name__ == "__main__":
    unittest.main()
