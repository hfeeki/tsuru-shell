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
import env

from configs import TARGET_FN, IDENT, DefaultTarget
from utils import minargs_required


class ITsuru(cmdln.Cmdln):
    name = "tsuru"
    #prompt = "tsuru> "

    def __init__(self):
        cmdln.Cmdln.__init__(self)
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

    @cmdln.alias("t")
    def do_target(self, subcmd, opts, *args):
        '''Get or set target.

        Usage: 
            target [url]
        '''
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

    @cmdln.alias("uc")
    @minargs_required(1)
    def do_user_create(self, subcmd, opts, *args):
        '''Creates a user.

        Usage: 
            user_create <email>
        '''
        # check email is valid
        # create a user with email
        email = args[0]
        am = auth.AuthManager(self.target)
        am.createUser(email)

    @cmdln.alias("ur")
    def do_user_remove(self, subcmd, opts, *args):
        '''Removes your user from server.

        Usage:
            user_remove 
        '''
        am = auth.AuthManager(self.target)
        am.removeUser()

    @cmdln.alias("lgi")
    @minargs_required(1)
    def do_login(self, subcmd, opts, *args):
        '''Login to server.

        Usage: 
            login <email>

        ${cmd_option_list}
        ''' 
        email = args[0]
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

    @cmdln.alias("cp")
    def do_change_password(self, subcmd, opts, *args):
        '''Change your password.

        Usage: 
            change_password
        '''
        am = auth.AuthManager(self.target)
        am.changePassword()

    @cmdln.alias("st", "s")
    def do_status(self, subcmd, opts, *args):
        """Display current login state.

        Usage:
            status 
        """
        am = auth.AuthManager(self.target)
        am.status()

    @cmdln.alias("uka")
    @minargs_required(0)
    def do_user_key_add(self, subcmd, opts, *args):
        '''Add your public key ($HOME/.ssh/tsuru_id_rsa.pub by default).

        Usage: 
            user_add_key [path/to/key/file.pub]
        '''
        km = key.KeyManager(self.target)
        if len(args) > 0:
            fn = args[0]            
            km.add(fn)
        else:
            km.add()

    @cmdln.alias("ukr")
    @minargs_required(0)
    def do_user_key_remove(self, subcmd, opts, *args):
        '''Remove your public key ($HOME/.ssh/tsuru_id_rsa.pub by default).

        Usage: 
            user_key_remove [path/to/key/file.pub]
        '''
        km = key.KeyManager(self.target)
        if len(args) > 0:
            fn = args[0]            
            km.remove(fn)
        else:
            km.remove()

    ################## Team commands ####################

    @cmdln.alias("tc")
    @minargs_required(1)
    def do_team_create(self, subcmd, opts, *args):
        '''Creates a new team.

        Usage: 
            team_create <name>
        '''
        name = args[0]
        am = auth.AuthManager(self.target)
        am.createTeam(name)        

    @cmdln.alias("tr")
    @minargs_required(1)
    def do_team_remove(self, subcmd, opts, *args):
        '''Removes a team from tsuru server.

        Usage: 
            team_remove <name>
        '''
        name = args[0]
        am = auth.AuthManager(self.target)
        am.removeTeam(name)

    @cmdln.alias("tua")
    @minargs_required(2)
    def do_team_user_add(self, subcmd, opts, *args):
        '''Adds a user to a team.

        Usage: 
            team_user_add <teamname> <useremail>
        '''
        x = args
        tname, uname = x[0], x[1]
        am = auth.AuthManager(self.target)
        am.addTeamUser(tname, uname)

    @cmdln.alias("tur")
    @minargs_required(2)
    def do_team_user_remove(self, subcmd, opts, *args):
        '''Removes a user from a team.

        Usage: 
            team_user_remove <teamname> <useremail>
        '''
        x = args
        tname, uname = x[0], x[1]
        am = auth.AuthManager(self.target)
        am.removeTeamUser(tname, uname)

    @cmdln.alias("tl")
    def do_team_list(self, subcmd, opts, *args):
        '''List all teams that you are member.

        Usage: 
            team_list
        '''
        am = auth.AuthManager(self.target)
        am.listTeam()

    ################## App commands ####################

    @cmdln.alias("al")
    def do_app_list(self, subcmd, opts, *args):
        '''Get a list of all apps.

        Usage: 
            app_list
        '''
        apm = apps.AppManager(self.target)
        apm.list()

    @cmdln.alias("ac")
    @minargs_required(2)
    def do_app_create(self, subcmd, opts, *args):
        '''Create an app.

        Usage: 
            app_create <name> <framework> 
        '''
        #x = minargs_check(args, 2)
        #if args is not None:
        x = args 
        name, framework = x[0], x[1]
        apm = apps.AppManager(self.target)
        apm.create(name, framework)

    @cmdln.alias("ai")
    @minargs_required(1)
    def do_app_info(self, subcmd, opts, *args):
        """Show information about your app.

        Usage: 
            app_info <appname>
        """
        name = args[0]
        apm = apps.AppManager(self.target)
        apm.get(name)

    @cmdln.alias("ar")
    @minargs_required(1)
    def do_app_remove(self, subcmd, opts, *args):
        """Remove an app.

        Usage: 
            app_remove <appname>
        """
        name = args[0]
        apm = apps.AppManager(self.target)
        apm.remove(name)

    @cmdln.alias("aua")
    @minargs_required(1)
    def do_app_unit_add(self, subcmd, opts, *args):
        """Add a new unit to an app.

        Usage: 
            app_unit_add <appname> [numunits=1]
        """
        aname = args[0]
        if len(args) > 1:
            numunits = args[1]
        else:
            numunits = 1
        apm = apps.AppManager(self.target)
        apm.unitadd(aname, numunits)

    @cmdln.alias("aur")
    @minargs_required(1)
    def do_app_unit_remove(self, subcmd, opts, *args):
        """Remove units from an app.

        Usage: 
            app_unit_remove <appname> [numunits=1]
        """
        aname = args[0]
        if len(args) > 1:
            numunits = args[1]
        else:
            numunits = 1
        apm = apps.AppManager(self.target)
        apm.unitremove(aname, numunits)

    @cmdln.alias("es")
    @cmdln.option("-a", "--app", dest="app")
    def do_env_set(self, subcmd, opts, *args):
        """Set environment variables for an app.

        Usage: 
            env-set <--app appname> <NAME=value> [NAME=value] ... 
        """        
        parser = self.get_optparser()
        (options, argx) = parser.parse_args()
        app = options.app 
        em = env.EnvManager(self.target)
        em.set(app, argx)

    @cmdln.alias("eg")
    @cmdln.option("-a", "--app", dest="app")
    def do_env_get(self, subcmd, opts, *args):
        """Retrieve environment variables for an app.

        Usage: 
            env-get <--app appname> [ENVIRONMENT_VARIABLE1] [ENVIRONMENT_VARIABLE2] ...
        """        
        parser = self.get_optparser()
        (options, argx) = parser.parse_args()
        app = options.app 
        em = env.EnvManager(self.target)
        em.get(app, argx)   

    @cmdln.alias("eu")
    @cmdln.option("-a", "--app", dest="app")
    def do_env_unset(self, subcmd, opts, *args):
        """Unset environment variables for an app.

        Usage: 
            env-unset <--app appname> <ENVIRONMENT_VARIABLE1> [ENVIRONMENT_VARIABLE2] ... [ENVIRONMENT_VARIABLEN]
        """        
        parser = self.get_optparser()
        (options, argx) = parser.parse_args()
        app = options.app 
        em = env.EnvManager(self.target)
        em.unset(app, argx)   

    ################## Misc commands ####################

    @cmdln.alias("quit")
    def do_exit(self, subcmd, opts, *args):
        """Exit/Quit the interactive shell"""
        self.stdout.write('\n')
        self.stdout.flush()
        self.stop = True

    @cmdln.alias("!", "sh")
    def do_shell(self, subcmd, opts, *args):
        """Pass command to a system shell when line begins with '!'"""
        import string
        os.system(string.join(args))



if __name__ == '__main__':
    console = ITsuru()
    sys.exit(console.main(argv=sys.argv, loop=cmdln.LOOP_IF_EMPTY))
## end of http://code.activestate.com/recipes/280500/ }}}
