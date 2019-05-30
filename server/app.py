from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
# ----- CONFIGURATION -----
DEBUG = True

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


@app.route('/stocks/<stock_id>', methods=['PUT', 'DELETE'])
def single_stock(stock_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        put_data = request.get_json()
        remove_stock(stock_id)
        STOCKS.append({
            'id': uuid.uuid4().hex,
            'ticker': put_data.get('ticker'),
            'company': put_data.get('company'),
            'price': put_data.get('price')
        })
        response_object['message'] = 'Stock Updated!'

    if request.method == 'DELETE':
        remove_stock(stock_id)
        response_object['message'] = 'Stock Removed!'

    return jsonify(response_object)


def remove_stock(stock_id):
    for stock in STOCKS:
        if stock['id'] == stock_id:
            STOCKS.remove(stock)
            return True
    return False


if __name__ == '__main__':
    app.run()