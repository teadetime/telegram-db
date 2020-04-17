from bs4 import BeautifulSoup as bs
import glob
import collections
import re

if __name__ == '__main__':
    #course_soup = bs(course_page.content, 'html.parser')
    chat_name = 'message'
    dict_list = []
    soup = bs(open('bod.html'), 'html.parser')
    #print(soup)
    count = 0
    user_dict = {}
    # Parsing entire message
    message_divs = soup.find_all('div', attrs={"id": re.compile('^message')})
    prev_sender = None
    for message in message_divs:
        mess_class = message.attrs['class']
        num_add = 1  # variable so multiple stacked messages are counted as one
        # Bot message
        if 'service' in mess_class:
            continue
        # Someone sent a message right after themselves, Maybe we should concatenate
        elif 'joined' in mess_class:
            sender = prev_sender
            num_add = 0
        # normal message
        else:
            sender = message.find('div', {'class': 'from_name'}).contents[0].strip()
            prev_sender = sender

        print(sender)
        reply = True if message.find('div', {'class': 'reply_to'}) else False
        text = message.find('div', {'class': 'text'}).getText() if message.find('div', {'class': 'text'}) else ''
        print(text)
        file = True if message.find('div', {'class': 'media_wrap'}) else False
        user_dict[sender] = user_dict.get(sender, {'text': '', 'file': 0, 'reply': 0, 'count': 0})
        user_dict[sender]['file'] += file
        user_dict[sender]['reply'] += reply
        user_dict[sender]['count'] += num_add
        user_dict[sender]['text'] += text.strip()
    sorted_result = sorted(user_dict.items(), reverse=True, key=lambda item: len(item[1]['text']))
    # word_cnt = [len(item[1]['text']) for item in sorted_result]
    # print(word_cnt)
    for person in sorted_result:
        print(person[0], 'Characters:', len(person[1]['text']), 'Replies:', person[1]['reply'])



    #for file in glob.glob(chat_name+'*'):
    #print(*sorted_result, sep = "\n")
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