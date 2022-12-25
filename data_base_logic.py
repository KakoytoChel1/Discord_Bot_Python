import sqlite3
from sqlite3 import Error


def add_new_item(db_file, item):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        sql = ''' INSERT INTO Users(channel_id,user_id,user_name)
                          VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def delete_item(db_file, channel_id):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        sql = 'DELETE FROM Users WHERE channel_id=?'
        cur = conn.cursor()
        cur.execute(sql, (channel_id,))
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def select_item(db_file, channel_id):
    conn = None
    rows = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE channel_id=?", (channel_id,))

        # must be one item
        rows = cur.fetchall()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return rows[0]
