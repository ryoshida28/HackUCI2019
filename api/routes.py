# Flask Imports
from flask import jsonify
from flask_restful import Resource, reqparse
from passlib.hash import sha256_crypt

# Python Imports
from datetime import datetime, date
import json
import os

# Our Imports
from account import Account
from response import Response
import db


class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name', type=str, required=True, trim=True)
        self.parser.add_argument('last_name', type=str, required=True, trim=True)
        self.parser.add_argument('email', type=str, required=True, trim=True)
        self.parser.add_argument('birthdate', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('confirm_password', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()
        res = Response()

        # Verify data
        if args['password'] != args['confirm_password']:
            res.setSuccess(False)
            res.addInvalidItems('password')
            res.addErrorMessage('Passwords do not match.')
            return jsonify(res.getResponse())
        
        password = sha256_crypt.hash(args['password'])

        newAcct = Account(0, args['first_name'], args['last_name'], args['email'], args['birthdate'], None)
        if db.createAccount(newAcct, password):
            res.setResponseObj(newAcct)
        else:
            res.setSuccess(False)
            res.addErrorMessage('Could not create account.')
        
        return res.getResponse()

class Login(Resource):
    pass

class GetAccount(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, required=True)
        self.parser.add_argument('token', type=str)
    def post(self):
        args = self.parser.parse_args()
        res = Response()

        # Verify Token
        a = db.verifyToken(args['id'], args['token'])
        if a == None:
            res.setSuccess(False)
            res.addErrorMessage('Not logged in.')
            return res.getResponse()
        else:
            print(a.getDict())
            res.setResponseObj(a)
            return res.getResponse()

class Logout(Resource):
    pass