import sqlite3 as sql
from initialize_DB import DB_PATH


def conn():
    """
    Connect to the DB
    @return conn: a connection to the DB
    @return cursor: a cursor with the connection
    """
    c = sql.connect(DB_PATH)
    cursor = c.cursor()
    return c, cursor


def close(c, cursor, commit_before_closing=False):
    """
    Close the cursor and connection to the DB
    @param c: connection to the DB
    @param cursor: cursor with the connection
    @param commit_before_closing: (default = False)
       True -> commit all queries before closing
       False -> rollback all non-committed queries before closing
    """
    if commit_before_closing:
        c.commit()
    cursor.close()
    c.close()
