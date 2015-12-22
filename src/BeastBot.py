import re
import time
import os
from multiprocessing import Process, Manager
import sys
import importlib
#from inc.modules.urlparsing import urlparse


# Should relocate this and make it configurable on the fly
debuging = True

def main():
    global conf
    global module
    # Connect to the socket
    irc = mainFunc.CreateSocket(conf['server'], conf['port'])
    # Authenticate to the IRC server
    mainFunc.Auth(conf['username'], conf['nickname'], conf['realname'], irc)
    botRunning = True
    
    # Loads the forum parser script
    if os.path.isfile('inc/constantModules/forumparser.py'):
        location = 'inc/constantModules'
        sys.path.append(location)
        forumparser = importlib.import_module('forumparser')
        functionProc = Process(target=forumparser.startTheParser, args=(irc,))
        functionProc.daemon = True
        functionProc.start()
        
    while botRunning:
        try:
            line = irc.recv(512)
        except Exception:
            # Bot disconnected
            errorhandling.inputInfo('Bot disconnected unexpectedly')
            # Attempt to restart
            botRunning = False
            errorhandling.inputInfo('Restarting bot: Failure to receive')
            irc.close()
            os.system('./restart.sh')
            # Bot shouldnt go past this point
            errorhandling.inputInfo('Bot failed restarting due to failure to receive. Reached the line it wasnt suppose to.')
            exit()

        if line and debuging == True:
            print line

        if line[0:4] == "PING":
            # Receives PING from server and sends back PONG
            irc.send("PONG " + line.split(" :")[1])
        elif re.search("PING :", line):
            irc.send("PONG " + line.split(" :")[1])
            try:
                # Sometimes ping messages get sent on the same line.
                irc.send("PONG " + line.split(" :")[2])
            except IndexError:
                pass
                # This is normal
            except Exception as e:
                errorhandling.inputError('critical', e, line)

        if ("STATUS") in line and ircFunc.getUsername(line).lower() == 'nickserv':
            if re.search(" 3 " , line):
                ircFunc.updateReg(line.split(" ")[4].strip(), True)
            else:
                ircFunc.updateReg(line.split(" ")[4].strip(), False)
        try:
            # Checks if user is banned from using the bot. If not it proceeds
            username = ircFunc.getUsername(line).lower()
            if username.lower() not in conf['botbanned'].lower().split(" "):
                # Checks whether something remotely looking like an URL is in
                # the line.
                '''
                This is the new url parsing.. It is having issues currently.... 
                Commented out and using old version for now.
                if 'http://' in line and line.split()[1] == 'PRIVMSG':
                    s = 0
                    while s != -1:
                        print line
                        s = line.find('http://', s)
                        print s
                        e = line.find(' ', s)
                        print e
                        #url = line[s:e].strip()
                        url = line[s:e]
                        message, username, msgto = ircFunc.ircMessage(line)
                        print 'in while s= %s e = %s' % (s, e)
                        print 'url = .%s.' % url
                        urlparse(url, msgto, irc)
                        s = e
                # Checks if the command starts with the command initializer
                '''
                '''
                if line.split(" ")[3][1:5] == "http":
                    try:
                        line = line.replace("http", "!http")
                    except Exception:
                        pass
                '''
                if line.split(" ")[3][1:5] == "http":
                    try:
                        line = line.replace("http", "!http")
                    except Exception:
                        pass
                if line.split(" ")[3][1] == conf['cominit']:
                    command = line.split(" ")[3][2:]
                    command = command.strip()
                    if command[0:4] == 'http':
                        command = 'http'
                    try:
                        if command[0:4] == 'help':
                            topic = line.split(" ")[4]
                            topic = topic.strip()
                            helpInfo = modFunc.getHelp(topic)
                            if helpInfo == False:
                                ircFunc.ircSay(ircFunc.getMsgto(line), 'Command does not exist.', irc)
                            elif helpInfo == '':
                                ircFunc.ircSay(ircFunc.getMsgto(line), 'There is no help for this command.', irc)
                            else:
                                ircFunc.ircSay(ircFunc.getMsgto(line), helpInfo, irc)
                        else:
                            # Gets information for the command to run
                            mod, function = modFunc.getCommand(command, loaded=True)
                            # If command doesnt exist, mod will equal Boolean False
                            if mod != False:
                                # Sense the command exists... RUN IT
                                try:
                                    functionProc = Process(target=getattr(module[mod], function), args=(line, irc,))
                                    functionProc.daemon = True
                                    functionProc.start()
                                except KeyError:
                                    module[mod] = importlib.import_module(mod)
                                    functionProc = Process(target=getattr(module[mod], function), args=(line, irc,))
                                    functionProc.daemon = True
                                    functionProc.start()
                                except Exception as e:
                                    errorhandling.inputError('critical', e, line)
                            else:
                                # Command did not exist
                                # Proceed with admin functions
                                # This is not in a module sense there are commands such as !quit and !restart
                                # Child processes can not close the parent process
                                if username in conf['botadmins'].lower().split(" "):
                                    # Checks if user is a admin
                                    if ircFunc.isRegged2(username, irc):
                                        # makes sure user is identified with nickserv
                                        if command == 'quit':
                                            # Disconnects and closes the bot
                                            errorhandling.inputInfo('Quiting: Command directed by: ' + username)
                                            botRunning = False
                                            irc.close()
                                            exit()
                                        elif command == 'update':
                                            # Makes the bot pull the newest source from github and then restart
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Shutting down for updates....', irc)
                                            botRunning = False
                                            errorhandling.inputInfo('Shutting down for updates: Command directed by: ' + username)
                                            irc.close()
                                            os.system('./pullupdates.sh')
                                            # Bot shouldnt go past this point
                                            errorhandling.inputError('critical', 'Bot failed updating by command. Reached the line it wasnt suppose to.', line)
                                            exit()
                                        elif command == 'restart':
                                            # Disconnects and restarts the bot
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Restarting bot...', irc)
                                            botRunning = False
                                            errorhandling.inputInfo('Restarting bot: Command directed by: ' + username)
                                            irc.close()
                                            os.system('./restart.sh')
                                            # Bot shouldnt go past this point
                                            errorhandling.inputError('critical', 'Bot failed restarting by command. Reached the line it wasnt suppose to.', line)
                                            exit()
                                        elif command == 'gitpull':
                                            # Just pulls newest source from github
                                            # Does not restart
                                            errorhandling.inputInfo("Pulling from git : Command directed by: " + username)
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Pulling from github.', irc)
                                            os.system('git pull')
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Done pulling from github', irc)
                                        elif command == 'reload':
                                            # Currently does nothing useful....
                                            # Would like this to reload modules on the fly with newest source.
                                            del module
                                            module = modFunc.reloadMods()
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Done reloading all modules', irc)
                                        elif command == 'modmanage-load':
                                            # Loads the module management module
                                            result = modFunc.LoadModule('modmanagement')
                                            if result == True:
                                                ircFunc.ircSay(msgto, 'Module has been loaded successfully', irc)
                                            else:
                                                ircFunc.ircSay(msgto, 'Either the module does not exist or something went wrong and it was NOT loaded successfully.', irc)
                                        elif command == 'purge':
                                            # Purges the module database and deletes old modules that no longer exist
                                            errorhandling.inputInfo("STARTING THY PURGE!!!!!!!! : Command directed by: " + username)
                                            modFunc.purgeMods()
                                            modFunc.purgeCommands()
                                            errorhandling.inputInfo("Purge has finished")
                                            ircFunc.ircSay(ircFunc.getMsgto(line), 'Finished purging commands and modules', irc)
                    except Exception, e:
                        errorhandling.inputError('critical', e, line)

                elif re.match("^:[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9\-\.]+\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU) 001 " + conf['tempnickname'] + " :Welcome", line):
                    # When connected to the server and authed, we can now join the default channels.
                    splitchannels = conf['channels'].split(" ")
                    for chan in splitchannels:
                        ircFunc.ircJoin(chan, irc)

                elif re.search(":This nickname is registered and protected.", line):
                    # When told by nickserv that the bot is not identified, its sends nickserv the password
                    ircFunc.ircSay("NICKSERV", "identify " + conf['nickservpassword'], irc)

                elif line[0:20] == "ERROR :Closing Link:":
                    # Something went wrong and the bot disconnected
                    # Attempts to reconnect
                    errorhandling.inputInfo("Bot disconnected due to ping timeout...")
                    errorhandling.inputInfo('Reconnecting in 30 seconds...')
                    time.sleep(30)
                    errorhandling.inputInfo("Reconnecting now....")
                    # Connect to the socket
                    irc = mainFunc.CreateSocket(conf['server'], conf['port'])
                    # Authenticate to the IRC server
                    mainFunc.Auth(conf['username'], conf['nickname'], conf['realname'], irc)
            msgto = ircFunc.getMsgto(line, convert=False)
            if msgto.lower() == conf['tempnickname'].lower():
                if username.lower() not in "nickserv chanserv hostserv".split(" "):
                    # Logs private messages to the bot
                    # Used to make sure no one is messing with it
                    functionProc = Process(target=privlog.input, args=(line,))
                    functionProc.daemon = True
                    functionProc.start()
            
            if line.split()[1] == 'KICK' and line.split()[3] == conf['tempnickname']:
                # Rejoin the channel when kicked
                ircFunc.ircJoin(line.split()[2], irc)
            
            if line.split()[1] == 'PRIVMSG' and line.split()[2] != conf['tempnickname']:
                # seen module recording
                # It ignores PMs to the bot for the seen module
                try:
                    command = 'seen_record'
                    mod, function = modFunc.getCommand(command, loaded=True)
                    # Checks if the module is loaded
                    # If the module is not loaded then do nothing
                    if mod != False:
                        nick = re.search(':(.*)!', line.lower().split()[0]).group(1)
                        nick = nick.strip()
                        channel = line.lower().split()[2]
                        msg = ' '.join(line.lower().split()[3:])[1:]
                        try:
                            functionProc = Process(target=getattr(module[mod], function), args=(nick, channel, msg, time.time()))
                            functionProc.daemon = True
                            functionProc.start()
                        except KeyError:
                            module[mod] = importlib.import_module(mod)
                            functionProc = Process(target=getattr(module[mod], function), args=(nick, channel, msg, time.time()))
                            functionProc.daemon = True
                            functionProc.start()
                        except Exception as e:
                            errorhandling.inputError('critical', e, line)
                except Exception, e:
                    errorhandling.inputError('critical', e)
        except IndexError:
            # Command does not exist
            # Ignore
            pass
        except Exception, e:
            errorhandling.inputError('critical', e, line)


