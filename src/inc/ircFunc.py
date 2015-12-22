import select
import mainFunc
import errorhandling
import configFunc
import time
from multiprocessing import Process, Manager
import socket
import sqlite3

def ircMode(chan, args, irc):
    irc.send("MODE %s %s\r\n" % (chan, args))


def ircSay(to, msg, irc):
#to=message to, msg=message to send, irc=socket
    irc.send("PRIVMSG %s :%s\r\n" % (to, msg))


def ircJoin(channel, irc):
#channel=channel to join, irc=socket
    channel = channel.strip()
    irc.send("JOIN %s\r\n" % (channel))
    oldchans = configFunc.getBotConf('tempchannels')
    if channel not in oldchans.split(" "):
        newchans = oldchans + " " + channel
        configFunc.setBotConf('tempchannels', newchans)


def ircPart(channel, irc):
#channel=channel to part, irc=socket
    channel = channel.strip()
    irc.send("PART %s\r\n" % (channel))
    oldchans = configFunc.getBotConf('tempchannels')
    newchans = oldchans.replace(channel, '')
    configFunc.setBotConf('tempchannels', newchans)


def ircNick(newnick, irc):
#newnick=New nickname for the bot, irc=socket
    irc.send("NICK %s\r\n" % (newnick))
    configFunc.setBotConf('tempnickname', newnick)


def ensureRegDB():
    import os
    if not os.path.isfile('conf/reg.db'):
        con = sqlite3.connect('conf/reg.db')
        while con:
            cur = con.cursor()
            cur.execute('''CREATE TABLE entries
                (nick TEXT,
                status TEXT,
                rec TEXT);''')
            con.commit()
            break

def regStatus(nick):
    nick = nick.lower()
    con = sqlite3.connect('conf/reg.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT * FROM entries WHERE nick='%s'" % nick)
        row = cur.fetchone()
        break
    if row == None:
        return "ERROR"
    else:
        status = row[1]
        if status == 'None':
            return None
        else:
            return status

def updateReg(nick, state):
    nick = nick.lower()
    con = sqlite3.connect('conf/reg.db')
    while con:
        cur = con.cursor()
        cur.execute("UPDATE entries SET status='%s' WHERE nick='%s'" % (state, nick))
        con.commit()
        break
    return True

def regSetRec(nick, state):
    nick = nick.lower()
    con = sqlite3.connect('conf/reg.db')
    try:
        while con:
            cur = con.cursor()
            cur.execute("DELETE FROM entries WHERE nick='%s'" % nick)
            con.commit()
            break
    except IndexError:
        pass
    if state:
        while con:
            cur = con.cursor()
            cur.execute("INSERT INTO entries (nick, status, rec) VALUES ('%s', 'None', 'True')" % nick)
            con.commit()
            break
    return True


def isRegged(nick, irc, sentline=False):
    nick = nick.lower()
    regSetRec(nick, True)
    start = True
    a = 0
    while start:
        a = a + 1
        if a > 3:
            return False
        i = 0
        ircSay("NickServ", "STATUS %s " % (nick,), irc)
        while i < 10:
            regstatus = regStatus(nick)
            if regstatus != None:
                if regstatus == "ERROR":
                    print 'something failed with a error getting the regstatus'
                if regstatus.lower() == 'true':
                    return True
                else:
                    return False
            i = i + 1
            time.sleep(0.1)
                


def isRegged2(nick, irc, sentline=False):
    """Function to check is user is identified with nickserv.
        true if Nickserv says he's registered."""
    #return True
    irc2 = irc
    irc2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
    received = False
    line = ""
    while received == False:
        ircSay("NickServ", "STATUS %s " % (nick), irc2)
        ircSay("NickServ", "STATUS %s " % (nick), irc2)
        ircSay("NickServ", "STATUS %s " % (nick), irc2)
        #ircSay("NickServ", "STATUS %s " % (nick), irc)
        #ircSay("NickServ", "STATUS %s " % (nick), irc)
        #ready = select.select([irc], [], [], 3)
        #if ready[0]:
        #line = irc.recv(256)
        line = irc2.recv(256)
        if ("STATUS %s" % nick) in line and getUsername(line).lower() == 'nickserv':
            received = True
    print "REG TEST" + line
    if line.find("STATUS %s 3" % (nick)) != -1 and getUsername(line).lower() == 'nickserv':
        irc2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return True
    else:
        if sentline is not False:
            errorhandling.inputAccess(info='Not identified to NickServ', line=sentline)
        else:
            errorhandling.inputAccess(info='Not identified to NickServ', username=nick)
        irc2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return False


def announce(message, username, irc):
    print 'in ircfunc func'
    message = ' '.join(message[1:])
    message = "ANOUNCEMENT FROM: " + str(username) + " - " + str(message)
    for channel in configFunc.getBotConf('tempchannels').strip().split(" "):
        ircSay(channel, message, irc)


def getMsgto(line, convert=True):
    msgto = line.split(" ")[2]
    if msgto == configFunc.getBotConf('tempnickname') and convert is True:
        msgto = getUsername(line)
    return msgto


def getUsername(line):
    return line.split("!")[0][1:].lower()


def ircMessage(line, whl=False):
    """Func to process message received from server."""
    splitline = line.split(" :")
    try:
        origmessage = splitline[1]
        message = origmessage.split(" ")
        username = getUsername(line).lower()
        if getMsgto(line) == configFunc.getBotConf('tempnickname'):
        # privmsg
            msgto = username
        else:
            msgto = getMsgto(line)
        if whl:
            parts = origmessage.split(" ", 1)
            if (len(parts) > 1):
                whole = parts[1]
            else:
                whole = ""
            return message, whole, username, msgto
        return message, username, msgto
    except IndexError as e:
        errorhandling.inputError('information', e, line)
    except Exception as e:
        errorhandling.inputError('critical', e, line)
