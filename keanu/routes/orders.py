#!/usr/bin/env python
import json
from flask import Blueprint, jsonify, request, g
from flask_autodoc import Autodoc


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

    # get all orders
    orders = Order.query.filter(Order.userId == str(g.user_id)).all()  # create orders list
    orders_list = []
    # create response
    for order in orders:
        orders_list.append({
            "_id": str(order.mongo_id),
            "items": str(json.dumps(order.items)),
            "total": str(order.total),
            "userId": str(order.userId),
            "delivery": str(order.delivery),
            "date": order.date
        })
    return jsonify({'data': {'orders': orders_list}})


@order_api.route('/order/add', methods=['POST'])
@auto.doc()
def add_order() -> tuple:
    from keanu.models.orders import Order

    if request.json is not None:
        # find specific item
        new_order = Order(
            items=request.json['items'],
            total=float(request.json['total']),
            userId=str(g.user_id),
            delivery=bool(request.json['delivery']),
            date=float(request.json['date'])
        )
        new_order.save()
        return jsonify({'data': {'orders': request.json}})
    else:
        return jsonify({'error': 'no order placed'}), 401