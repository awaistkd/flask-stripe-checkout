import os
import stripe
from flask import Flask, jsonify, render_template, request

stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():

    amount = 500    # amount in cents
    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='A Test Charge'
    )

    return render_template('charge.html', amount=amount)


@app.route('/hello')
def hello_world():
    return jsonify('hello, world!')


if __name__ == '__main__':
    app.run()
