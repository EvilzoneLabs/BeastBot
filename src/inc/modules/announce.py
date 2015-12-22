from inc import *

modFunc.addCommand('announce', 'announce', 'announceInit')

def announceInit(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if message[1]:
                    ircFunc.announce(message, username, irc)
            except IndexError:
                ircFunc.ircSay(msgto, 'You did not enter a announcement to make', irc)
            except Exception as e:
                errorhandling.inputError('critical', e, line)
