import psycopg2

def psql_connect():
    conn_string = "host='localhost' dbname='test1' user='testuser' password='yadbonusy'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    return cur, conn

