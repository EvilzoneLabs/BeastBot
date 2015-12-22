from inc import *
#from __future__ import with_statement
import re
import contextlib
from urllib import urlencode
from urllib2 import urlopen
import sys

modFunc.addCommand('tiny', 'tinyurl', 'getTiny')
modFunc.addCommand('tinygfm', 'tinyurl', 'tinyLMGTFY')
modFunc.addCommand('tinylmgtfy', 'tinyurl', 'tinyLMGTFY')
modFunc.addCommand('lmgtfy', 'tinyurl', 'tinyLMGTFY')


def getTiny(line, irc):
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    url = ' '.join(message[1:])
    if url != "":
        request_url = ('http://tinyurl.com/api-create.php?%s' % urlencode({'url':url}))
        with contextlib.closing(urlopen(request_url)) as response:
            ircFunc.ircSay(msgto, response.read().decode('utf-8'), irc)
        
def tinyLMGTFY(line, irc):
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    url = ' '.join(message[1:])
    url = 'http://lmgtfy.com/?q=' + url
    request_url = ('http://tinyurl.com/api-create.php?%s' % urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        ircFunc.ircSay(msgto, response.read().decode('utf-8'), irc)
