from keanu.app import flask_db as db
from mongoalchemy.document import Index


class Orders(db.Document):
    id = db.IntField(required=True)
    items = db.ListField(required=True)
    total = db.DecimalField
    userId = db.IntField(required=True)
    date = db.DateTimeField(required=True)

