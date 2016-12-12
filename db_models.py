from dbconnect import psql_connect
from passlib.hash import sha256_crypt


def user_autorisation(username,password):
    curr, conn = psql_connect()
    curr.execute("SELECT * FROM tusers where USERNAME=(%s)", (username,))
    user_data = curr.fetchone()
    if user_data != None:
        if  sha256_crypt.verify(password, user_data[4]):
            return True
        else:
            return False
    else:
        return False

def get_flowers():
    curr, conn = psql_connect()
