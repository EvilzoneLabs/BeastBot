'''

Module Management module for BeastBot

'''

from inc import *


modFunc.addCommand('mod-load', 'modmanagement', 'modLoad', 'admin', 'The parameters for this command are: blah')
modFunc.addCommand('mod-list', 'modmanagement', 'modList', 'admin', 'this is another test')
modFunc.addCommand('mod-default', 'modmanagement', 'modDef', 'admin', 'testing this')
modFunc.addCommand('mod-def', 'modmanagement', 'modDef')
modFunc.addCommand('mod-unload', 'modmanagement', 'modUnload')

def modList(line, irc):
    message, username, msgto = ircFunc.ircMessage(line.strip())
    if username.lower() in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username.lower(), irc)):
            numArgs = len(message) - 1
            if numArgs > 0:
                if message[1].strip() == 'loaded':
                    loadedMods = modFunc.listMods('loaded')
                    ircFunc.ircSay(msgto, 'Loaded Modules: %s' % loadedMods, irc)
                elif message[1].strip() == 'unloaded':
                    unloadedMods = modFunc.listMods('unloaded')
                    ircFunc.ircSay(msgto, 'Unloaded Modules: %s' % unloadedMods, irc)
                elif message[1].strip() == 'default':
                    defaultMods = modFunc.defaultManage()
                    ircFunc.ircSay(msgto, 'Modules loaded by default: %s' % defaultMods, irc)
                elif message[1].strip() == 'all':
                    existMods = modFunc.listMods('exist')
                    ircFunc.ircSay(msgto, 'Existant Modules: %s' % existMods, irc)
                else:
                    ircFunc.ircSay(msgto, 'Parameters for this command are: loaded, unloaded, default, all', irc)
            else:
                    ircFunc.ircSay(msgto, 'Parameters for this command are: loaded, unloaded, default, all', irc)

def modLoad(line, irc):
    message, username, msgto = ircFunc.ircMessage(line.strip())
    if username.lower() in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username.lower(), irc)):
            numArgs = len(message) - 1
            if numArgs > 0:
                if message[1].strip() != "":
                    result = modFunc.LoadModule(message[1].strip())
                    if result:
                        ircFunc.ircSay(msgto, 'Module (%s) has been loaded successfully' % message[1].strip(), irc)
                    else:
                        ircFunc.ircSay(msgto, 'Could not load module: %s. It either does not exist, or something went wrong.' % message[1].strip(), irc)
                else:
                    ircFunc.ircSay(msgto, '%s, you must specify a module to load.' % username, irc)
            else:
                ircFunc.ircSay(msgto, '%s, you must specify a module to load.' % username, irc)
                

def modUnload(line, irc):
    message, username, msgto = ircFunc.ircMessage(line.strip())
    if username.lower() in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username.lower(), irc)):
            numArgs = len(message) - 1
            if numArgs > 0:
                if message[1].strip() != "":
                    modFunc.UnloadModule(message[1].strip())
                    ircFunc.ircSay(msgto, 'Module has been unloaded.', irc)
                else:
                    ircFunc.ircSay(msgto, 'You must specify a module to unload.', irc)
            else:
                ircFunc.ircSay(msgto, 'You must specify a module to unload.', irc)
                

def modDef(line, irc):
    message, username, msgto = ircFunc.ircMessage(line.strip())
    if username.lower() in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username.lower(), irc)):
            numArgs = len(message) - 1
            if numArgs > 1:
                if message[1].strip() == 'add':
                    modFunc.defaultManage(message[2].strip(), 'add')
                    ircFunc.ircSay(msgto, '%s, has been added to the Default Load List.' % message[2].strip(), irc)
                elif message[1].strip() == 'del':
                    modFunc.defaultManage(message[2].strip(), 'del')
                    ircFunc.ircSay(msgto, '%s, has been removed from the Default Load List.' % message[2].strip(), irc)
                else:
                    ircFunc.ircSay(msgto, 'The arguments for this command are: add <moduleName> OR del <moduleName>', irc)
            else:
                ircFunc.ircSay(msgto, 'The arguments for this command are: add <moduleName> OR del <moduleName>', irc)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                
                    
