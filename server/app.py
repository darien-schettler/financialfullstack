from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import stripe
import os

# ----- CONFIGURATION -----
DEBUG = True

# Figure where to put this later... safekeeping currently
ALPHA_API = "J8XGZWZWS7ZXJZ0G"

# ----- CONSTANTS -----
STOCKS = [
    {
        'id': uuid.uuid4().hex,
        'ticker': 'WEED.TO',
        'company': 'Canopy Growth Corporation',
        'price': '57.19'
    },
    {
        'id': uuid.uuid4().hex,
        'ticker': 'TSLA',
        'company': 'Tesla Motors',
        'price': '191.26'
    },
    {
        'id': uuid.uuid4().hex,
        'ticker': 'DIS',
        'company': 'The Walt Disney Corporation',
        'price': '131.70'
    },
    {
        'id': uuid.uuid4().hex,
        'ticker': 'BYND',
        'company': 'Beyond Meat Inc.',
        'price': '94.73'
    },
    {
        'id': uuid.uuid4().hex,
        'ticker': 'UBER',
        'company': 'Uber Technologies Inc.',
        'price': '39.60'
    }
]

# ----- INSTANTIATE THE APP -----
app = Flask(__name__)
app.config.from_object(__name__)

# ----- ENABLE CORS -----
#
# It's worth noting that the above setup allows cross-origin requests on all routes, from any domain, protocol, or port.
#
# In a production environment, you should only allow cross-origin requests from the domain where
# the front-end application is hosted. Refer to the Flask-CORS documentation for more info on this.
CORS(app, resources={r'/*': {'origins': '*'}})


# SANITY CHECK ROUTE
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/stocks', methods=['GET', 'POST'])
def all_stocks():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        STOCKS.append({
            'id': uuid.uuid4().hex,
            'ticker': post_data.get('ticker'),
            'company': post_data.get('company'),
            'price': post_data.get('price')
        })

        response_object['message'] = 'Stock added!'

    else:
        response_object['stocks'] = STOCKS

    return jsonify(response_object)


@app.route('/charge', methods=['POST'])
def create_charge():
    # Get the information payload from the front end
    post_data = request.get_json()

    # Get the amount and convert it to cents
    amount = round(float(post_data.get('stock')['price']) * 100)

    # Set the stripe api key to be the one loaded into the local environment
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # Create the charge object with various post parameters
    charge = stripe.Charge.create(
        amount=amount,
        currency='cad',
        card=post_data.get('token'),
        description=post_data.get('stock')['ticker']
    )

    # Create the response object
    response_object = {
        'status': 'success',
        'charge': charge
    }
    # Return the response object and a success code
    return jsonify(response_object), 200


@app.route('/charge/<charge_id>')
def get_charge(charge_id):

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    # Create the response object
    response_object = {
        'status': 'success',
        'charge': stripe.Charge.retrieve(charge_id)
    }
    return jsonify(response_object), 200


@app.route('/stocks/<stock_id>', methods=['GET', 'PUT', 'DELETE'])
def single_stock(stock_id):
    response_object = {'status': 'success'}

    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_stock = ''
        for stock in STOCKS:
            if stock['id'] == stock_id:
                return_stock = stock
        response_object['stock'] = return_stock

    if request.method == 'PUT':
        put_data = request.get_json()
        remove_stock(stock_id)
        STOCKS.append({
            'id': uuid.uuid4().hex,
            'ticker': put_data.get('ticker'),
            'company': put_data.get('company'),
            'price': put_data.get('price')
        })
        response_object['message'] = 'Stock updated!'

    if request.method == 'DELETE':
        remove_stock(stock_id)
        response_object['message'] = 'Stock removed!'

    return jsonify(response_object)


def remove_stock(stock_id):
    for stock in STOCKS:
        if stock['id'] == stock_id:
            STOCKS.remove(stock)
            return True
    return False


if __name__ == '__main__':
    app.run()
