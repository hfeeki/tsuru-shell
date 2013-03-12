# -*- coding: utf-8 -*-
#!/usr/bin/env python

## 
## Author:   Michael
## Date:     27 April 2013
## Version:  1.0
## 
## Copyright (c) 2013, Michael


import os
import sys
from libs import cmdln

from cmds import apps   
from cmds import users
from cmds import keys
from cmds import envs
from cmds import services

from configs import TARGET_FN, TOKEN_FN, CUSER_FN, DefaultTarget, WORK_HOME
from configdb import cfgdb
from utils import minargs_required, getCurrentUser, isLoggedIn
from libs.icolor import cformat

'''
$ python ishell.py t
   local     http://127.0.0.1:8080
 * develop   http://192.168.33.10:8080
   Test      http://localhost:6000
'''
class ITsuru(cmdln.Cmdln):
    name = "tsuru"
    #prompt = "tsuru> "

    def __init__(self):
        cmdln.Cmdln.__init__(self)
        dt = cfgdb.get_default_target()
        self.target_name = dt['name']
        self.target = dt['url']
        self.prompt = self._getPrompt()
        self.intro  = cformat('''#BLUE;                                     
   ----------------------------------------------------------
   |        ______   _____    __  __   ____     __  __      |
   |       /_  __/  / ___/   / / / /  / __ \   / / / /      |
   |        / /     \__ \   / / / /  / /_/ /  / / / /       |
   |       / /     ___/ /  / /_/ /  / _, _/  / /_/ /        |
   |      /_/     /____/   \____/  /_/ |_|   \____/         |
   |                                                        |
   ----------------------------------------------------------
    Welcome! Current target is: %s - %s \n\n''' % (self.target_name, self.target)) ## defaults to None

    def _getPrompt(self):
        import urlparse        
        t = self.target = cfgdb.get_default_target()['url']
        netloc = urlparse.urlparse(t).netloc
        u = getCurrentUser()
        prompt = self.prompt
        if isLoggedIn():
            prompt = cformat("#GREEN;[%s@%s]tsuru> " % (u, netloc))
        else:
            prompt = cformat("#GREEN;[@%s]tsuru> " % (netloc))
        return prompt

    def postcmd(self, argv):
        self.prompt = self._getPrompt()

    @cmdln.alias("w", "wel")
    def do_welcome(self, subcmd, opts, *args):
        '''Show the welcome banner.
        '''
        print(self.intro)

    @cmdln.alias("t", "target")
    def do_target_get(self, subcmd, opts, *args):
        '''Get or set target.

        Usage: 
            target 
            or
            target_get 

        '''
        ts = cfgdb.get_targets()
        for t in ts:
            if t['default']:
                print("%2s %-10s%s" % ('*', t['name'], t['url']))
            else:
                print("%2s %-10s%s" % (' ', t['name'], t['url']))        

    @cmdln.alias("ta")
    @cmdln.option("-d", "--default", action="store_true", dest="default")
    @minargs_required(2)
    def do_target_add(self, subcmd, opts, *args):
        '''Add a new named target.

        Usage:
            target_add <name> <url> [-d]

        ${cmd_option_list}
        '''
        name, url = args[0], args[1]
        if opts.default :
            cfgdb.add_target(name, url, True)
        else:
            cfgdb.add_target(name, url)

    @cmdln.alias("tr")
    @minargs_required(1)
    def do_target_remove(self, subcmd, opts, *args):
        '''Remove a named target.

        Usage:
            target_remove <name>

        Note:
            You can provide name or url or both of them. If both provided, only url will be used.

        ${cmd_option_list}
        '''
        name = args[0]
        cfgdb.remove_target(name)


    @cmdln.alias("tds")
    @minargs_required(1)
    def do_target_default_set(self, subcmd, opts, *args):
        '''Set a named target as the only default.

        Usage:
            target_default_set <name> 
        '''
        name = args[0]
        cfgdb.set_default_target(name)
        
    @cmdln.alias("dt", "tdg")
    def do_target_default_get(self, subcmd, opts, *args):
        '''Get the default target.

        Usage:
            target_default_get 
        '''
        x = cfgdb.get_default_target()
        if x:
            print("%2s %-10s%s" % ('*', x['name'], x['url']))

    ################## User commands ####################

    @cmdln.alias("ul")
    def do_user_list(self, subcmd, opts, *args):
        '''List local users.

        Usage:
            user_list 
        '''
        us = cfgdb.get_users()
        for x in us:
            if x['default']:
                print("%2s %-10s%s" % ('*', x['name'], x['email']))
            else:
                print("%2s %-10s%s" % (' ', x['name'], x['email'])) 

    @cmdln.alias("uc")
    @minargs_required(2)
    def do_user_create(self, subcmd, opts, *args):
        '''Creates a user.

        Usage: 
            user_create <username> <email>
        '''
        # check email is valid
        # create a user with email
        user, email = args[0], args[1]
        am = users.AuthManager(self.target)
        am.createUser(user, email)

    @cmdln.alias("ur")
    def do_user_remove(self, subcmd, opts, *args):
        '''Removes your user from server.

        Usage:
            user_remove 
        '''
        am = users.AuthManager(self.target)
        am.removeUser()

    @cmdln.alias("lgi")
    @minargs_required(2)
    def do_login(self, subcmd, opts, *args):
        '''Login to server.

        Usage: 
            login <username> <email>

        ${cmd_option_list}
        ''' 
        name, email = args[0], args[1]
        am = users.AuthManager(self.target)
        am.login(name, email)
        # TODO: change the prompt
        return 

    @cmdln.alias("lgo")
    def do_logout(self, subcmd, opts, *args):
        '''Clear local authentication credentials.

        Usage: 
            logout

        ${cmd_option_list}
        '''
        am = users.AuthManager(self.target)
        am.logout()
        # TODO: change the prompt
        self.prompt = self._getPrompt()
        return

    @cmdln.alias("cp")
    def do_change_password(self, subcmd, opts, *args):
        '''Change your password.

        Usage: 
            change_password
        '''
        am = users.AuthManager(self.target)
        am.changePassword()

    @cmdln.alias("st", "s")
    def do_status(self, subcmd, opts, *args):
        """Display current login state.

        Usage:
            status 
        """
        am = users.AuthManager(self.target)
        am.status()

    @cmdln.alias("cu")
    def do_user_current(self, subcmd, opts, *args):
        """Show current user.
        """
        am = users.AuthManager(self.target)
        am.getCurrentUser()        

    @cmdln.alias("uka")
    @minargs_required(0)
    def do_user_key_add(self, subcmd, opts, *args):
        '''Add your public keys ($HOME/.ssh/tsuru_id_rsa.pub by default).

        Usage: 
            user_add_key [path/to/keys/file.pub]
        '''
        km = keys.KeyManager(self.target)
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
        km = keys.KeyManager(self.target)
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
        am = users.AuthManager(self.target)
        am.createTeam(name)        

    @cmdln.alias("tr")
    @minargs_required(1)
    def do_team_remove(self, subcmd, opts, *args):
        '''Removes a team from tsuru server.

        Usage: 
            team_remove <name>
        '''
        name = args[0]
        am = users.AuthManager(self.target)
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
        am = users.AuthManager(self.target)
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
        am = users.AuthManager(self.target)
        am.removeTeamUser(tname, uname)

    @cmdln.alias("tl")
    def do_team_list(self, subcmd, opts, *args):
        '''List all teams that you are member.

        Usage: 
            team_list
        '''
        am = users.AuthManager(self.target)
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

    @cmdln.alias("aes")
    @cmdln.option("-a", "--app", dest="app")
    @cmdln.option("-v", "--vars", dest="vars")
    def do_app_env_set(self, subcmd, opts, *args):
        """Set environment variables for an app.

        Usage: 
            app_env_set <--app appname> <--vars NAME=value [NAME=value] ...>  
        """        
        em = envs.EnvManager(self.target)
        em.set(opts.app, opts.vars)

    @cmdln.alias("aeg")
    @cmdln.option("-a", "--app", dest="app")
    @cmdln.option("-v", "--vars", dest="vars")
    def do_app_env_get(self, subcmd, opts, *args):
        """Retrieve environment variables for an app.

        Usage: 
            app_env_get <--app appname> <--vars ENVIRONMENT_VARIABLE1 [ENVIRONMENT_VARIABLE2] ...>
        """        
        em = envs.EnvManager(self.target)
        em.get(opts.app, options.vars)   

    @cmdln.alias("aeu")
    @cmdln.option("-a", "--app", dest="app")
    @cmdln.option("-v", "--vars", dest="vars")
    def do_app_env_unset(self, subcmd, opts, *args):
        """Unset environment variables for an app.

        Usage: 
            app_env_unset <--app appname> <--vars ENVIRONMENT_VARIABLE1 [ENVIRONMENT_VARIABLE2] ...>
        """        
        em = envs.EnvManager(self.target)
        em.unset(opts.app, options.vars)   

    #################### Service commands ####################

    @cmdln.alias("sa")
    @minargs_required(2)
    def do_service_add(self, subcmd, opts, *args):
        '''Create a service instance to one or more apps make use of.

        Usage: 
            service-add <servicename> <instancename>

            e.g.:
                $ tsuru service_add mongodb tsuru_mongodb

            Will add a new instance of the "mongodb" service, named "tsuru_mongodb".
        '''
        sm = services.ServiceManager(self.target)
        svcname, instname = args[0], args[1]
        sm.add(svcname, instname)

    @cmdln.alias("sl")
    def do_service_list(self, subcmd, opts, *args):
        '''Get all available services, and user's instances for this services.

        Usage:
            service_list 
        '''
        sm = services.ServiceManager(self.target)
        sm.list()

    @cmdln.alias("sb")
    @minargs_required(2)
    def do_service_bind(self, subcmd, opts, *args):
        '''Bind a service instance to an app.

        Usage:
            service_bind <instancename> <appname>
        '''
        sm = services.ServiceManager(self.target)
        instname, appname = args[0], args[1]
        sm.bind(instname, appname)

    @cmdln.alias("sub")
    @minargs_required(2)
    def do_service_unbind(self, subcmd, opts, *args):
        '''Unbind a service instance from an app.

        Usage:
            service_unbind <instancename> <appname>
        '''
        sm = services.ServiceManager(self.target)
        instname, appname = args[0], args[1]
        sm.unbind(instname, appname)

    @cmdln.alias("ss", "sst")
    @minargs_required(1)
    def do_service_status(self, subcmd, opts, *args):
        '''Check status of a given service instance.

        Usage:
            service_status <instancename>
        '''
        sm = services.ServiceManager(self.target)
        instname = args[0]
        sm.status(instname)

    @cmdln.alias("si")
    @minargs_required(1)
    def do_service_info(self, subcmd, opts, *args):
        '''List all instances of a service.

        Usage:
            service_info <servicename>
        '''
        sm = services.ServiceManager(self.target)
        svcname = args[0]
        sm.info(svcname)

    @cmdln.alias("sd")
    @minargs_required(1)
    def do_service_doc(self, subcmd, opts, *args):
        '''Show documentation of a service.

        Usage:
            service_doc <servicename>
        '''
        sm = services.ServiceManager(self.target)
        svcname = args[0]
        sm.doc(svcname)

    #################### Misc commands ####################

    @cmdln.alias("x", "q", "quit")
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


def main():
    # setup our working environments
    if not os.path.exists(WORK_HOME):
        os.mkdir(WORK_HOME)

    console = ITsuru()
    sys.exit(console.main(argv=sys.argv, loop=cmdln.LOOP_IF_EMPTY))


if __name__ == '__main__':
    main()
    
## end of http://code.activestate.com/recipes/280500/ }}}
