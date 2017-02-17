from flask import Flask, jsonify
from keanu.routes import login

flask_app = Flask(__name__)

# flask_app.register_blueprint(spec_api)
flask_app.register_blueprint(login.login_api)


@flask_app.route('/spec')
def spec():
    return jsonify({})

if __name__ == "__main__":
    flask_app.run(debug=True)
