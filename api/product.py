from response import Dictable

class Product(Dictable):
    def __init__(self, id, account_id, name, description, min_price, max_price, categories=[], images=[]):
        self.id = id
        self.account_id = account_id
        self.name = name
        self.description = description
        self.price = [min_price, max_price]
        self.categories = categories
        self.images = images
    
    def getDict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'description': self.description,
            'min_price': self.price[0],
            'max_price': self.price[1],
            'categories': self.categories,
            'images': self.images
        }
