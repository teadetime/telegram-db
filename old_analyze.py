from bs4 import BeautifulSoup as bs
import glob
import collections
import re

if __name__ == '__main__':
    chat_name = 'buds'
    user_dict = {}
    dict_list = []
    for file in glob.glob(chat_name+'*'):
        soup = bs(open(file), 'html.parser')
        message_divs = soup.find_all('div', attrs={"id": re.compile('^message')})
        for mess in message_divs:
            if mess.find('div', {'class': 'from_name'}):
                name = mess.find('div', {'class': 'from_name'}).contents[0].strip()
            else: continue
            text = mess.find('div', {'class': 'text'}).getText() if mess.find('div', {'class': 'text'}) else ''
            chars = len(text)
            words = len(text.split())
            user_dict[name] = user_dict.get(name, 0)+1
        dict_list.append(user_dict)
    # Sum up the dictionaries
    counter = collections.Counter()
    for d in dict_list:
        counter.update(d)
    result = dict(counter)
    sorted_result = sorted(result.items(), reverse=True, key=lambda item: item[1])
    print(*sorted_result, sep = "\n")
