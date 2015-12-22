'''
    UrbanDictionary module for BeastBot
'''

from inc import *
import urllib
import json


modFunc.addCommand('ud', 'urban', 'urban')
modFunc.addCommand('urban', 'urban', 'urban')
modFunc.addCommand('wtf', 'urban', 'urban')

def urban(line, irc):
    splitline = line.split(" :")
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    try:
        if len(message) > 1:
            if msgto.lower() == configFunc.getBotConf('nickname').lower():
                msgto = username
            msg2 = message[1].lower()
            if msg2.strip():
                url = 'http://api.urbandictionary.com/v0/define?term=' + whole
                info = urllib.urlopen(url)
                try:
                    data = json.loads(info.read())
                    definition = data['list'][0]['definition'].replace("\n", " ").replace("\r", "")
                    thumbsup = data['list'][0]['thumbs_up']
                    thumbsdown = data['list'][0]['thumbs_down']
                    thumbsdown = str(thumbsdown)
                    thumbsup = str(thumbsup)
                    msg = whole.strip()
                    output = msg + ": " + definition + " Up: " + thumbsup + " Down: " + thumbsdown
                    ircFunc.ircSay(msgto, output, irc)
                except IndexError:
                    ircFunc.ircSay(msgto, 'No definition for: ' + whole, irc)
                except ValueError:
                    output = "Bad search term, bro"
                    # print output
                    ircFunc.ircSay(msgto, output, irc)
                except Exception, e:
                    errorhandling.errorlog('critical', e, line)
        else:
            output = "Please enter a search term"
            # print output
            ircFunc.ircSay(msgto, output, irc)
    except Exception, e:
        errorhandling.inputError('critical', e, line)
