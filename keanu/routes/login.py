#!/usr/bin/env python
import jwt
import datetime
import json
from jwt.algorithms import ECAlgorithm
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc

login_api = Blueprint('loginApi', __name__)

auto = Autodoc()

# import User model here to avoid circular imports
from keanu.models.users import User
#


@login_api.route('/login/spec')
def login_doc():
    """
    Documentation for the /login route
    :return:
    """
    return auto.html()


@login_api.route('/login/register', methods=['POST'])
@auto.doc()
def register() -> dict:
    """
    Register a new user!
    :return:
    """
    username = request.headers['username']
    password = request.headers['password']
    return jsonify(jsonify({'data': {'success': True}}))


@login_api.route('/login', methods=['POST'])
@auto.doc()
def login() -> dict:
    """
    Login to the api
    Pass in the username and password in the header
    A token is returned
    {"data": {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE0ODkxODUyMjAsInNvbWVQY"}}
    :return: token
    """

    username = request.headers['username']
    password = request.headers['password']

    # find user from database
    user =  User.query.filter(User.username == username, User.password == password).first()

    # generate a new token for the user for 1 week
    jwt_token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
        'somePayload': 'wowwww'},
        'secret', algorithm='HS512')

    user.token = jwt_token.decode("utf-8")
    user.save()

    return jsonify({'data': {'token': jwt_token.decode("utf-8")}})
