from flask import jsonify
from abc import ABC, abstractmethod

class Dictable(ABC):
    @abstractmethod
    def getDict(self):
        pass

class Response:
    """ Defines a standard response. 
        Use getResponse() to get a json string representation of the response.
        - invalid_items should only be single words defining specific invalid data input.
        - err_messages should only be sentences and phrases describing an error."""

    def __init__(self):
        """ Instantiates a default Response object. Success is initially set to True."""
        self._success = True
        self._invalid_items = []
        self._err_messages = []
        self._dictable = None
    
    def isSuccess(self):
        return self._success
    
    def getInvalidItems(self):
        return self._invalid_items
    
    def getErrorMessages(self):
        return self._err_messages

    def setSuccess(self, success: bool):
        """ Sets whether the response should return a success or error."""
        self._success = success

    def setResponseObj(self, o):
        """ Expects o to an instance of Dictable."""
        self._dictable = o
    
    def addInvalidItems(self, *items):
        """ All positional arguments must be strings."""
        self._invalid_items.extend(items)
    
    def addErrorMessage(self, err):
        """ Adds an error message to the Response object."""
        self._err_messages.append(err)

    def addResponse(self, res):
        """ Adds the invalid items and the error messages to this Response.
        Success is only true if both this and res are success."""
        if type(res) == Response:
            self._success = self._success and res.isSuccess()
            self._invalid_items.extend(res.getInvalidItems())
            self._err_messages.extend(res.getErrorMessages())

    def getResponse(self):
        """ Gets a JSON representation of the response object."""
        res = {
            'success': self._success,
            'invalid_items': self._invalid_items,
            'error_messages': self._err_messages
        }

        if self._dictable != None and isinstance(self._dictable, Dictable):
            res['object'] = self._dictable.getDict()
        
        return jsonify(res)

    def getResponseObj(self):
        return self._dictable

    def __bool__(self):
        return self._success