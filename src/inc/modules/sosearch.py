import requests  # maybe change to urllib2 ?
from bs4 import BeautifulSoup  # I'm fucked if I may not use that... jk

# BeastBot
from inc import *
modFunc.addCommand('sosearch', 'sosearch', 'sosearch')

BASE_URL = 'http://www.stackoverflow.com/search?q=QUERY'


def get_search_url(search):
    # craft an url for a search query and return it
    return BASE_URL.replace('QUERY', search.replace(' ', '+'))


def get_questions(url):
    # find all questions linked to from a search
    # result page and return their URLs
    txt = requests.get(url).content
    soup = BeautifulSoup(txt, 'lxml')
    questions = [link.get('href')
                 for link in soup.find_all('a')
                 if link.get('href') and
                 link.get('data-searchsession') and
                 link.get('href').startswith('/questions/')]
    return ['http://www.stackoverflow.com' + l for l in questions]


def sosearch(line, irc):
    # return all questions that are found based on a query
    message, username, msgto = ircFunc.ircMessage(line)
    query = '+'.join(message[1:]).strip()
    urls = get_questions(get_search_url(query))
    for q in urls[:1]:
        ircFunc.ircSay(msgto, q, irc)
