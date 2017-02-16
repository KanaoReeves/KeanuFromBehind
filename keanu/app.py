from flask import Flask, jsonify
from keanu.routes import login
from flask_autodoc import Autodoc

flask_app = Flask(__name__)
auto = Autodoc(flask_app)

flask_app.register_blueprint(login.login_api)


@flask_app.route('/spec')
def spec():
    return auto.html()


@flask_app.route('/test')
def applol():
    return jsonify({'data': 'success'})

if __name__ == "__main__":
    flask_app.run(debug=True)
