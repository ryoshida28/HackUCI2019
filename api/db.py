from passlib.hash import sha256_crypt
import json
import os
from datetime import datetime, timedelta
import base64
from account import Account


def lastInsertID(filename):
    db = None
    with open(filename, 'r') as fp:
        db = json.load(fp)
    if db == None:
        return 0
    else:
        return int(db['last_insert_id'])
        

def generateToken(expires=3600):
    token = base64.b64encode(os.urandom(24)).decode('utf-8')
    expiration_date = datetime.utcnow() +timedelta(seconds=expires)
    return (token, expiration_date)

def createAccount(acct, passHash):
    db = None
    with open(os.path.join('db', 'accounts.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    else:
        if acct.email in (authObj['email'] for authObj in db['authorization']):
            return False
        acct.id = db['last_insert_id']+1
        acct.date_created = datetime.utcnow()
        token = generateToken()
        acct.tokens.append({'token': token[0], 'expires': str(token[1])})
        db['accounts'].append(acct.getDict())
        db['authorization'].append({'id': acct.id, 'email': acct.email, 'password': passHash})
        db['last_insert_id'] = acct.id
        with open(os.path.join('db', 'accounts.json'), 'w') as fp:
            json.dump(db, fp)
        return True

def getAccountByID(id, db):
    for acct in db['accounts']:
        if id==acct['id']:
            retrievedAcct = Account(acct['id'], acct['first_name'], acct['last_name'], acct['email'], acct['birthdate'], acct['date_created'])
            retrievedAcct.tokens = acct['tokens']
            return retrievedAcct
    return None

def verifyToken(id, token):
    db = None

    with open(os.path.join('db', 'accounts.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    else:
        acct = getAccountByID(id, db)
        if acct == None:
            return False
        else:
            if token in (token['token'] for token in acct.tokens):
                return acct
            return False