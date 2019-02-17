from passlib.hash import sha256_crypt
import json
import os
from datetime import datetime, timedelta
import base64
from account import Account
from collections import defaultdict
from product import Product


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

        os.mkdir(os.path.join('static', 'images', str(acct.id)))
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

def authenticate(email, password):
    db = None
    
    with open(os.path.join('db', 'accounts.json'), 'r') as fp:
        db = json.load(fp)
    if db == None:
        return False
    else:
        for account in db['authorization']:
            if account['email'] == email and sha256_crypt.verify(password, account['password']):
                token = generateToken()
                for i in range(len(db['accounts'])):
                    if db['accounts'][i]['id'] == account['id']:
                        db['accounts'][i]['tokens'].append({'token': token[0], 'expires': str(token[1])})
                with open(os.path.join('db', 'accounts.json'), 'w') as fp:
                    json.dump(db, fp)
                return getAccountByID(account['id'], db)
        return False

def removeToken(id, token):
    db = None

    with open(os.path.join('db', 'accounts.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    else:
        found_token = False
        for i in range(len(db['accounts'])):
            print(db['accounts'][i]['id'], id)
            if db['accounts'][i]['id'] == id:
                for j in range(len(db['accounts'][i]['tokens'])):
                    print(id, db['accounts'][i]['tokens'][j]['token'], token)
                    if db['accounts'][i]['tokens'][j]['token'] == token:
                        del db['accounts'][i]['tokens'][j]
                        found_token = True
                        break
    
    with open(os.path.join('db', 'accounts.json'), 'w') as fp:
        json.dump(db, fp)

    return found_token

def uploadFile(f, product, img_id):
    filepath = os.path.join('static', 'images',str(product.account_id), str(product.id))
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    
    print(f.mimetype)
    imgpath = os.path.join(filepath, 'img-'+ str(img_id) + '.' + f.mimetype.split('/')[1])
    f.save(imgpath)
    return imgpath

def createProduct(product):
    db = None
    with open(os.path.join('db', 'products.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    else:
        product.id = db['last_insert_id'] + 1
        db['last_insert_id'] = product.id
        db['products'].append(product.getDict())
        with open(os.path.join('db', 'products.json'), 'w') as fp:
            json.dump(db, fp)

        return True

def getAllProducts(categories=[], account_id=None):
    db = None
    with open(os.path.join('db', 'products.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    categories = set(categories)
    matches_dict = defaultdict(list)
    for product in db['products']:
        if (account_id == None) or (int(account_id) == product['account_id']):
            matches = len(set(product['categories']) and categories)
            productObj = Product(product['id'],product['account_id'], product['name'], product['description'], product['min_price'], product['max_price'], product['categories'], product['images'])
            matches_dict[matches].append(productObj)
            
    products = []
    for matches, product in sorted(matches_dict.items(), reverse=True):
        for p in product:
            products.append(p.getDict())
    return products

def getAllCategories():
    db = None
    with open(os.path.join('db', 'products.json'), 'r') as fp:
        db = json.load(fp)
    
    if db == None:
        return False
    
    categories = defaultdict(int)
    for product in db['products']:
        for category in product['categories']:
            categories[category] += 1
    
    return [c for c,_ in sorted(categories.items(), key=(lambda x: x[1]))]