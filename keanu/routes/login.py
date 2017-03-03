#!/usr/bin/env python
from flask import Blueprint, jsonify
from flask_autodoc import Autodoc
# from keanu.models.users import User
#import keanu.models.users as users

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
    from keanu.models.users import User
    # TODO: Connect to db and verify user
    return jsonify({'data': {'success': True}})
