from keanu.app import flask_db as db


class ItemQuantity(db.Document):
    itemId = db.StringField(required=True)
    quantity = db.IntField(required=True)


class Order(db.Document):
    config_collection_name = 'orders'

    items = db.ListField(db.DocumentField(ItemQuantity), required=True)
    total = db.FloatField(required=True)
    userId = db.StringField(required=True)
    delivery = db.BoolField(required=True)
    date = db.StringField(required=True)
