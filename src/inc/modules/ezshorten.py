'''
	Shorten and unshorten functions for the http://ezl.ink service
	by evilzone.org community.
	This module is for EZBot 
'''

from inc import *
from robobrowser import RoboBrowser
from robobrowser.forms.form import Form
import re, os
from urllib.parse import urlparse
import requests


modFunc.addCommand('shorten', 'ezshorten', 'shorten')
modFunc.addCommand('unshorten', 'ezshorten', 'unshorten')

def shorten(line, irc):
    try:
        message, username, msgto = ircFunc.ircMessage(line)
        if message[1]:
            url = message[1].strip().lower()
        #morons are too lazy to type out the URL scheme
        if urlparse(url).scheme == '': #rfc3987: parse(url, rule='URI')['scheme']
            url = 'http://{}'.format(url)
        try:
            #And i wonder if it is a valid URL
            tld = urlparse(url).netloc.split('.')[1]
        except IndexError as e:
            ircFunc.ircSay(msgto, '{0}, give me a valid URL to shorten. Louge off you skeleton pile..'.format(username))
            return
            
        #lay on the force bro.    
        browser = RoboBrowser(history=True)
        browser.open('http://ezl.ink/index.php')
        form = browser.get_form(0)
        assert isinstance(form, Form)

        form["url"] = url

        browser.submit_form(form)
        html = browser.parsed
    
        shorturl = re.findall('http[s]?://ezl.ink/[a-zA-Z0-9]+', str(html))
        ircFunc.ircSay(msgto, '{0}, shorturl: {1}'.format(username, shorturl[0]))
    except IndexError as e:
		#fricking no args
		ircFunc.ircSay(msgto, '{0}, give me a URL to shorten. Twart XD.'.format(username), irc)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)


    

def unshorten(line, irc):
    try:
        message, username, msgto = ircFunc.ircMessage(line)
        if message[1]:
            url = message[1].strip().lower()
        if urlparse(url).scheme == '':
		    url = 'http://{}'.format(url)
        shorturl = re.findall('http[s]?://ezl.ink/[a-zA-Z0-9]+', str(url))[0]
        if shorturl:
            r = requests.get(shorturl, allow_redirects = True)
            if r.url == 'http://ezl.ink/index.php' and 'The url doesn\'t exist.' in r.text:
                ircFunc.ircSay(msgto, '{0}, {1} doesn\'t exist in http://ezl.ink database, move on moron.'.format(username, shorturl))
                return
            ircFunc.ircSay(msgto '{0}, LongURL: {1}'.format(username, r.url), irc)
        else:
            ircFunc.ircSay(msgto, '{0}, that is no http://ezl.ink shortened url. Puddi\'s cousin. XD.'.format(username), irc)
    except IndexError as e:
		#fricking no args
		ircFunc.ircSay(msgto, '{0}, give me a URL to unshorten. Twart XD.'.format(username), irc)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)
