import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "./stats.db"

    sql_create_invocations_table = """ CREATE TABLE IF NOT EXISTS invocations (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        command text NOT NULL,
                                        invoker integer NOT NULL,
                                        target text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_invocations_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == "__main__":
    main()