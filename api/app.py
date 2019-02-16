""" Contains all the route control for the api."""

from flask import Flask, jsonify, redirect, url_for, session, request
from flask_restful import Resource, Api
from flask_cors import CORS     # Allows cross origin references to api
from flaskext.mysql import MySQL


from account import Register, Login, GetAccount, Logout

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'hack2019'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bg73d3Pj4gB7Ihkh'  # Do not change
app.config['MYSQL_DATABASE_DB'] = 'bargain_swipes'

CORS(app)   # This allows access from all domains, TODO: fix this
api = Api(app)

# Setup MySQL
mysql = MySQL()
mysql.init_app(app)

api.add_resource(Register, '/register', resource_class_args=(mysql,))
api.add_resource(Login, '/login', resource_class_args=(mysql,))
api.add_resource(GetAccount, '/account', resource_class_args=(mysql,))
api.add_resource(Logout, '/logout', resource_class_args=(mysql,))

if __name__ == '__main__':
    app.run(debug=True)