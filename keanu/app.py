#!/usr/bin/env python
import os
from flask import Flask, jsonify, request
from flask_mongoalchemy import MongoAlchemy
from flask_autodoc import Autodoc
from keanu.routes.login import login_api
from keanu.routes.items import item_api

flask_app = Flask(__name__)
flask_app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.getenv('DBURI', 'mongodb://localhost/kanaoreeves')
flask_app.config['MONGOALCHEMY_DATABASE'] = 'kanaoreeves'
flask_db = MongoAlchemy(flask_app)

flask_app.register_blueprint(login_api)
flask_app.register_blueprint(item_api)
auto = Autodoc(flask_app)


@flask_app.route('/spec', methods=['GET'])
def spec():
    """
    Spec for root endpoints
    :return:
    """
    return auto.html()


@flask_app.before_request
def before_request() -> tuple:
    """
    Checks if a token header in requests
    :return:
    """
    from keanu.models.users import User
    no_auth_paths = ['/', '/spec', '/favicon.ico', '/item', '/item/58be0265f188127b8fd2af52', '/login', '/login/register']
    if request.path not in no_auth_paths and 'token' in request.headers:
        token = request.headers['token']
        user = User.query.filter(User.token == token).first()
        if user is None:
            return jsonify({'error': 'not a valid token'}), 401


@flask_app.route('/', methods=['GET'])
@auto.doc()
def root():
    """
    Root api to test if its working
    :return:
    """
    return jsonify({'data': {'success': True}})


@flask_app.errorhandler(404)
def handel404(error):
    """
    Method to handle 404 error
    :return:
    """
    err_string = 'Route not found: '+request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string+' '+error}), 404


@flask_app.errorhandler(400)
def handel400(error):
    err_string = str(error) + ' ' + request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string}), 400


@flask_app.errorhandler(500)
def handel500(error):
    flask_app.logger.error(error)
    return jsonify({'error': error}), 500


if __name__ == "__main__":
    flask_app.run(debug=True)
