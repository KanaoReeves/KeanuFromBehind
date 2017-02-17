from flask import Blueprint, jsonify

customer_api = Blueprint('customer_api', __name__)

@customer_api.route('/customer')
def customer() -> dict:
    """
    """
    return jsonify({})
