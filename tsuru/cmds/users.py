# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import json
import requests
import getpass

from tsuru.utils import login_required
from tsuru.configdb import MyConfigDb

class AuthManager(object):

    def __init__(self, target, dbn):
        self.target = target
        self.dbn = dbn  # must set it, login_required will use it
        self.cfgdb = MyConfigDb.Instance(dbn)

    def createUser(self, username, email):        
        password = getpass.getpass("Please input your password: ")
        confirm = getpass.getpass("Confirm: ")
        if password != confirm:
            print "Passwords didn't match."
            return None         
        data = {
            "email": email,
            "password": password,
        }
        response = requests.post(
            "{0}/users".format(self.target),
            data=json.dumps(data)
        )
        if response.ok:
            print "User '%s' successfully created!" % email
        else:
            print "User '%s' failed to created! Reason: %s" % (email, response.content)

    @login_required
    def removeUser(self):
        """removes your user from tsuru server.
        """
        # http DELETE http://127.0.0.1:7080/user/user2@gmail.com
        q = "Are you sure you want to remove your user from tsuru? (y/n) "
        a = raw_input(q)
        if a == "n" or a == "N":
            print("Abort.")
            return
        response = requests.delete(
            "{0}/users".format(self.target),
            headers = self.auhd            
        )
        if response.ok:
            # remove local token record
            x = self.cfgdb.get_default_user()
            if x and x['email'] and x['token']:
                self.cfgdb.remove_user(name=x['name'], email=x['email'], token=x['token'])
            print "Remove user successfully!" 
        else:
            print "Remove user failed!\nReason: %s" % (response.content)

    def login(self, name, email):
        '''Login to server.
        '''
        # http POST http://127.0.0.1:8080/users/xbee@outlook.com/tokens password=fq9798
        # if token file exists
        if self.cfgdb.is_user_loggedin(name):
            a = raw_input("It looks like you have logged in, Do you realy want to login again? (y/n) ").strip()
            if a == 'n' or a == 'N':
                print("Abort.")
                return 
        password = getpass.getpass("Please input your password: ")
        data = {
            "password": password
        }
        response = requests.post(
            "{0}/users/{1}/tokens".format(self.target, email),
            data=json.dumps(data)
        )
        if response.ok:            
            # write it to $HOME/.tsuru_token
            c = response.json()['token']
            self.cfgdb.add_user(name, email, c, True)
            print("Successfully logged in!")
        else:
            print("Failed to logged in!\nReason: %s" % response.content)

    def logout(self):
        '''Clear default user's local authentication credentials.'''
        x = self.cfgdb.get_default_user()
        if x and x['email'] and x['token']:
            self.cfgdb.remove_user(name=x['name'], email=x['email'])
            print("Successfully logged out!")
        else:
            print("You're not logged in!")

    def status(self):
        x = self.cfgdb.get_default_user()
        if x and x['email'] and x['token']:
            print("You: %s have logged into %s !" % (x['name'], self.target))
        else:
            print("You're not logged in!")

    def getCurrentUser(self):
        x = self.cfgdb.get_default_user()
        if x:
            print("Current user is: %s, email: %s" % (x['name'], x['email']))
            return x
        else:
            print("There is no default user.")
            return None
     
    @login_required   
    def createTeam(self, name):
        '''creates a new team.
        '''
        # http POST http://127.0.0.1:8080/teams name=TEST Authorization:TOKEN
        data = {
            "name": name
        }
        response = requests.post(
            "{0}/teams".format(self.target),
            data=json.dumps(data),
            headers = self.auhd
        )
        if response.ok:
            print "Team '%s' successfully created!" % name
        else:
            print "Team '%s' failed to create!\nReason: %s" % (name, response.content)

    @login_required
    def removeTeam(self, name):
        '''removes a team from tsuru server.
        '''
        # http DELETE http://127.0.0.1:8080/teams/TEST Authorization:TOKEN           
        q = "Are you sure you want to remove team ? (y/n) "
        a = raw_input(q).strip()
        if a == "n" or a == "N":
            print("Abort")
            return 
        if a == "y" or a == "Y":            
            response = requests.delete(
                "{0}/teams/{1}".format(self.target, name),
                headers = self.auhd
            )
            if response.ok:
                print "Remove team '%s' successfully!" % name
            else:
                print "Remove team '%s' failed!\nReason: %s" % (name, response.content)
            return 

    @login_required
    def addTeamUser(self, tname, uname):
        '''adds a user to a team.\nUsage: addteamuser <teamname> <useremail>
        '''
        response = requests.put(
            "{0}/teams/{1}/{2}".format(self.target, tname, uname),
            headers = self.auhd
        )
        if response.ok:
            print("Successfully add user %s to team %s." % (uname, tname))
        else:
            print("Failed to add user %s to team %s.\nReason: %s" % (uname, tname, response.content))

    @login_required
    def removeTeamUser(self, tname, uname):
        '''removes a user from a team.
        '''
        response = requests.put(
            "{0}/teams/{1}/{2}".format(self.target, tname, uname),
            headers = self.auhd
        )
        if response.ok:
            print("Successfully remove user %s from team %s." % (uname, tname))
        else:
            print("Failed to remove user %s from team %s.\nReason: %s" % (uname, tname, response.content))

    @login_required
    def listTeam(self):
        '''List all teams that you are member.
        '''
        # http GET http://192.168.33.10:8080/teams Authorization:c6af13c174b1
        response = requests.get(
            "{0}/teams".format(self.target),
            headers = self.auhd
        )
        if response.ok:
            if len(response.content.strip()) == 0:
                print(" name")
                print("======")
                return 
            else:
                # list all of teams
                ts = response.json()
                print(" name")
                print("======")
                for x in ts:
                    print(' ' + x['name'])
        else:
            print("Failed to list all of teams.\nReason: %s" % response.content) 

    @login_required
    def changePassword(self):
        cp = getpass.getpass("Current password: ")
        np = getpass.getpass("New password: ")
        ncp = getpass.getpass("Confirm: ")
        if np != ncp: 
            print("New password and password confirmation didn't match.")
            return 
        data = {
            "old": cp,
            "new": np
        }
        response = requests.put(
            "{0}/users/password".format(self.target), 
            data=json.dumps(data),
            headers = self.auhd
        )
        if response.ok:
            print("Successfully changed password.")
        else:
            print("Failed to change password.\nReason: %s" % (response.content))