def LocalUpdateConf(conf):
    # Keep the variables updated with the configuration from the database
    # Allows us to dynamically set channels, admins, bans etc....
    while True:
        a = configFunc.getAllBotConf()
        for key, value in a.iteritems():
            conf[key] = value
        time.sleep(5)


if __name__ == "__main__":
    # Writes imports from inc/ to inc/__init__.py
    file = open('inc/__init__.py', 'w')
    includeFiles = "__all__ =['mainFunc', 'ircFunc', 'errorhandling', 'configFunc', 'modFunc', 'privlog']"
    file.write(includeFiles)
    file.close()
    # Includes *.py files from inc/
    from inc import *
    # Makes sure configuration exists and if not creates it
    configFunc.ensureConf()
    ircFunc.ensureRegDB()
    # Cleans temp nick and chans
    configFunc.CleanTemps()
    # Sets modules exist to 0
    configFunc.CleanModulesDB()
    # Sets commands exist to 0
    configFunc.CleanCommandsDB()
    # Finds loaded modules and marks them as exist = 1
    modFunc.ScanModules()
    # Loads modules marked as Default Load
    module = modFunc.LoadDefaultModules()

    manager = Manager()
    conf = manager.dict()
    conf['conf'] = 'conf'
    functionProc = Process(target=LocalUpdateConf, args=(conf,))
    functionProc.daemon = True
    functionProc.start()

    # Sleep to provide time to grab the conf
    print '5'
    time.sleep(1)
    print '4'
    time.sleep(1)
    print '3'
    time.sleep(1)
    print '2'
    time.sleep(1)
    print '1'

    main()
