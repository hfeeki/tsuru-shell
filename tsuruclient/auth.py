#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
import getpass

from configs import TOKEN_FN


class AuthManager(object):

    def __init__(self, target):
        self.target = target

    def createUser(self, email):        
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
            print "User '%s' failed to created!" % email
        return response.json()

    def removeUser(self, email):
        """removes your user from tsuru server.
        """
        # http DELETE http://127.0.0.1:7080/user/user2@gmail.com
        q = "Are you sure you want to remove your user from tsuru? (y/n) "
        a = raw_input(q)
        if a != "y" or a != "Y":
            print("Abort.")
            return
        response = requests.delete("{0}/users/{1}".format(self.target, email))
        if response.ok:
            print "Remove '%s' successfully!" % email
        else:
            print "Remove '%s' failed! Reason: %s" % (email, response.content)

    def login(self, email):
        '''Login to server.
        '''
        # http POST http://127.0.0.1:8080/users/xbee@outlook.com/tokens password=fq9798
        # if token file exists
        if os.path.exists(TOKEN_FN):
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
            fn = TOKEN_FN
            with open(fn, 'w') as f:
                f.write(c)
            print("Successfully logged in!")
            return 
        else:
            print("Failed to logged in!\nReason: %s" % response.content)
            return 

    def logout(self):
        '''clear local authentication credentials.'''
        fn = TOKEN_FN
        if os.path.exists(fn):
            os.remove(fn)
            print("Successfully logged out!")
        else:
            print("You're not logged in!")
        

    def createTeam(self, name):
        '''creates a new team.
        '''
        # http POST http://127.0.0.1:8080/teams name=TEST Authorization:TOKEN
        data = {
            "name": name
        }
        headers = None
        if os.path.exists(TOKEN_FN):
            token = open(TOKEN_FN).read().strip()
            headers = {'Authorization': token}
        response = requests.post(
            "{0}/teams".format(self.target),
            data=json.dumps(data),
            headers = headers
        )
        if response.ok:
            print "Team '%s' successfully created!" % name
        else:
            print "Team '%s' failed to created! Reason: %s" % (name, response.content)

    def removeTeam(self, name):
        '''removes a team from tsuru server.
        '''
        # http DELETE http://127.0.0.1:8080/teams/TEST Authorization:TOKEN
        headers = None
        if os.path.exists(TOKEN_FN):
            token = open(TOKEN_FN).read().strip()
            headers = {'Authorization': token}
        else:
            print("Please login first!")
            return
        q = "Are you sure you want to remove team ? (y/n) "
        a = raw_input(q).strip()
        if a == "n" or a == "N":
            print("Abort")
            return 
        if a == "y" or a == "Y":            
            response = requests.delete(
                "{0}/teams/{1}".format(self.target, name),
                headers = headers
            )
            if response.ok:
                print "Remove team '%s' successfully!" % name
            else:
                print "Remove team '%s' failed! Reason: %s" % (name, response.content)
            return 

    def addTeamUser(self, tname, uname):
        '''adds a user to a team.
        Usage: addteamuser <teamname> <useremail>
        '''
        pass

