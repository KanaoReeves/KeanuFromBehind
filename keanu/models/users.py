from keanu.app import flask_db as db
from mongoalchemy.document import Index


class PaymentInfo(db.Document):
    name = db.StringField(required=True)  # Name on Credit Card
    cardType = db.EnumField(db.StringField(), 'VISA', 'MASTERCARD', 'AMEX')
    num = db.IntField(required=True)  # Credit Card Number
    cvNum = db.IntField(required=False)  # CVV Number on back of credit card
    expiry = db.DateTimeField(required=False)


class UserFullName(db.Document):
    firstName = db.StringField(required=True)
    lastName = db.StringField(required=True)


class Address(db.Document):
    number = db.IntField(required=True)
    name = db.StringField(required=True)
    streetType = db.StringField(required=True)
    postalCode = db.StringField(required=True)


class User(db.Document):
    config_collection_name = 'users'

    username = db.StringField(required=True)
    password = db.StringField(required=True)
    token = db.StringField(required=False)
    displayName = db.DocumentField(UserFullName)
    email = db.StringField(required=True)
    email_index = Index().ascending('email').unique()
    adminRights = db.BoolField(required=True)
    paymentInfo = db.DocumentField(PaymentInfo)
    address = db.DocumentField(Address)


class Order(db.Document):
    id = db.IntField(required=True)
    items = db.StringField(required=True)
    total = db.DecimalField
    userId = db.IntField(required=True)
    date = db.DateTimeField(required=True)


class Tags(db.Document):
    id = db.IntField(required=True)
    tag = db.StringField(required=True)


class Items(db.Document):
    id = db.IntField(required=True)
    name = db.StringField(required=True)
    description = db.StringField(max_length=150, required=True)
    price = db.DecimalField(required=True)
    calories = db.IntField(required=True)
    category = db.StringField(required=True)
    tags = db.DocumentField(Tags)
