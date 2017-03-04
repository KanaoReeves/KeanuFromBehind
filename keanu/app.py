#!/usr/bin/env python
import os
from flask import Flask, jsonify, request
from flask_mongoalchemy import MongoAlchemy
from flask_autodoc import Autodoc
from keanu.routes.login import login_api

flask_app = Flask(__name__)
flask_app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.getenv('DBURI', 'mongodb://localhost/kanaoreeves')
flask_app.config['MONGOALCHEMY_DATABASE'] = 'kanaoreeves'
flask_db = MongoAlchemy(flask_app)

flask_app.register_blueprint(login_api)
auto = Autodoc(flask_app)


@flask_app.route('/spec', methods=['GET'])
def spec():
    """
    Spec for root endpoints
    :return:
    """
    return auto.html()


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
    :param error:
    :return:
    """
    err_string = 'Route not found: '+request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string}), 404


@flask_app.errorhandler(400)
def handel400(error):
    err_string = str(error) + ' ' + request.path
    flask_app.logger.error(err_string)
    return jsonify({'error': err_string}), 400

if __name__ == "__main__":
    flask_app.run(debug=True)
