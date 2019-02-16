""" Contains all the route control for the api."""

from flask import Flask, jsonify, redirect, url_for, session, request
from flask_restful import Resource, Api
from flask_cors import CORS     # Allows cross origin references to api


from routes import Register, Login, GetAccount, Logout

app = Flask(__name__)

CORS(app)   # This allows access from all domains, TODO: fix this
api = Api(app)


api.add_resource(Register, '/register')
# api.add_resource(Login, '/login')
api.add_resource(GetAccount, '/account')
# api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)