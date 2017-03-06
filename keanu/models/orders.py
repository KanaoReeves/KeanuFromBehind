from keanu.app import flask_db as db
from mongoalchemy.document import Index


class Order(db.Document):
    config_collection_name = 'orders'

    items = db.ListField(db.IntField(),required=True)
    total = db.FloatField(required=True)
    userId = db.IntField(required=True)
    date = db.DateTimeField(required=True)

