from keanu.app import flask_db as db


class PaymentInfo(db.Document):
    name = db.StringField(required=True)  # Name on Credit Card
    num = db.IntField(required=True)  # Credit Card Number
    cvNum = db.IntField(required=True)  # CVV Number on back of credit card
    expiry = db.DateTimeField(required=True)


class UserFullName(db.Document):
    firstName = db.StringField(required=True)
    lastName = db.StringField(required=True)


class Address(db.Document):
    name = db.StringField(required=True)
    number = db.IntField(required=True)
    postalCode = db.StringField(required=True)


class Users(db.Document):
    username = db.StringField(required=True).unique()
    password = db.StringField(required=True)
    displayName = db.DocumentField(UserFullName, required=True)
    email = db.StringField(required=True)
    adminRights = db.BoolField(required=True)
    paymentInfo = db.DocumentField(PaymentInfo, required=True)
    address = db.Document(Address, required=True)






    # description = db.StringField()
    # catogery = db.StringField()
    # tag = db.ListField(db.StringField())