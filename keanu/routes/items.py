#!/usr/bin/env python
import json
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc

item_api = Blueprint('itemApi', __name__)

auto = Autodoc()


@item_api.route('/item/spec')
def login_doc():
    """
    Documentation for the /item route
    :return:
    """
    return auto.html()


@item_api.route('/item', methods=['GET'])
@auto.doc()
def get_all_items() -> dict:
    """
    returns all the items as a json array
    :return:
    """
    from keanu.models.items import Item
    # get all items
    items = Item.query.all()
    # create items list
    items_list = []
    # create response
    for item in items:
        items_list.append({
            "_id": str(item.mongo_id),
            "name": item.name,
            "description": item.description,
            "imageURL": item.imageURL,
            "price": item.price,
            "calories": item.calories,
            "category": item.category,
            "tags": item.tags
        })
    return jsonify({'data': {'items': items_list}})


@item_api.route('/item/id/<id>', methods=['GET'])
@auto.doc()
def get_item_by_id(id) -> tuple:
    from keanu.models.items import Item
    # find specific item
    item = Item.query.filter(Item.mongo_id == id).first()
    item_json = {
        "_id": str(item.mongo_id),
        "name": item.name,
        "description": item.description,
        "imageURL": item.imageURL,
        "price": item.price,
        "calories": item.calories,
        "category": item.category,
        "tags": item.tags
    }
    return jsonify({'data': {'item': item_json}})


@item_api.route('/item/category/<category>', methods=['GET'])
@auto.doc()
def get_item_by_category(category) -> tuple:
    from keanu.models.items import Item
    # find items by category
    items = Item.query.filter(Item.category == category)
    # create items list
    items_list = []
    # create response
    for item in items:
        items_list.append({
            "_id": str(item.mongo_id),
            "name": item.name,
            "description": item.description,
            "imageURL": item.imageURL,
            "price": item.price,
            "calories": item.calories,
            "category": item.category,
            "tags": item.tags
        })
    return jsonify({'data': {'items': items_list}})
