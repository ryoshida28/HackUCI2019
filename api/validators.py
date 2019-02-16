import re
from response import Response

def validateName(name: str):
    return type(name)==str and re.match('^[A-Za-z]{1,50}$', name) != None

def validateEmail(email: str):
    return type(email)==str and re.match(r'^[^@]+@[^@]+\.[^@]+$', email) != None

def validateAge(age: int):
    return type(age)==int and 8<=age

def validatePass(password, confirm_password):
    """ Returns a Response object that informs whether the password is legal and matches the confimation password."""
    # Ensure legal password, must be longer than 8 characters
    res = Response()
    if len(password) < 8:
        res.setSuccess(False)
        res.addErrorMessage('Password must be 8 characters long')
        return res

    if password == confirm_password:
        return res
    else:
        res.setSuccess(False)
        res.addErrorMessage('Confirm Password does not match Password.')
        return res