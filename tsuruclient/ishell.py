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
import sys
import cmdln
try:
    import readline
except:
    readline = None

import apps   
import auth
import key

from configs import TARGET_FN, IDENT, DefaultTarget
from utils import minargs_required


class ITsuru(cmdln.Cmdln):
    name = "tsuru"

    def __init__(self):
        cmdln.Cmdln.__init__(self)
        self._get_target()
        self.intro  = "Welcome to tsuru console! Current target is: %s ." % self.target ## defaults to None

        #self.apps = apps.AppManager(self.target)
        #self.auth = auth.AuthManager(self.target)

    def get_optparser(self):
        parser = cmdln.Cmdln.get_optparser(self)
        parser.add_option("-s", "--shell", action="store_true", 
            help="enter interactive shell")
        return parser

    def _get_target(self):
        fn = TARGET_FN
        if os.path.exists(fn):            
            with open(fn) as f:
                self.target = f.read().strip()
        else:
            self.target = DefaultTarget    

    def do_target(self, subcmd, opts, *args):
        '''Get or set target.\nUsage: target [url]'''
        fn = TARGET_FN
        if len(args) < 1:
            self._get_target()            
        else:
            # write target
            target = args.strip()
            with open(fn, 'w') as f:
                f.write(target)
            self.target = target
            print("Set target as %s success." % target)
        print("Current target is: %s ." % self.target)

    ################## User commands ####################

    @minargs_required(1)
    def do_user_create(self, subcmd, opts, *args):
        '''Creates a user.\nUsage: user_create <email>'''
        # check email is valid
        # create a user with email
        email = self.argx[0]
        am = auth.AuthManager(self.target)
        am.createUser(email)

    def do_user_remove(self, subcmd, opts, *args):
        '''Removes your user from server.'''
        am = auth.AuthManager(self.target)
        am.removeUser()

    @cmdln.alias("lgi")
    @cmdln.option("-p", action="store_true", dest="password")
    @minargs_required(1)
    def do_login(self, subcmd, opts, *args):
        '''Login to server.

        Usage: 
            login <email>

        ${cmd_option_list}
        ''' 
        email = self.argx[0]
        am = auth.AuthManager(self.target)
        am.login(email)
        return 

    @cmdln.alias("lgo")
    def do_logout(self, subcmd, opts, *args):
        '''Clear local authentication credentials.

        Usage: 
            logout

        ${cmd_option_list}
        '''
        am = auth.AuthManager(self.target)
        am.logout()

    def do_change_password(self, subcmd, opts, *args):
        '''Change your password.\nUsage: change_password'''
        am = auth.AuthManager(self.target)
        am.changePassword()

    @minargs_required(0)
    def do_user_add_key(self, subcmd, opts, *args):
        '''Add your public key ($HOME/.ssh/tsuru_id_rsa.pub by default).\nUsage: user_add_key [path/to/key/file.pub]
        '''
        km = key.KeyManager(self.target)
        if len(self.argx) > 0:
            fn = self.argx[0]            
            km.add(fn)
        else:
            km.add()

    @minargs_required(0)
    def do_user_remove_key(self, subcmd, opts, *args):
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
    def do_team_create(self, subcmd, opts, *args):
        '''Creates a new team.\nUsage: team_create <name>'''
        name = self.argx[0]
        am = auth.AuthManager(self.target)
        am.createTeam(name)        

    @minargs_required(1)
    def do_team_remove(self, subcmd, opts, *args):
        '''Removes a team from tsuru server.\nUsage: team_remove <name>'''
        name = self.argx[0]
        am = auth.AuthManager(self.target)
        am.removeTeam(name)

    @minargs_required(2)
    def do_team_user_add(self, subcmd, opts, *args):
        '''adds a user to a team.\nUsage: team_user_add <teamname> <useremail>
        '''
        x = self.argx
        tname, uname = x[0], x[1]
        am = auth.AuthManager(self.target)
        am.addTeamUser(tname, uname)

    def do_team_list(self, subcmd, opts, *args):
        '''List all teams that you are member.\nUsage: team_list
        '''
        am = auth.AuthManager(self.target)
        am.listTeam()

    ################## App commands ####################
    def do_app_list(self, subcmd, opts, *args):
        '''Get a list of all apps.\nUsage: app_list
        '''
        apm = apps.AppManager(self.target)
        apm.list()

    @minargs_required(2)
    def do_app_create(self, subcmd, opts, *args):
        '''Create an app.\nUsage: app_create <name> <framework> 
        '''
        #x = minargs_check(args, 2)
        #if self.argx is not None:
        x = self.argx 
        name, framework = x[0], x[1]
        apm = apps.AppManager(self.target)
        apm.create(name, framework)

    @minargs_required(1)
    def do_app_info(self, subcmd, opts, *args):
        """Show information about your app.\nUsage: app_info <appname>
        """
        name = self.argx[0]
        apm = apps.AppManager(self.target)
        apm.get(name)

    @minargs_required(1)
    def do_app_remove(self, subcmd, opts, *args):
        """Remove an app.\nUsage: app_remove <appname>
        """
        name = self.argx[0]
        apm = apps.AppManager(self.target)
        apm.remove(name)

    @minargs_required(1)
    def do_app_unit_add(self, subcmd, opts, *args):
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
    def do_app_unit_remove(self, subcmd, opts, *args):
        """Remove units from an app.\nUsage: app_unit_remove <appname> [numunits=1]
        """
        aname = self.argx[0]
        if len(self.argx) > 1:
            numunits = self.argx[1]
        else:
            numunits = 1
        apm = apps.AppManager(self.target)
        apm.unitremove(aname, numunits)

    @cmdln.alias("anot", "an")
    @cmdln.option("-a", action="store_true", dest="all")
    @cmdln.option("-c", action="store_true", dest="changenums")
    @cmdln.option("-q", action="store_true", dest="quiet")
    def do_annotate(self, subcmd, opts, *args):
        """Print file lines along with their revisions"""
        print "p4 %s: opts=%s action=%r" % (subcmd, opts, args)


if __name__ == '__main__':
    console = ITsuru()
    sys.exit(console.main(argv=sys.argv, loop=cmdln.LOOP_NEVER))
## end of http://code.activestate.com/recipes/280500/ }}}
