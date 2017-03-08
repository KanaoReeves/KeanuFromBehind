from keanu.app import flask_db as db


class Order(db.Document):
    config_collection_name = 'orders'

    items = db.ListField(db.IntField(),required=True)
    total = db.FloatField(required=True)
    userId = db.StringField(required=True)
    date = db.DateTimeField(required=True)

