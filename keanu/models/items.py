from keanu.app import flask_db as db


class Item(db.Document):
    config_collection_name = 'items'

    name = db.StringField(required=True)
    description = db.StringField(max_length=150, required=True)
    imageURL = db.StringField(required=True)
    price = db.FloatField(required=True)
    calories = db.IntField(required=True)
    category = db.StringField(required=True)
    tags = db.ListField(db.StringField(), required=True)
