from inc import *
import urllib2
import string
import re

modFunc.addCommand('http', 'urlparsing', 'urlparse')


def urlparse(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    message[0] = message[0].replace("!http", "http")
    good = False
    try:
        sock = urllib2.urlopen(message[0], timeout=4)
        html = sock.read()
        sock.close()
        start = html.find('<title>') + 7
        titletest = html.find('<title>')
        titletest2 = html[titletest:]
        titletest2 = titletest2[0:7]
        if titletest2 == '<title>':
            good = True
        end = html.find('</title>', start)
        title = html[start:end]
        title = title.strip()
        if title != "" and good:
            title = title.strip()
            title = filter(lambda x: x in string.printable, title)
            title = title[0:100]
            output = "Title: [ " + title + " ]"
            ircFunc.ircSay(msgto, output, irc)
    except IndexError as e:
        errorhandling.inputError('information', e, line)
    except Exception as e:
        errorhandling.inputError('critical', e, line)
