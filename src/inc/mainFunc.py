import sys
import socket
import sqlite3
import os
import importlib
import ircFunc
import errorhandling
import configFunc

def CreateSocket(server, port):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    irc.connect((server, int(port)))
    return irc


def Auth(username, nickname, realname, irc):
    irc.send('NICK %s\r\n' % nickname)
    configFunc.setBotConf('tempnickname', nickname)
    irc.send('USER %s %s %s :%s\r\n' % (username, nickname, nickname, realname))
