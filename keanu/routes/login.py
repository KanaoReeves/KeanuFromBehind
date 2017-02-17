from flask import Blueprint, jsonify

login_api = Blueprint('login_api', __name__)


@login_api.route('/login')
def login() -> dict:
    """
    Login to the api
    :return:
    """
    return jsonify({'data': {'success': True}})
