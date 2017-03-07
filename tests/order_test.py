import unittest
import json

from keanu.app import flask_app


class TestOrderRoute(unittest.TestCase):

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

    def test_get_user_orders(self):
        result = self.app.get('/order')
        json_data = json.loads(result.data)
        self.assertTrue(len(json_data['data']['orders']) > 1, 'no orders in db')
