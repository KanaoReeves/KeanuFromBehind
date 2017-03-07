#!/usr/bin/env python
import json
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc

order_api = Blueprint('orderApi', __name__)

auto = Autodoc()

from keanu.models.orders import Order

@order_api.route('/order/spec')
def login_doc():
    """
    Documentation for the /order route
    :return:
    """
    return auto.html()


@order_api.route('/order', methods=['GET'])
@auto.doc()
def get_all_orders() -> dict:
    """
    returns all the orders for user as a json array
    :return:
    """
    from keanu.models.users import User
    # get all orders
    orders = Order.query.filter(User.request.headers['_id'])
    # create orders list
    orders_list = []
    # create response
    for order in orders:
        orders_list.append({
            "_id": str(order.mongo_id),
            "items": order.items,
            "total" : order.total,
            "userId": order.userId,
            "date": order.date
        })
    return jsonify({'data': {'orders': orders_list}})


@order_api.route('/order/add', methods=['POST'])
@auto.doc()
def add_order(order) -> None:

    # find specific item
    new_order = Order(
            items= order.items,
            total= order.total,
            userId= order.userId,
            date= order.date
    )
    new_order.save()
