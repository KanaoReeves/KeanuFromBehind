#!/usr/bin/env python
import json
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc
from keanu.routes.login import login_api

order_api = Blueprint('orderApi', __name__)

auto = Autodoc()


@order_api.route('/order/spec')
def order_doc():
    """
    Documentation for the /order route
    :return:
    """
    return auto.html()


@order_api.route('/order', methods=['GET'])
@auto.doc()
def get_user_orders() -> dict:
    """
    returns all the orders for user as a json array
    :return:
    """
    from keanu.models.orders import Order
    #from keanu.models.users import User
    # get all orders
    if ('_Id' in request.headers) :
        id = request.headers['_id']
        orders = Order.query.filter(id)
        # create orders list
        orders_list = []
        # create response
        for order in orders:
            orders_list.append({
                "_id": str(order.mongo_id),
                "items": order.items,
                "total": order.total,
                "userId": order.userId,
                "date": order.date
            })
        return jsonify({'data': {'orders': orders_list}})

    else:
        return jsonify({'error': 'user not signed in'}), 401



@order_api.route('/order/add', methods=['POST'])
@auto.doc()
def add_order() -> tuple:

    if request.json is not None:
        # find specific item
        new_order = Order(
                items= request.json['items'],
                total= request.json['total'],
                userId= request.json['userId'],
                date= request.json['date']
        )
        new_order.save()
        return jsonify({'data': {'order': request.json}})
    else:
        return jsonify({'error': 'no order placed'}), 401
