from flask import Blueprint, jsonify, g, request
from flask_autodoc import Autodoc
import datetime

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

@customer_api.route('/customer/profile', methods=['GET'])
@auto.doc()
def customer_profile_info() -> dict:
    """
    Gets a customers profile info
    :return:
    """
    from keanu.models.users import User
    user = User.query.get(g.user_id)

    return jsonify(user)

@customer_api.route('customer/profile/edit', methods=['POST'])
@auto.doc()
def customer_profile_update() -> dict:
    from keanu.models.users import User

    if request.json is not None:

        from keanu.models.users import User, UserFullName, PaymentInfo, Address
        if request.json is not None:
            user_update = User(
                username=request.json['username'],
                password=request.json['password'],
                displayName=UserFullName(
                    firstName=request.json['displayName']['firstName'],
                    lastName=request.json['displayName']['lastName']
                ),
                email=request.json['email'],
                adminRights=request.json['adminRights'],
                paymentInfo=PaymentInfo(
                    name=request.json['paymentInfo']['name'],
                    cardType=request.json['paymentInfo']['cardType'],
                    num=int(request.json['paymentInfo']['num']),
                    expiry=datetime.datetime.strptime(request.json['paymentInfo']['expiry'],
                                                      "%w/%m/%y %I:%M:%S %p UTC")
                ),
                address=Address(
                    number=int(request.json['address']['number']),
                    name=request.json['address']['name'],
                    streetType=request.json['address']['streetType'],
                    postalCode=request.json['address']['postalCode']
                )
            )

        user_update.save()

        # user = {
        #     '_id':  user_update.mongo_id,
        #     'username':  user_update.name,
        #     'password': user_update.password,
        #     'displayName': {'firstName': user_update.displayName.displayName, 'lastName': user_update.displayName.lastName},
        #     'email':  user_update.email,
        #     'paymentInfo': { 'name': user_update.paymentInfo.name, 'cardType': , 'num': , 'cvNum': , 'expiry': },
        #     'address':  user_update.address
        # }

        return jsonify({'data': {'message': 'Updated with item id: ' + str(user_update.mongo_id),
                                 'mongo_id': str(user_update.mongo_id)}
                        })
    else:
        return jsonify({'error': 'user not updated'})


