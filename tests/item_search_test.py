import json
import unittest
from keanu.app import flask_app


class TestItemRoute(unittest.TestCase):

    def setUp(self):
        """
        Setup app for testing
        :return:
        """
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        """
        Remove app after testing
        :return:
        """
        self.app.delete()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_search_two_chars(self):
        result = self.app.get('/item/search', query_string={'q': 'tu'})
        json_data = json.loads(result.data)['data']['items']
        self.assertIsNotNone(json_data, 'no search results returned')

    def test_search_tags(self):
        result = self.app.get('/item/search', query_string={'q': 'chicken'})
        json_data = json.loads(result.data)['data']['items']
        self.assertIsNotNone(json_data, 'no search results returned')

    def test_no_search_results(self):
        result = self.app.get('/item/search', query_string={'q': '1231123'})
        json_data = json.loads(result.data)['data']['items']
        self.assertTrue(len(json_data) == 0, 'Search results returned when it shouldn\'t')
