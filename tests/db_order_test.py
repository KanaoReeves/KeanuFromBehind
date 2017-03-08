import unittest

from keanu.app import flask_app
from keanu.models.orders import Order
import datetime


class TestOrders(unittest.TestCase):

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
        new_order = Order(
            items=[123, 25, 33],
            total=29.99,
            userId='58bda399c2e2222840edddb2',
            date=datetime.datetime.now()
        )

        new_order.save()
        found_order = Order.query.filter(Order.userId == new_order.userId).first()
        self.assertEqual(new_order.items, found_order.items, "Order is not equal")
        new_order.remove()
