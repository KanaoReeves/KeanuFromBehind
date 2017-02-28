#!/usr/bin/env python
from flask import Flask, jsonify
from flask_mongoalchemy import MongoAlchemy
from flask_autodoc import Autodoc
from keanu.routes.login import login_api

flask_app = Flask(__name__)
flask_app.config['MONGOALCHEMY_CONNECTION_STRING'] = os.getenv('DBURI', 'mongodb://localhost/kanaoreeves')
flask_app.config['MONGOALCHEMY_DATABASE'] = 'kanaoreeves'
flask_app.config['MONGOALCHEMY_SAFE_SESSION'] = True
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


if __name__ == "__main__":
    flask_app.run(debug=True)
