#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

class AuthManager(object):

	def __init__(self, target):
        self.target = target

	def create(self, email):
		import getpass
		password = getpass.getpass("Please input your password: ")
		confirm = getpass.getpass("Confirm: ")
		if password != confirm:
			print "Passwords didn't match."
			return None 		
		data = {
            "email": name,
            "password": password,
        }
        response = requests.post(
            "{0}/users".format(self.target),
            data=json.dumps(data)
        )
        if response.ok:
        	print "User '%s' successfully created!" % email
        	return response.json
        else:
        	print "User '%s' failed to created!" % email
        	return response.json


