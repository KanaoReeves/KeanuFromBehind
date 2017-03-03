#!/usr/bin/env python
import jwt, datetime
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc


login_api = Blueprint('loginApi', __name__)

auto = Autodoc()


@login_api.route('/login/spec')
def login_doc():
    return auto.html()


@login_api.route('/login', methods=['POST'])
@auto.doc()
def login() -> dict:
    """
    Login to the api
    :return:
    """
    # Import user here to avoid circular input
    from keanu.models.users import User, Address, PaymentInfo, UserFullName
    username: str = request.headers['username']
    password: str = request.headers['password']
    user = User.query.filter(User.username == username, User.password == password).first()

    return jsonify({'data': {'success': True}})
