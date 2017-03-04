import unittest

import json
from keanu.app import flask_app


class TestLogin(unittest.TestCase):
    def setUp(self):
        """
        Setup app for testing
        :return:
        """
        self.app = flask_app.test_client()
        self.app.testing = True

    def tearDown(self):
        self.app.delete()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_login_token(self):
        result = self.app.post('/login', headers={'username': 'aaron', 'password': 'password'})
        json_response = json.loads(result.data)
        self.assertTrue(json_response['data']['token'] is not None, 'error with json '+json_response)

    def test_register_new_users(self):
        data = '{"address": {"name": "Main", "number": 123, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Aaron", "lastName": "Smith"}, ' \
               '"email": "example@example.com", "password": "smith", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "steve Smith", "num": 451535486}, "username": "steve"}'
        result = self.app.post('/login/register', data=data, content_type='application/json')
        json_response = json.loads(result.data)
        self.assertEqual(json.dumps(json_response['data']['user']), data, 'data returned is not the same')
