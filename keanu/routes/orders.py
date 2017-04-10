#!/usr/bin/env python
import json
import requests
from datetime import datetime
from flask import Blueprint, jsonify, request, g
from flask_autodoc import Autodoc

order_api = Blueprint('orderApi', __name__)

auto = Autodoc()


@order_api.route('/order/spec', strict_slashes=False)
def order_doc():
    """
    Documentation for the /order route
    :return:
    """
    return auto.html()


@order_api.route('/order', strict_slashes=False, methods=['GET'])
@auto.doc()
def get_user_orders() -> dict:
    """
    returns all the orders for user as a json array
    :return:
    """
    from keanu.models.orders import Order

    # get all orders
    orders = Order.query.filter(Order.userId == str(g.user_id)).all()  # create orders list
    orders_list = []
    # create response
    for order in orders:
        items_list = []
        for item in order.items:
            items_list.append({'itemId': item.itemId, 'quantity': item.quantity})
        orders_list.append({
            "_id": str(order.mongo_id),
            "items": items_list,
            "total": str(order.total),
            "delivery": str(order.delivery),
            "date": datetime.strptime(order.date, '%d:%m:%Y')
        })

    orders_list.sort(key=lambda o: o['date'], reverse=True)
    return jsonify({'data': {'orders': orders_list}})


@order_api.route('/order/add', strict_slashes=False, methods=['POST'])
@auto.doc()
def add_order() -> tuple:
    """
    Adds a new order to the database 
    :return: 
    """
    from keanu.models.orders import Order, ItemQuantity

    if request.json is not None:
        # find specific item
        items = []

        for item in request.json['items']:
            key, value = item.popitem()
            items.append(ItemQuantity(itemId=key, quantity=value))

        new_order = Order(
            items=items,
            total=request.json['price'],
            userId=str(g.user_id),
            delivery=request.json['delivery'],
            date=request.json['date']
        )
        new_order.save()
        if 'pushUserId' in request.json:
            send_notification(request.json['pushUserId'])
        # returns a message
        return jsonify({'data': {
            'message': 'order added with id ' + str(new_order.mongo_id),
            'orderId': str(new_order.mongo_id)
            }
        })
    else:
        return jsonify({'error': 'no order placed'}), 401


def send_notification(push_user_id: str):
    """
    Sends a push notification to the user
    :param push_user_id: 
    :return: 
    """
    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic ZmI2ZTQ2OGQtMTkxMC00OGFhLTkxODItNGY0NTI4M2U5ZDhl"}
    body = {
        "app_id": "0c73a76c-be9a-4c17-ab9e-0ad31cbaa349",
        "include_player_ids": [push_user_id],
        "contents": {"en": "Your order is now being processed"}
    }
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(body))
    print(req.status_code, req.reason)
