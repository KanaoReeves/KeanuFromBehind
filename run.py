import os
from keanu.app import flask_app
port = int(os.environ.get('PORT', 5000))
flask_app.run(host='0.0.0.0', port=port)
