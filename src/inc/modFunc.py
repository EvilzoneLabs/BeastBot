import imp
import os
import mainFunc
import ircFunc
import errorhandling
import configFunc
import sqlite3
import sys
import importlib

'''
Module Management
'''

def ScanFolderForMods():
    path = 'inc/modules/'
    # Scans selcted folder for all files ending in .py
    files = os.listdir(path)
    imps = []
    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
                name = name[0]
                imps.append(name)
    file = open(path + '__init__.py', 'w')
    toWrite = '__all__ =' + str(imps)
    file.write(toWrite)
    file.close()
    return imps

def getHelp(command):
	con = sqlite3.connect('conf/conf.db')
	while con:
		cur = con.cursor()
		cur.execute("SELECT help FROM commands WHERE init='%s'" % command)
		row = cur.fetchone()
		break
	if row == None:
		return False
	else:
		return row[0]

def getCommand(command, loaded=None):
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        if loaded is not None:
            if loaded == True:
                loaded = 1
            else:
                loaded = 0
            cur.execute("SELECT * FROM commands WHERE init='%s' AND loaded='%s'" % (command, loaded))
        else:
            cur.execute("SELECT * FROM commands WHERE init='%s'" % command)
        row = cur.fetchone()
        break
    if row == None:
        return False, False
    elif row[2] == 1: # Means command is loaded
        if row[6] == 1: # Means command is enabled
            module = row[4]
            function = row[5]
            return module, function
    else:
        return False, False


def ScanModules():
    folder = 'inc/modules/'
    mods = ScanFolderForMods()
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT name FROM modules")
        rows = cur.fetchall()
    total = ''
    for row in rows:
        row = str(row)
        row = row.replace("(u'", '')
        row = row.replace("',)", ' ')
        total = total + row
    for mod in mods:
        if mod in total:
            mod = mod.strip()
            print 'module is aready in there... Setting exist flag on mod: ' + mod
            con = sqlite3.connect('conf/conf.db')
            with con:
                cur = con.cursor()
                cur.execute("UPDATE modules SET exist=1 WHERE name='" + mod + "'")
                con.commit()
        else:
            print "mod is not in there " + mod + " creting entry."
            con = sqlite3.connect('conf/conf.db')
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO modules VALUES('" + folder + "', 1, '" + mod + "', 0, 0)")
                con.commit()
    # Used at startup to find all modules and add to sql db if not already added... does not load them though


def addCommand(command, module, function, perm='', helpInfo=''):
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT init FROM commands WHERE init='%s' AND module='%s' AND function='%s'" % (command, module, function))
        row = cur.fetchone()
        break
    if row == None:
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT * FROM commands WHERE init='%s'")
            row = cur.fetchone()
            break
        if row != None:
            errorhandling.inputError('warning', 'Tried to load ' + command + ', but that command already exist.', 'Module: ' + module + ' - Function: ' + function)
        else:
            con = sqlite3.connect('conf/conf.db')
            while con:
                cur = con.cursor()
                cur.execute("INSERT INTO commands VALUES('%s', '%s', 1, '%s', '%s', '%s', 1)" % (helpInfo, perm, command, module, function))
                con.commit()
                break
    else:
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("UPDATE commands SET loaded=1 WHERE init='%s'" % command)
            cur.execute("UPDATE commands SET help='%s' WHERE init='%s'" % (helpInfo, command))
            cur.execute("UPDATE commands SET perm='%s' WHERE init='%s'" % (perm, command))
            con.commit()
            break


def LoadDefaultModules():
    module = {}
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT location, name FROM modules WHERE defaultload=1 AND exist=1")
        rows = cur.fetchall()
    for row in rows:
        location = str(row[0])
        modname = str(row[1])
        #Need to set the loaded flag
        con = sqlite3.connect('conf/conf.db')
        with con:
            cur = con.cursor()
            cur.execute("UPDATE modules SET loaded=1 WHERE name='%s' AND location='%s'" % (modname, location))
            con.commit()
        if location not in sys.path:
            sys.path.append(location)
        module[modname] = importlib.import_module(modname)
        print "Loaded: " + modname + " from: " + location + " sense it had the default load flag"
    # Ran after startup to load modules in sql db markes as load default
    return module


