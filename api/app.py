""" Contains all the route control for the api."""

from flask import Flask, jsonify, redirect, url_for, session, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS     # Allows cross origin references to api

import os
import json

from routes import Register, Login, GetAccount, Logout, GetProducts
import db
from response import Response
from product import Product


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '\db'

CORS(app)   # This allows access from all domains, TODO: fix this
api = Api(app)


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GetAccount, '/account')
api.add_resource(Logout, '/logout')
# api.add_resource(GetProducts, '/products')

@app.route('/products', methods=['GET'])
def getProducts():
    products = db.getAllProducts()
    return jsonify(products)

@app.route('/products/<category>', methods=['GET'])
def getProductsByCategory(category):
    return jsonify(db.getProductsByCat(category))

@app.route('/account/<account_id>/products', methods=['GET'])
def get_product_by_account_id(account_id):
    products = db.getAllProducts([], account_id)
    print(products)
    return jsonify(products)

@app.route('/post_item', methods=['POST'])
def post_item():
    if request.method == 'POST':
        res = Response()
        data = request.form
        account_id = int(data['account_id'])
        token = data['token']

        # Get Account
        acct = db.verifyToken(account_id, token)
        if not acct:
            res.setSuccess(False)
            res.addErrorMessage('Invalid Tokens')
            return res.getResponse()
        
        # Get Product
        prod = Product(0, acct.id, data['name'], data['description'], data['min_price'], data['max_price'], json.loads(data['categories']), [])

        os.path.isdir("/db/images/{account_id}")
        id = 0
        for f in dict(request.files):
            filename = db.uploadFile(request.files[f],prod,id)
            prod.addImage(filename)
            id += 1
        
        # Save Product
        if db.createProduct(prod):
            res.setResponseObj(prod)
        else:
            res.setSuccess(False)

        return res.getResponse()

@app.route('/categories', methods=['GET'])
def getCategories():
    return jsonify(db.getAllCategories())


# @app.route('/static/images/<account_id>/<product_id>/<filename>', methods=['GET'])
# def getFile(account_id, product_id, filename):
#     path = os.path.join(app.config['UPLOAD_FOLDER'], account_id, product_id)
#     print(path)
#     return send_from_directory(path, filename)

if __name__ == '__main__':
    app.run(debug=True)