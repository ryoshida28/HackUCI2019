from response import Dictable
class Account(Dictable):

    def __init__(self, id, fname, lname, email, birthdate, date_created):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.birthdate = birthdate
        self.date_created = date_created
        self.tokens = []
    
    def getDict(self):
        return {
            'id': self.id,
            'first_name': self.fname,
            'last_name': self.lname,
            'email': self.email,
            'birthdate': self.birthdate,
            'date_created': str(self.date_created),
            'tokens': self.tokens
        }
