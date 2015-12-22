from inc import *
import re


modFunc.addCommand('join', 'botadministration', 'join')
modFunc.addCommand('part', 'botadministration', 'part')
modFunc.addCommand('nick', 'botadministration', 'changenick')
modFunc.addCommand('set', 'botadministration', 'set')


def set(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username.lower() in configFunc.getBotConf('botadmins').lower().split(" "):
        if (ircFunc.isRegged(username, irc, line)):
            try:
                if message[1].strip() == '':
                    del message[1]
                if message[1].strip() == 'admin':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            CurrentAdmins = configFunc.getBotConf('botadmins')
                            NewAdmins = str(CurrentAdmins) + ' ' + str(message[3])
                            NewAdmins = NewAdmins.lower()
                            configFunc.setBotConf('botadmins', NewAdmins)
                            out = 'Admin list updated to: ' + NewAdmins
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'del':
                            CurrentAdmins = configFunc.getBotConf('botadmins')
                            NewAdmins = CurrentAdmins.replace(message[3].strip(), '')
                            configFunc.setBotConf('botadmins', NewAdmins)
                            out = 'Admin list updated to: ' + NewAdmins
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'list':
                            AdminList = configFunc.getBotConf('botadmins')
                            out = ('Bot admins are: %s' % AdminList)
                            ircFunc.ircSay(msgto, out, irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set admin' are: add, del, list"
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.inputError('critical', e, line)
                if message[1].strip() == 'botban':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            CurrentBans = configFunc.getBotConf('botbanned')
                            NewBans = str(CurrentBans) + ' ' + str(message[3])
                            modFunc.setBotConf('botbanned', NewBans)
                            out = 'Ban list updated to: ' + NewBans
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'del':
                            CurrentBans = configFunc.getBotConf('botbanned')
                            NewBans = CurrentBans.replace(message[3].strip(), '')
                            configFunc.setBotConf('botbanned', NewBans)
                            out = 'Ban list updated to: ' + NewBans
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'list':
                            BanList = configFunc.getBotConf('botbanned')
                            if BanList.strip() == "":
                                out = "There are currently no nicks banned from the bot..."
                            else:
                                out = "Current nicks banned from the bot: " + BanList
                            ircFunc.ircSay(msgto, out, irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set ban' are: add, del, list"
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.inputError('critical', e, line)
                elif message[1].strip() == 'channel':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            if re.search(',0', message[3]):
                                ircFunc.ircSay(msgto, 'No.... Just.... No......', irc)
                            else:
                                CurrentChannels = configFunc.getBotConf('channels')
                                NewChannels = str(CurrentChannels) + ' ' + str(message[3])
                                configFunc.setBotConf('channels', NewChannels)
                                out = 'Channel list updated to: ' + NewChannels
                                ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'del':
                            CurrentChannels = configFunc.getBotConf('channels')
                            NewChannels = CurrentChannels.replace(message[3].strip(), '')
                            configFunc.setBotConf('channels', NewChannels)
                            out = 'Channel list updated to: ' + NewChannels
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'list':
                            Channels = configFunc.getBotConf('channels')
                            out = ("Current default channels: %s" % Channels)
                            ircFunc.ircSay(msgto, out, irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set channel' are: add, del, list"
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.inputError('critical', e, line)
                elif message[1].strip() == 'nick':
                    try:
                        configFunc.setBotConf('nick', message[2])
                        ircFunc.ircSay(msgto, 'Default nickname set to: ' + message[2], irc)
                    except IndexError:
                        out = "You did not specify a new default nickname..."
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.inputError('critical', e, line)
                else:
                    del message[1]
                    print message[1]
            except IndexError:
                out = "Options for 'set' are: admin, channel, nick"
                ircFunc.ircSay(msgto, out, irc)
            except Exception as e:
                errorhandling.inputError('critical', e, line)


def changenick(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username.lower() in configFunc.getBotConf('botadmins').lower().split(" "):
        if (ircFunc.isRegged(username, irc, line)):
            try:
                if message[1]:
                    ircFunc.ircNick(message[1], irc)
                    print message[1]
            except IndexError:
                ircFunc.ircNick(configFunc.getBotConf('nickname'), irc)
            except Exception as e:
                errorhandling.inputError('critical', e, line)


def part(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username.lower() in configFunc.getBotConf('botadmins').lower().split(" "):
        if (ircFunc.isRegged(username, irc, line)):
            try:
                if message[1]:
                    ircFunc.ircPart(message[1], irc)
            except IndexError:
                ircFunc.ircSay(msgto, "No channel specified...", irc)
            except Exception as e:
                errorhandling.inputError('critical', e, line)


def join(line, irc):
    try:
        message, username, msgto = ircFunc.ircMessage(line)
        if username.lower() in configFunc.getBotConf('botadmins').lower().split(" "):
            if (ircFunc.isRegged(username, irc, line)):
                try:
                    if re.search(',0', message[1]):
                        ircFunc.ircSay(msgto, 'No....', irc)
                    elif message[1]:
                        ircFunc.ircJoin(message[1], irc)
                except IndexError:
                    splitchannels = configFunc.getBotConf('channels').split(" ")
                    for chan in splitchannels:
                        ircFunc.ircJoin(chan, irc)
                except Exception as e:
                    errorhandling.inputError('critical', e, line)
    except Exception as e:
        errorhandling.inputError('critical', e, line)
