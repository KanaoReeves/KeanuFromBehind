#!/usr/bin/env python
import jwt
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, request
from flask_autodoc import Autodoc

login_api = Blueprint('loginApi', __name__)

auto = Autodoc()


@login_api.route('/login/spec', strict_slashes=False)
def login_doc():
    """
    Documentation for the /login route
    :return:
    """
    return auto.html()


@login_api.route('/login/register', strict_slashes=False, methods=['POST'])
@auto.doc()
def register() -> tuple:
    """
    Register a new user
    :return:
    """
    # import here because of circular reference
    from keanu.models.users import User, UserFullName, PaymentInfo, Address
    if request.json is not None:
        new_user = User(
            username=request.json['username'],
            password=generate_password_hash(request.json['password']),
            displayName=UserFullName(
                firstName=request.json['displayName']['firstName'],
                lastName=request.json['displayName']['lastName']
            ),
            email=request.json['email'],
            adminRights=request.json['adminRights'],
            paymentInfo=PaymentInfo(
                name=request.json['paymentInfo']['name'],
                cardType=request.json['paymentInfo']['cardType'],
                num=int(request.json['paymentInfo']['num']),
                expiry=datetime.datetime.strptime(request.json['paymentInfo']['expiry'],
                                                  "%w/%m/%y %I:%M:%S %p UTC")
            ),
            address=Address(
                number=int(request.json['address']['number']),
                name=request.json['address']['name'],
                streetType=request.json['address']['streetType'],
                postalCode=request.json['address']['postalCode']
            )
        )
        new_user.save()
        return jsonify({'data': {'user': request.json}})
    else:
        return jsonify({'error': 'no username or password provided'}), 401


@login_api.route('/login', strict_slashes=False, methods=['POST'])
@auto.doc()
def login() -> tuple:
    """
    Login to the api
    Pass in the username and password in the header
    A token is returned
    {"data": {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE0ODkxODUyMjAsInNvbWVQY"}}
    :return: token
    """
    # import here because of circular reference
    from keanu.models.users import User
    if ('username' in request.headers) and ('password' in request.headers):
        username = request.headers['username']
        password = request.headers['password']
    else:
        return jsonify({'error': 'no username or password provided'}), 403

    # find user from database
    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify({'error': 'wrong username or password'}), 403
    else:
        # verify password
        if not check_password_hash(user.password, password):
            return jsonify({'error': 'wrong username or password'}), 403

    # generate a new token for the user for 1 week
    jwt_token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
        'user_id': str(user.mongo_id)},
        'secret', algorithm='HS512')

    user.token = jwt_token.decode("utf-8")
    user.save()

    return jsonify(
        {
            'data': {
                'token': jwt_token.decode("utf-8"),
                'adminRights': user.adminRights
            }
        }
    )
