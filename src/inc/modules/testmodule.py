from inc import *

mainFunc.addCommand('commandhere', 'modulename', 'functionname')


def functionname(line, irc):
    splitline = line.split(" :")
    try:
        message = splitline[1]
        origmessage = message
        messagechars = message
        message = message.split(" ")
        username = line.split("!")[0].replace(':', '')
        msgto = line.split(" ")[2]
        command = message[0]
    except IndexError:
        errorhandling.inputError('information', e, line)
    except Exception:
        errorhandling.inputError('critical', e, line)
    to = msgto
    msg = origmessage.split(" ", 1)[1]
    ircFunc.ircSay(msgto, msg, irc)
