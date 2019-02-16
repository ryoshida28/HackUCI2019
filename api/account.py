from flask import request, jsonify
from flask_restful import Resource, reqparse
from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt

import re
from datetime import datetime
from response import Response, Dictable
import db as DB
import validators as Validate
import secrets

class Account(Dictable):
    def __init__(self, id=0, fName=None, lName=None, email=None, age=0, date_created=None):
        """ Creates an account. Data must be validated before being created."""
        self.id = id
        self.name = [fName, lName]
        self.email = email
        self.age = age
        self.created = date_created

    def getDict(self):
        return {
            'id': self.id,
            'fname': self.name[0],
            'lname': self.name[1],
            'email': self.email,
            'age': self.age,
            'created': self.created
        }
    
    def __eq__(self, right):
        return type(right) == Account and self.id == right.id

    @staticmethod
    def crtFromDBDict(d: dict):
        return Account(d['id'], d['first_name'], d['last_name'], d['email'], d['age'], d['date_created']) if d else False


get_account_parser = reqparse.RequestParser()
get_account_parser.add_argument('token', type=str)
get_account_parser.add_argument('id', type=int)
class GetAccount(Resource):
    def __init__(self, mysql):
        self._mysql = mysql
    def post(self):
        res = Response()
        args = get_account_parser.parse_args()

        if DB.tokenMatch(args['token'], args['id'], self._mysql):
            o = Account.crtFromDBDict(DB.getAttribute(args['id'],'*',self._mysql))
            res.setResponseObj(o)
        else:
            res.setSuccess(False)
            res.addErrorMessage('Not Logged In.')
        
        return res.getResponse()

# Set up data parser
register_parser = reqparse.RequestParser()
register_parser.add_argument('fname', type=str, required=True, trim=True)
register_parser.add_argument('lname', type=str, required=True, trim=True)
register_parser.add_argument('email', type=str, required=True, trim=True)
register_parser.add_argument('birthdate', type=datetime, required=True)
register_parser.add_argument('password', type=str, required=True)
register_parser.add_argument('confirm_pass', type=str, required=True)

class Register(Resource):
    """ Defines how to sign-up an account."""
    def __init__(self, mysql):
        self._mysql = mysql

    
    def post(self):
        args = register_parser.parse_args()
        res = Response()

        validators = {
            'first name':   Validate.validateName(args['fname']),
            'last name':    Validate.validateName(args['lname']),
            'email':        Validate.validateEmail(args['email']),
            'age':          Validate.validateAge(args['age']),
            'password':     Validate.validatePass(args['password'], args['confirm_pass'])
        } 

        if not all(validators.values()):
            res.setSuccess(False)
            res.addInvalidItems(*(i[0] for i in validators.items() if not i[1]))
            if not validators['password']: res.addResponse(validators['password'])
            return res.getResponse()

        newAcc = Account(id=0, fName=args['fname'], lName=args['lname'], email=args['email'], age=args['age'], date_created=None)

        passhash = sha256_crypt.hash(args['password'])

        # Add to Database
        if DB.createAccount(newAcc, passhash, self._mysql):
            token = secrets.token_urlsafe()
            if DB.addToken(token, newAcc.id, self._mysql):
                res.setSession(token, newAcc.id)
            else:
                res.setSuccess(False)
                res.addErrorMessage('Could not set token.')

            res.setResponseObj(newAcc)
        else:
            res.setSuccess(False)
            res.addErrorMessage('An unknown database error occurred.')
        
        return res.getResponse()

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, trim=True)
login_parser.add_argument('password', type=str, required=True)
class Login(Resource):
    def __init__(self, mysql):
        self._mysql = mysql
    
    def post(self):
        args = login_parser.parse_args()
        res = Response()

        validators = {
            'email':    Validate.validateEmail(args['email'])
        }

        if not all(validators.values()):
            res.setSuccess(False)
            res.addInvalidItems(*(i[0] for i in validators.items() if not i[1]))
            return res
        

        # Verify account
        acctResp = DB.verifyAccount(args['email'], args['password'], self._mysql)
        if not acctResp:
            res.addResponse(acctResp)
        else:
            # Generate Token
            acct = Account.crtFromDBDict(acctResp.getResponseObj())
            token = secrets.token_urlsafe()
            DB.addToken(token, acct.id, self._mysql)
            res.setSession(token, acct.id)
            res.setResponseObj(acct)
        

        return res.getResponse()

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('token', type=str, required=True)
logout_parser.add_argument('id', type=int)
class Logout(Resource):
    def __init__(self, mysql):
        self._mysql = mysql
    
    def post(self):
        # Remove access token
        args = logout_parser.parse_args()
        res = Response()
        if not DB.removeToken(args['token'], args['id'], self._mysql):
            res.setSuccess(False)
            res.addErrorMessage('Could not logout.')
        return res.getResponse()

