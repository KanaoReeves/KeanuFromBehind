from flask import Blueprint, jsonify
from flask_autodoc import Autodoc

login_api = Blueprint('login_api', __name__)
from ..app import flask_app
auto = Autodoc(flask_app)


@login_api.route('/login/spc')
def login_doc():
    return auto.html()


@login_api.route('/login')
@auto.doc()
def login() -> dict:
    """
    Login to the api
    :return:
    """
    return jsonify({'data': {'success': True}})
