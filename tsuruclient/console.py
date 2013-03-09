#!/usr/bin/env python
# -*- coding: utf-8 -*-

## {{{ http://code.activestate.com/recipes/280500/ (r1)
## console.py
## Author:   James Thiele
## Date:     27 April 2004
## Version:  1.0
## Location: http://www.eskimo.com/~jet/python/examples/cmd/
## Copyright (c) 2004, James Thiele

import os
import cmd
try:
    import readline
except:
    readline = None

import apps   
import auth
import key

from configs import TARGET_FN, IDENT
from utils import minargs_required

class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        if not readline :
            self.completekey = None
        self.prompt = "(tsuru)> "
        self.intro  = "Welcome to tsuru console!" ## defaults to None

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e


DefaultTarget = "http://tsuru.plataformas.glb.com:8080"


class ITsuru(Console):

    def __init__(self):
        Console.__init__(self)
        self._get_target()
        self.intro  = "Welcome to tsuru console! Current target is: %s ." % self.target ## defaults to None

        #self.apps = apps.AppManager(self.target)
        #self.auth = auth.AuthManager(self.target)

    def _get_target(self):
        fn = TARGET_FN
        if os.path.exists(fn):            
            with open(fn) as f:
                self.target = f.read().strip()
        else:
            self.target = DefaultTarget    

    def do_target(self, arg):
        fn = TARGET_FN
        if len(arg) < 1:
            self._get_target()            
        else:
            # write target
            target = arg.strip()
            with open(fn, 'w') as f:
                f.write(target)
            self.target = target
            print("Set target as %s success." % target)
        print("Current target is: %s ." % self.target)

    def help_target(self):
        print("Get or set target.\nUsage: target [url]")

    ################## User commands ####################

    @minargs_required(1)
    def do_user_create(self, args):
        '''Creates a user.\nUsage: user_create <email>'''
        # check email is valid
        # create a user with email
        email = self.argx[0]
        am = auth.AuthManager(self.target)
        am.createUser(email)

    def do_user_remove(self, args):
        '''Removes your user from server.'''
        am = auth.AuthManager(self.target)
        am.removeUser()

    @minargs_required(1)
    def do_login(self, args):
        '''Login to server.\nUsage: login <email>
        ''' 
        email = self.argx[0]
        am = auth.AuthManager(self.target)
        am.login(email)
        return 

    def do_logout(self, args):
        '''Clear local authentication credentials.\nUsage: logout
        '''
        am = auth.AuthManager(self.target)
        am.logout()

    def do_change_password(self, args):
        '''Change your password.\nUsage: change_password'''
        am = auth.AuthManager(self.target)
        am.changePassword()

    @minargs_required(0)
    def do_user_add_key(self, args):
        '''Add your public key ($HOME/.ssh/tsuru_id_rsa.pub by default).\nUsage: user_add_key [path/to/key/file.pub]
        '''
        km = key.KeyManager(self.target)
        if len(self.argx) > 0:
            fn = self.argx[0]            
            km.add(fn)
        else:
            km.add()

    @minargs_required(0)
    def do_user_remove_key(self, args):
        '''Remove your public key ($HOME/.ssh/tsuru_id_rsa.pub by default).\nUsage: user_remove_key [path/to/key/file.pub]
        '''
        km = key.KeyManager(self.target)
        if len(self.argx) > 0:
            fn = self.argx[0]            
            km.remove(fn)
        else:
            km.remove()

    ################## Team commands ####################

    @minargs_required(1)
    def do_team_create(self, args):
        '''Creates a new team.\nUsage: team_create <name>'''
        name = self.argx[0]
        am = auth.AuthManager(self.target)
        am.createTeam(name)        

    @minargs_required(1)
    def do_team_remove(self, args):
        '''Removes a team from tsuru server.\nUsage: team_remove <name>'''
        name = self.argx[0]
        am = auth.AuthManager(self.target)
        am.removeTeam(name)

    @minargs_required(2)
    def do_team_user_add(self, args):
        '''adds a user to a team.\nUsage: team_user_add <teamname> <useremail>
        '''
        x = self.argx
        tname, uname = x[0], x[1]
        am = auth.AuthManager(self.target)
        am.addTeamUser(tname, uname)

    def do_team_list(self, args):
        '''List all teams that you are member.\nUsage: team_list
        '''
        am = auth.AuthManager(self.target)
        am.listTeam()

    ################## App commands ####################
    def do_app_list(self, args):
        '''Get a list of all apps.\nUsage: app_list
        '''
        apm = apps.AppManager(self.target)
        apm.list()

    @minargs_required(2)
    def do_app_create(self, args):
        '''Create an app.\nUsage: app_create <name> <framework> 
        '''
        #x = minargs_check(args, 2)
        #if self.argx is not None:
        x = self.argx 
        name, framework = x[0], x[1]
        apm = apps.AppManager(self.target)
        apm.create(name, framework)

    @minargs_required(1)
    def do_app_info(self, args):
        """Show information about your app.\nUsage: app_info <appname>
        """
        name = self.argx[0]
        apm = apps.AppManager(self.target)
        apm.get(name)

    @minargs_required(1)
    def do_app_remove(self, args):
        """Remove an app.\nUsage: app_remove <appname>
        """
        name = self.argx[0]
        apm = apps.AppManager(self.target)
        apm.remove(name)

    @minargs_required(1)
    def do_app_unit_add(self, args):
        """Add a new unit to an app.\nUsage: app_unit_add <appname> [numunits=1]
        """
        aname = self.argx[0]
        if len(self.argx) > 1:
            numunits = self.argx[1]
        else:
            numunits = 1
        apm = apps.AppManager(self.target)
        apm.unitadd(aname, numunits)

    @minargs_required(1)
    def do_app_unit_remove(self, args):
        """Remove units from an app.\nUsage: app_unit_remove <appname> [numunits=1]
        """
        aname = self.argx[0]
        if len(self.argx) > 1:
            numunits = self.argx[1]
        else:
            numunits = 1
        apm = apps.AppManager(self.target)
        apm.unitremove(aname, numunits)

    


if __name__ == '__main__':
    console = ITsuru()
    console . cmdloop() 
## end of http://code.activestate.com/recipes/280500/ }}}
