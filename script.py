#!/shop/bin/python
import psycopg2
import sys


def main():
    # Define our connection string
    conn_string = "host='localhost' dbname='test1' user='testuser' password='yadbonusy'"

    # print the connection string we will use to connect
    print("Connecting to database\n	->%s" % (conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    print(cur.execute("SELECT * FROM ftable where category = 0"))
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    rows = cur.fetchall()
    print(rows)
    #for row in rows:
      #  print( "   ", row[1])
    print("Connected!\n")
    #cur.execute('INSERT INTO users (uid, username, email, password) VALUES (%s, %s, %s, %s)', ('1','admin','bodya','123456'))
    #cur.execute('INSERT INTO users (uid, username, email, password) VALUES (%s, %s, %s, %s)',
     #           ('2', 'admin2', 'bodya2', '123456'))
    #conn.commit()
    #print(cur.execute("SELECT * FROM users"))

    cur.close()
    conn.close()
if __name__ == "__main__":
    main()