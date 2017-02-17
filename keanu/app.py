from flask import Flask, jsonify
from flask_autodoc import Autodoc

from keanu.routes.login import login_api

flask_app = Flask(__name__)
auto = Autodoc(flask_app)

flask_app.register_blueprint(login_api)


@flask_app.route('/')
def applol():
    return jsonify({'data': 'success'})


@flask_app.route('/spec')
def spec():
    return auto.html()

if __name__ == "__main__":
    flask_app.run(debug=True)
