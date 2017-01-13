import os
basedir = os.path.abspath(os.path.dirname(__file__))
#CSRF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'
#SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:yadbonusy@localhost/test1' local
MONGOALCHEMY_DATABASE = 'mzv'
MONGOALCHEMY_SERVER = 'ds055925.mlab.com'
MONGOALCHEMY_PORT = '55925'
MONGOALCHEMY_USER = 'admin'
MONGOALCHEMY_PASSWORD = 'admin'
MONGOALCHEMY_CONNECTION_STRING='mongodb://admin:admin@ds055925.mlab.com:55925/mzv'
SQLALCHEMY_DATABASE_URI = 'postgres://fkjqvmbn:NSHmfUpjQIBJJ0YXADVILhuwyK0GV8Kx@fizzy-cherry.db.elephantsql.com:5432/fkjqvmbn'
