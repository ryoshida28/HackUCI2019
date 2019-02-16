import os

class Config:
    """ Used to set any configuration settings to flask app.
    Store as static variables"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False