import time
import sys
import mainFunc
import ircFunc
import os


def ensureDir(username):
    if not os.path.isdir('log/privlog/%s' % (username)):
        print 'making dir ' + username
        os.system('mkdir log/privlog/%s' % (username))


def input(log):
    log = str(log)
    log = log.strip('\r')
    log = log.strip('\n')
    username = ircFunc.getUsername(log)
    # Makes sure sever is not sending message
    if " " not in username:
        ensureDir(username)
        date = time.strftime("%Y-%m-%d")
        logtime = time.strftime("%H:%M:%S")
        file = open("log/privlog/%s/%s.log" % (username, date), 'a')
        output = logtime + " - " + log
        file.write(output + "\n")
        file.close()
