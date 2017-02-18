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
