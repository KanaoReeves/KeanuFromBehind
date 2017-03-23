import unittest
import json
from keanu.app import flask_app


class TestCustomerInfo(unittest.TestCase):
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

    def login(self):
        login_result = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        return json.loads(login_result.data)['data']['token']

    def test_get_customer_payment_info(self):
        token = self.login()
        result = self.app.get('/customer/payment', headers={'token': token})
        json_data = json.loads(result.data)
        self.assertTrue(json_data['data']['paymentInfo'] is not None, 'no payment info')
