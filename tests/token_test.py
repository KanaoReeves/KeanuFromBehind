import unittest
import json
from keanu.app import flask_app


class TestToken(unittest.TestCase):
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

    def no_token_error(self):
        result = self.app.post('/url-not-in-approved-no-auth-list')
        json_response = json.loads(result.data)
        self.assertEqual(json_response['error'], 'not a valid token', 'incorrect error given')
        self.assertEqual(result.status, 401, 'error code not equal 401')
