import unittest

from keanu.app import flask_app


class TestItems(unittest.TestCase):

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

    def test_add_new_item(self):
        new_item = Items(
            id='8888',
            name='Test Item',
            description='This is just a test description',
            price=9.99,
            calories=500,
            category='Entrees',
            tags=['bread', 'healthy']
        )


        new_item.save()
        found_item = Items.query.filter(Items.id == new_item.id).first()
        self.assertEqual(new_item.id, found_item.id, "Items not equal")
        new_item.remove()
