from passlib.hash import sha256_crypt
from response import Response
accounts_columns = ('id', 'first_name', 'last_name', 'email', 'birthdate', 'password', 'date_created')

def getLastInsertID(mysql):
    """ Gets the last insert id into any table."""
    sql = 'SELECT LAST_INSERT_ID();'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()
    resp = cur.fetchone()
    return resp[0] if res>0 else False

def getAttribute(id, columns, mysql):
    """ Gets the specified attributes of the row with specified id.
        Returns a dictionary with keys as the attribute name and values as the returned value.
        if columns is a string, that one attribute will be found. If an iterable, all attributes in iterable will be found."""
    tbl_name = 'accounts'
    colStr = columns if type(columns) == str else ', '.join(columns)
    sql = f'SELECT {colStr} FROM {tbl_name} WHERE id={id};'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()
    if type(columns) == str:
        if columns.strip() == '*' or columns.strip().lower() == 'all':
            columns = accounts_columns
        else:
            columns = columns.split()
    
    resp = {col.strip(): val for col, val in zip(columns, cur.fetchone())}
    return resp if res > 0 else False

def verifyAccount(email, password, mysql):
    tbl_name = 'accounts'
    colStr = ', '.join(accounts_columns)
    sql = f'SELECT {colStr} FROM {tbl_name} WHERE email="{email}";'
    print(sql)
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()

    response = Response()
    if res > 0:
        row = {col: val for col, val in zip(accounts_columns, cur.fetchone())}
        if sha256_crypt.verify(password, row['password']):
            del row['password']
            response.setResponseObj(row)
        else: 
            response.setSuccess(False)
            response.addErrorMessage('Password does not match email')
    else: 
        response.setSuccess(False)
        response.addErrorMessage('Email does not exist.')
    return response


def createAccount(a, hashedPass, mysql):
    """ Saves new account to database. Will mutate account object, getting its id and date created."""
    tbl_name = 'accounts'
    sql = f'INSERT INTO {tbl_name}(first_name, last_name, email, birthdate, password) ' + \
        f'VALUES("{a.name[0]}", "{a.name[1]}", "{a.email}", {a.age}, "{hashedPass}");'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()
    if res > 0:
        id = getLastInsertID(mysql)
        a.id = id
        a.created = getAttribute(a.id, ('date_created',), mysql)['date_created']
        return a.id and a.created
    else: return False

def addToken(token, id, mysql):
    tbl_name = 'tokens'
    sql = f'INSERT INTO {tbl_name} (account_id, token) ' + \
        f'VALUES({id}, "{token}");'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()
    return res > 0

def tokenMatch(token, id, mysql):
    tbl_name = 'tokens'
    sql = f'SELECT token FROM {tbl_name} WHERE account_id={id};'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    cur.close()
    if res > 0:
        for t in cur.fetchall():
            if token == t[0]:
                return True
    return False

def removeToken(token, id, mysql):
    tbl_name = 'tokens'
    sql = f'SELECT id, token FROM {tbl_name} WHERE account_id={id};'
    cur = mysql.get_db().cursor()
    res = cur.execute(sql)
    if res > 0:
        for t in cur.fetchall():
            if token == t[1]:
                sql = f'DELETE FROM {tbl_name} WHERE id={t[0]};'
                if cur.execute(sql) > 0:
                    return True
    return False