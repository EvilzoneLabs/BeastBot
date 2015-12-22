'''
    SEEN module for BeastBot
'''
from inc import *
import sqlite3
import time, os
import datetime
import pytz


db_file = 'db/seen.db'

def init():
    if not os.path.exists(db_file.split('/')[0]):
        os.mkdir('db')
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM Karma')
    except StandardError:
        c.execute('CREATE TABLE IF NOT EXISTS seen_values(nick TEXT, channel TEXT, message TEXT, time INTEGER)')
        conn.commit()
    conn.close()


init()


modFunc.addCommand('seen', 'seen', 'seen')
modFunc.addCommand('seen_record', 'seen', 'set_seen_values')

def seen(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    try:
        if message[1]:
            nick = message[1].strip().lower()
            values = get_seen_value(nick)
            if values[0] == msgto:
                channel = 'here'
            else:
                channel = 'another channel' #not mentioning channels for privacy

            lastmsg = values[1]
            time_seen = values[2]

            timestamp = format_time(time_seen)
            ircFunc.ircSay(msgto, 'I last saw {0} on {1} in {2} saying: "{3}"'.format(nick, timestamp, channel, lastmsg), irc)
    except TypeError as e:
        ircFunc.ircSay(msgto, 'Sorry, i haven\'t seen {0} around.'.format(nick), irc)
    except IndexError as e:
        ircFunc.ircSay(msgto, '{0}, seen who?'.format(username), irc)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)

def set_seen_values(nick, channel, message, time):
    nick = nick.lower()
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    with conn:
        c.execute('SELECT * FROM seen_values WHERE nick=?',[nick])
        result=c.fetchone()
        if result is not None:
            c.execute('UPDATE seen_values SET channel=?, message=?, time=? WHERE nick=?', [channel, message, time, nick])
        else:
            c.execute('INSERT INTO seen_values VALUES (?, ?, ?, ?)',[nick, channel, message, time])
        conn.commit()
    
def get_seen_value(nick):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    with conn:
        c.execute('SELECT channel, message, time FROM seen_values WHERE nick=?', [nick])
        result = c.fetchone()
        return result

def format_time(timestamp):
    tformat = '%Y-%m-%d @ %H:%M:%S'
    return datetime.datetime.fromtimestamp(timestamp).strftime(tformat)
