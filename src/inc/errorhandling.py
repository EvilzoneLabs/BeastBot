import ConfigParser
import time
import sys
import traceback
import mainFunc
import ircFunc
import os


def errorinfo():
    info = traceback.extract_tb(sys.exc_info()[-1])
    info = str(info)
    info = ''.join(info)
    info = info.replace("[('", '').replace("')]", '').replace("'", '')
    info = info.split(",")
    var = {}
    var['filename'] = info[0]
    var['linenumber'] = info[1]
    var['functionname'] = info[2]
    var['linetext'] = info[3]
    return var


def log(level, message, info, additional=None):
    try:
        additional = additional.strip('\n').strip('\r')
    except Exception:
        pass
    date = time.strftime("%Y-%m-%d")
    file = open('log/%s.log' % (date), 'a')
    log = level
    log = log + ' - ' + time.strftime("%H:%M:%S")
    log = log + ' - ' + message
    log = log + ' - Filename: ' + info['filename']
    log = log + ' - Line Number: ' + info['linenumber']
    log = log + ' - Function: ' + info['functionname']
    log = log + ' - Line Text: ' + info['linetext']
    if additional:
        log = log + ' - Additional Information: ' + additional
    file.write(log + "\n")
    file.close()


def inputError(option, message, additional=None):
    info = errorinfo()
    message = str(message)
    option = option.upper()
    log(option, message, info, additional)


def inputInfo(info):
    info = str(info)
    date = time.strftime("%Y-%m-%d")
    logtime = time.strftime("%H:%M:%S")
    file = open("log/%s.log" % (date), 'a')
    output = logtime + " - " + info
    file.write(output + "\n")
    file.close()


def ensureAccessDir():
    date = time.strftime("%Y-%m-%d")
    if not os.path.isdir('log/AccessViolations'):
        print 'Making Invalid Access Directory'
        os.system('mkdir log/AccessViolations')
    if not os.path.isdir('log/AccessViolations/%s' % date):
        print 'Making Access Invalid Date Dir'
        os.system('mkdir log/AccessViolations/%s' % date)


def inputAccess(info=False, line=False, username=False):
    date = time.strftime("%Y-%m-%d")
    logtime = time.strftime("%H:%M:%S")
    ensureAccessDir()
    if line != False:
        message, whole, username, msgto = ircFunc.ircMessage(line, whl=True)
        message = ' '.join(message)
        message = str(message)
        username = username.strip().replace("\n", '')
        message = message.strip().replace("\n", '')
        line = str(line)
        line = line.strip().replace("\n", "")
        output = 'INVALID-ACCESS: ' + logtime + " - Username: " + username
        output = output + " - Command: " + message + " - MsgTo: " + msgto
        if info is not False: 
            output = output + " - Reason: " + info
        output = output + " ---- Raw: " + line
    else:
        output = 'INVALID-ACCESS: ' + logtime + " - Username: " + username
        if info is not False:
            output = output + " - Reason: " + info

    file = open("log/AccessViolations/%s/%s-INVALID-ACCESS.log" % (date, username), 'a')
    file.write(output + "\n")
    file.close()
