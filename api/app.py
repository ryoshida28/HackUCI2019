""" Contains all the route control for the api."""

from flask import Flask, jsonify, redirect, url_for, session, request
from flask_restful import Resource, Api
from flask_cors import CORS     # Allows cross origin references to api

import os

from routes import Register, Login, GetAccount, Logout
import db
from response import Response
from product import Product

app = Flask(__name__)

CORS(app)   # This allows access from all domains, TODO: fix this
api = Api(app)


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetAccount, '/account')
api.add_resource(Logout, '/logout')
# api.add_resource(PostItem, '/post_item')

@app.route('/post_item', methods=['POST'])
def post_item():
    if request.method == 'POST':
        res = Response()
        data = request.data
        account_id = int(data['account_id'])
        token = data['token']

        # Get Account
        acct = db.verifyToken(account_id, token)
        if not acct:
            res.setSuccess(False)
            res.addErrorMessage('Invalid Tokens')
            return res.getResponse()
        
        # Get Product
        prod = Product(0, acct.id, data['name'], data['description'], data['min_price'], data['max_price'], data['categories'], None)

        os.path.isdir("/db/images/{account_id}")
        for _, f in request.files:
            db.uploadFile(f,)
        r = request.files['images']
        print(r)
        return jsonify({'heool': str(r)})

if __name__ == '__main__':
    app.run(debug=True)