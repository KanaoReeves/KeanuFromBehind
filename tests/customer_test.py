import unittest
import json
from flask import g
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

    def test_get_user_info(self):
        #data = '{"address": {"name": "Main", "number": 123, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
        #      '"adminRights": false, "displayName": {"firstName": "Aaron", "lastName": "Smith"}, ' \
        #     '"email": "example@example.com", "password": "smith", "paymentInfo": {"cardType": "VISA", ' \
        #    '"expiry": "1/1/17 12:00:00 AM UTC", "name": "steve Smith", "num": 451535486}, "username": "steve"}'
        token = self.login()
        result = self.app.get('/customer/profile', headers={'token': token})
        #json_data = json.loads(result.data)
        self.assertIsNotNone(result,  'No user info')

    def test_user_profile_update(self):
        from keanu.models.users import User

        #creating new user
        data = '{"address": {"name": "Queen", "number": 155, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Jane", "lastName": "Doe"}, ' \
               '"email": "example69@example.com", "password": "password", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "Jane Doe", "num": 451535486}, "username": "Jane"}'
        reg_result = self.app.post('/login/register', data=data, content_type='application/json')
        #login to get token
        login_result = self.app.post('/login', headers={'username': 'Jane', 'password': 'password'})
        json_response = json.loads(login_result.data)['data']['token']
        self.assertIsNotNone(json_response)
        #update user info
        updated_data = '{"address": {"name": "Baker", "number": 221, "postalCode": "M3E5R1", "streetType": "Street"}, ' \
               '"adminRights": false, "displayName": {"firstName": "Jane", "lastName": "Doe"}, ' \
               '"email": "example@example.com", "password": "password", "paymentInfo": {"cardType": "VISA", ' \
               '"expiry": "1/1/17 12:00:00 AM UTC", "name": "Jane Doe", "num": 451535486}, "username": "Jane"}'

        result = self.app.post('/customer/profile/edit', data = updated_data,  headers={'token': json_response})
        json_data = json.loads(result.data)
        self.assertIsNotNone(len(json_data))
        user = User.query.filter(User.token == json_response).first()
        user.remove()



