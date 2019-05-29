from flask import Flask, jsonify
from flask_cors import CORS

# ----- CONFIGURATION -----
DEBUG = True


# ----- CONSTANTS -----
STOCKS = [
    {
        'ticker': 'WEED.TO',
        'company': 'Canopy Growth Corporation',
        'price': '57.19'
    },
    {
        'ticker': 'TSLA',
        'company': 'Tesla Motors',
        'price': '191.26'
    },
    {
        'ticker': 'DIS',
        'company': 'The Walt Disney Corporation',
        'price': '131.70'
    },
    {
        'ticker': 'BYND',
        'company': 'Beyond Meat Inc.',
        'price': '94.73'
    },
    {
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


@app.route('/stocks', methods=['GET'])
def all_stocks():
    return jsonify({
        'status': 'success',
        'stocks': STOCKS
    })


if __name__ == '__main__':
    app.run()
