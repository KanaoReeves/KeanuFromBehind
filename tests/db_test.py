import unittest, json
from keanu.app import flask_app, flask_db as db
from keanu.models.users import User, UserFullName, PaymentInfo, Address
import datetime


class TestDB(unittest.TestCase):

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

    def test_add_new_user(self):
        new_user = User(
            username='aaron',
            password='password',
            displayName=UserFullName(firstName='Aaron', lastName='Smith'),
            email='aaron@example.com',
            adminRights=False,
            paymentInfo=PaymentInfo(
               name='Aaron Smith',
               cardType='VISA',
               num=451535486,
               expiry=datetime.datetime(2017, 1, 1)
            ),
            address=Address(
               number=123,
               name='Main',
               streetType='Boulevard',
               postalCode='M3E5R1'
            )
        )

        new_user.save()
        found_user = User.query.filter(User.email == new_user.email).first()
        self.assertEqual(new_user.email, found_user.email, "User emails not equal")
        new_user.remove()
