import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def add_invocation(conn, invocation):
    sql = ''' INSERT INTO invocations(command,invoker,target)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, invocation)
    conn.commit()
    return

def select_stats_by_field(conn, field):
    cur = conn.cursor()
    cur.execute("SELECT {}, COUNT(*) FROM invocations GROUP BY {} ORDER BY COUNT(*) DESC".format(field, field))

    rows = cur.fetchall()

    return rows

def select_stats(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM invocations")

    rows = cur.fetchall()

    return rows