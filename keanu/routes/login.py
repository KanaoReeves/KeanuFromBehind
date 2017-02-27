#!/usr/bin/env python
from flask import Blueprint, jsonify
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
    # TODO: Connect to db and verify user
    return jsonify({'data': {'success': True}})
