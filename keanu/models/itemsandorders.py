from keanu.app import flask_db as db
from mongoalchemy.document import Index


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
    tags = db.ListField(Tags, required=True)