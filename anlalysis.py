import re
import sqlite3
from sqlite3 import Error

def sql_connection(db):
    try:
        con = sqlite3.connect(db)
        return con
    except Error:
        print(Error)

def sql_query(conn, query, values = None):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    if values is None:
        cur.execute(query)
    else:
        cur.execute(query, values)
    rows = cur.fetchall()
    return rows

if __name__ == '__main__':
    '''
    Database Version Code
    '''
    con = sql_connection('buds.db')
    order_users = "SELECT users.name FROM messages JOIN users on messages.fk_sender_id = users.id"

    order_users2 = "SELECT fk_sender_id, count()  FROM messages INNER join users GROUP BY fk_sender_id ORDER BY count() DESC"
    "SELECT count(messages.id) FROM messages Inner JOIN users on messages.fk_sender_id == users.id GROUP BY fk_sender_id "
    ret = sql_query(con, order_users2)
    print(ret)