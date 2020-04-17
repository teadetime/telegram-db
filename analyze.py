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
    con = sql_connection('telegram.db')
    user_table = "CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, name text)"
    message_table = "CREATE TABLE IF NOT EXISTS  messages(id integer PRIMARY KEY, content text,  time text, photo integer, backtoback integer, reply integer,   fk_sender_id integer Not Null, FOREIGN  KEY  (fk_sender_id) REFERENCES  users (id) )"
    sql_exec(con, user_table)
    sql_exec(con, message_table)

    chat_name = 'message'
    prev_sender = None
    for file in glob.glob(chat_name + '*'):
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

            # user_dict[sender] = user_dict.get(sender, {'text': '', 'file': 0, 'reply': 0, 'count': 0})
            # user_dict[sender]['file'] += file
            # user_dict[sender]['reply'] += reply
            # user_dict[sender]['count'] += num_add
            # user_dict[sender]['text'] += text.strip()

    # chat_name = 'message'
    # dict_list = []
    # soup = bs(open('bod.html'), 'html.parser')
    # # print(soup)
    # count = 0
    # user_dict = {}
    # # Parsing entire message
    # message_divs = soup.find_all('div', attrs={"id": re.compile('^message')})
    # prev_sender = None
    # for message in message_divs:
    #     mess_class = message.attrs['class']
    #     num_add = 1  # variable so multiple stacked messages are counted as one
    #     # Bot message
    #     if 'service' in mess_class:
    #         continue
    #     # Someone sent a message right after themselves, Maybe we should concatenate
    #     elif 'joined' in mess_class:
    #         sender = prev_sender
    #         num_add = 0
    #     # normal message
    #     else:
    #         sender = message.find('div', {'class': 'from_name'}).contents[0].strip()
    #         prev_sender = sender
    #     reply = True if message.find('div', {'class': 'reply_to'}) else False
    #     text = message.find('div', {'class': 'text'}).getText() if message.find('div', {'class': 'text'}) else ''
    #     file = True if message.find('div', {'class': 'media_wrap'}) else False
    #     user_dict[sender] = user_dict.get(sender, {'text': '', 'file': 0, 'reply': 0, 'count': 0})
    #     user_dict[sender]['file'] += file
    #     user_dict[sender]['reply'] += reply
    #     user_dict[sender]['count'] += num_add
    #     user_dict[sender]['text'] += text.strip()
    # sorted_result = sorted(user_dict.items(), reverse=True, key=lambda item: len(item[1]['text']))
    # # word_cnt = [len(item[1]['text']) for item in sorted_result]
    # # print(word_cnt)
    # for person in sorted_result:
    #     print(person[0], 'Characters:', len(person[1]['text']), 'Replies:', person[1]['reply'])

    # for file in glob.glob(chat_name+'*'):
    # print(*sorted_result, sep = "\n")
    #     sent_messages = soup.find_all('div', attrs={"class": 'from_name'})
    #     for mess in sent_messages:
    #         name = mess.contents[0].strip()
    #         user_dict[name] = user_dict.get(name, 0)+1
    #     dict_list.append(user_dict)
    # # Sum up the dictionaries
    # counter = collections.Counter()
    # for d in dict_list:
    #     counter.update(d)
    # result = dict(counter)
    # sorted_result = sorted(result.items(), reverse=True, key=lambda item: item[1])
    # print(*sorted_result, sep = "\n")
