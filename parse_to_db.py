from bs4 import BeautifulSoup as bs
import glob
import collections
import re
import sqlite3
from sqlite3 import Error


def sql_connection(db):
    try:
        con = sqlite3.connect(db)
        return con
    except Error:
        print(Error)


def sql_exec(con, table):
    cursorObj = con.cursor()
    cursorObj.execute(table)
    con.commit()

def sql_insert(con, table, values = None):
    cur = con.cursor()
    if values is None:
        cur.execute(table)
    else:
        cur.execute(table, values)
    con.commit()

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

def check_user(db_con, user_name):
    mess_tuple = (user_name,)
    query = "SELECT EXISTS( SELECT 1 FROM users where name = ?)"
    result = sql_query(db_con, query, mess_tuple)
    return bool(result[0][0])


if __name__ == '__main__':
    '''
    Database Version Code
    '''
    con = sql_connection('buds.db')
    user_table = "CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, name text)"
    message_table = "CREATE TABLE IF NOT EXISTS  messages(id integer PRIMARY KEY, content text,  time text, photo integer, backtoback integer, reply integer,   fk_sender_id integer Not Null, FOREIGN  KEY  (fk_sender_id) REFERENCES  users (id) )"
    sql_exec(con, user_table)
    sql_exec(con, message_table)

    chat_name = 'bud'
    prev_sender = None
    for file in glob.glob(chat_name + '*.html'):
        print(file)
        soup = bs(open(file), 'html.parser')
        # Parsing entire message
        message_divs = soup.find_all('div', attrs={"id": re.compile('^message')})
        for message in message_divs:
            backtoback = 0
            mess_class = message.attrs['class']
            # Bot message
            if 'service' in mess_class:
                continue
            # Someone sent a message right after themselves, Maybe we should concatenate
            elif 'joined' in mess_class:
                sender = prev_sender
                backtoback = 1
            # normal message
            else:
                sender = message.find('div', {'class': 'from_name'}).contents[0].strip()
                prev_sender = sender
            reply = 1 if message.find('div', {'class': 'reply_to'}) else 0
            mess_text = message.find('div', {'class': 'text'}).getText() if message.find('div',
                                                                                         {'class': 'text'}) else ''
            file = 1 if message.find('div', {'class': 'media_wrap'}) else 0

            if not check_user(con, sender):
                insert_user = "INSERT INTO users(name) VALUES(?)"
                mess_tuple = (sender,)
                sql_insert(con, insert_user, mess_tuple)

            # Insert row into Messages table
            insert_mess = "INSERT INTO messages(content, time, photo, reply, backtoback, fk_sender_id) " \
                          "VALUES(?, ?, ?, ?, ?, ?)"
            mess_tuple = (mess_text, '2019-03-17', file, reply, backtoback, sender)
            sql_insert(con, insert_mess, mess_tuple)
            # TODO: get timestamp
