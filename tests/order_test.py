import unittest
import json

from keanu.app import flask_app
from keanu.models.orders import Order


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

    def test_add_new_order(self):
        login = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        json_login = json.loads(login.data)
        data = '{"date": "12:05:2017","delivery": true,"items": [' \
               '{"58cb056f98717507c730d78b": 5},{"58cb0577630cc007c7870772": 2},' \
               '{"58d13f3e63ae2507c70a7d5e": 1}' \
               '],"price": 25.06}'

        result = self.app.post('/order/add/', headers={'token': json_login['data']['token']}, data=data, content_type='application/json')
        json_response = json.loads(result.data)
        self.assertIsNotNone(json_response['data']['orderId'], 'error in response')
        added_order = Order.query.get(json_response['data']['orderId'])
        added_order.remove()

    def test_get_user_orders(self):
        login = self.app.post('/login', headers={'username': 'steve', 'password': 'smith'})
        json_response = json.loads(login.data)['data']['token']
        self.assertIsNotNone(json_response)
        result = self.app.get('/order', headers={'token': json_response})
        json_data = json.loads(result.data)
        self.assertIsNotNone(len(json_data), 'no orders in db')
