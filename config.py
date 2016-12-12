import os
basedir = os.path.abspath(os.path.dirname(__file__))
#CSRF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'
#SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:yadbonusy@localhost/test1' local
MONGOALCHEMY_DATABASE = 'fshop'
MONGOALCHEMY_SERVER = 'ds119368.mlab.com'
MONGOALCHEMY_PORT = '19368'
MONGOALCHEMY_USER = 'admin'
MONGOALCHEMY_PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = 'postgres://fkjqvmbn:NSHmfUpjQIBJJ0YXADVILhuwyK0GV8Kx@fizzy-cherry.db.elephantsql.com:5432/fkjqvmbn'
MONGOALCHEMY_CONNECTION_STRING='mongodb://admin:123456@ds119368.mlab.com:19368/fshop'