def purgeMods():
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM modules WHERE exist=0")
        con.commit()
    return con.total_changes

def purgeCommands():
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM commands WHERE loaded=0 AND enabled=1")
        con.commit()
    return con.total_changes


def reloadMods():
    ScanModules()
    module = {}
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT location, name FROM modules WHERE loaded=1 AND exist=1")
        rows = cur.fetchall()
    for row in rows:
        location = str(row[0])
        modname = str(row[1])
        print 'reloading: ' + modname + ' , ' + location
        if location not in sys.path:
            sys.path.append(location)
        module[modname] = importlib.import_module(modname)
        print "Reloaded: " + modname + " from: " + location
    return module

def defaultManage(name=None, mode=None):
    returnvar = False
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        if mode == 'add':
            cur.execute("UPDATE modules SET defaultload=1 WHERE name='%s'" % name)
            con.commit()
            returnvar = True
            break
        elif mode == 'del':
            cur.execute("UPDATE modules SET defaultload=0 WHERE name='%s'" % name)
            con.commit()
            returnvar = True
            break
        else:
            cur.execute("SELECT name FROM modules WHERE defaultload=1")
            rows = cur.fetchall()
            break
    if mode is not 'add' and mode is not 'del':
        returnvar = ''
        for row in rows:
            returnvar = returnvar + str(row[0]) + ', ' 
    return returnvar

def listMods(mode='loaded'):
    if mode == 'loaded':
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules WHERE loaded=1")
            rows = cur.fetchall()
            break
    elif mode == 'unloaded':
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules WHERE loaded=0 AND exist=1")
            rows = cur.fetchall()
            break
    elif mode == 'default':
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules WHERE defaultload=1")
            rows = cur.fetchall()
            break
    elif mode == 'exist':
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules WHERE exist=1")
            rows = cur.fetchall()
            break
    elif mode == 'all':
        con = sqlite3.connect('conf/conf.db')
        while con:
            cur = con.cursor()
            cur.execute("SELECT name FROM modules")
            rows = cur.fetchall()
            break
    else:
        return False
    returnvar = ''
    for row in rows:
        returnvar = returnvar + str(row[0]) + ', '
    return returnvar

def LoadModule(name):
    print 'attempting to load: ' + str(name)
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT location, name FROM modules WHERE name='" + name + "' AND exist=1 LIMIT 1")
        row = cur.fetchone()
        break
    if row == None:
        return False
    else:
        location = row[0]
        name = str(row[1])
        con = sqlite3.connect('conf/conf.db')
        with con:
            cur = con.cursor()
            cur.execute("UPDATE modules SET loaded=1 WHERE name='%s'" % (name))
            con.commit()
        if location not in sys.path:
            sys.path.append(location)
        importlib.import_module(name)
        try:
            mod = imp.load_source(name,"./%s%s.py" % (location, name))
        except Exception as e:
            errorhandling.inputError('critical', e, 'could not reload')
        print name + ' has been loaded succesfuly'
        return True


def returnModule():
    module = {}
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT location, name FROM modules WHERE exist=1 AND loaded=1")
        rows = cur.fetchall()
        break
    for row in rows:
        location = str(row[0])
        modname = str(row[1])
        if location not in sys.path:
            sys.path.append(location)
        module[modname] = importlib.import_module(modname)

    return module


def UnloadModule(name):
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("UPDATE commands SET loaded=0 WHERE module='%s'" % name)
        cur.execute("UPDATE modules SET loaded=0 WHERE name='%s'" % name)
        con.commit()
        break
