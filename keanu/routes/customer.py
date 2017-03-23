from flask import Blueprint, jsonify, g
from flask_autodoc import Autodoc

customer_api = Blueprint('customer_api', __name__)

auto = Autodoc()


@customer_api.route('/customer/spec')
@auto.doc()
def customer_doc():
    """
    Documentation for customer
    info page
    """
    return auto.html()


@customer_api.route('/customer/payment', methods=['GET'])
@auto.doc()
def customer_payment_info() -> dict:
    """
    Gets a customers payment info
    """
    from keanu.models.users import User
    user = User.query.get(g.user_id)
    payment_info = user.paymentInfo

    return jsonify({
        'data': {
            'paymentInfo':
                {
                    'name': payment_info.name,
                    'cardType': payment_info.cardType,
                    'num': payment_info.num,
                    'expiry': payment_info.expiry
                }
        }
    })
