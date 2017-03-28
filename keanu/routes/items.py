#!/usr/bin/env python
from flask import Blueprint, jsonify, request, g
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


@item_api.route('/admin/item/add', methods=['POST'])
@auto.doc()
def add_new_item() -> tuple:
    from keanu.models.items import Item
    if request.json is not None and g.is_admin:
        new_item = Item(
            name=request.json['name'],
            description=request.json['description'],
            imageURL=request.json['imageURL'],
            price=request.json['price'],
            calories=request.json['calories'],
            category=request.json['category'],
            tags=request.json['tags']
        )
        new_item.save()

        return jsonify({'data': {'item': request.json, 'itemId': str(new_item.mongo_id)}})
    else:
        return jsonify({'error': 'invalid item' + request.json}), 403


@item_api.route('/admin/item/delete/<item_id>', methods=['POST'])
@auto.doc()
def delete_item(item_id):
    from keanu.models.items import Item
    # search for item by id
    item = Item.query.get(str(item_id))
    if item is not None and g.is_admin:
        # remove item
        item.remove()
        return jsonify({'data': {'success': True}})
    else:
        return jsonify({'error': 'No item found with id ' + item_id})


@item_api.route('/admin/item/update', methods=['POST'])
@auto.doc()
def update_item():
    from keanu.models.items import Item

    if request.json is not None:
        item_update = Item.query.get(request.json['_id'])
        item_update.calories = request.json['calories']
        item_update.category = request.json['category']
        item_update.description = request.json['description']
        item_update.imageURL = request.json['imageURL']
        item_update.name = request.json['name']
        item_update.price = request.json['price']
        item_update.tags = request.json['tags']

        item_update.save()

        item = {
            '_id': item_update.mongo_id,
            'name': item_update.name,
            'description': item_update.description,
            'imageURL': item_update.imageURL,
            'price': item_update.price,
            'calories': item_update.calories,
            'category': item_update.category
        }

        return jsonify({'data': {'message': 'Updated with item id: ' + str(item_update.mongo_id),
                                 'mongo_id': str(item_update.mongo_id)}
                        })
    else:
        return jsonify({'error': 'item not updated'})
