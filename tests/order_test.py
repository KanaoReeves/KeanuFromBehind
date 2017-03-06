import unittest

from keanu.app import flask_app
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
        new_order = Orders(
            id='8888',
            items=[123, 25, 33],
            total=29.99,
            userId=500,
            date=datetime.now()
        )

        new_order.save()
        found_order = Orders.query.filter(Orders.id == new_order.id).first()
        self.assertEqual(new_order.id, found_order.id, "Order is not equal")
        new_order.remove()
