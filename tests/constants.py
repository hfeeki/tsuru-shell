# -*- coding: utf-8 -*-

__author__ = 'michael'

import os

ELoginFirst = 'Please login first!'
IRemoveApp = "Successfully remove an app."
ICreateApp = "Successfully created an app."
IAddUnit = "Successfully add units to an app."
IRemoveUnit = "Successfully remove units from an app."
ICreateUser = "User '%s' successfully created!"
IRemoveUser = "Remove user successfully!"
ILogin = "Successfully logged in!"
ILogout = "Successfully logged out!"
ELogin = "Failed to logged in!\nReason: %s"
QRemoveUser = "Are you sure you want to remove your user from tsuru? (y/n) "
QHaveLoggedIn = "It looks like you have logged in, Do you realy want to login again? (y/n) "

TestAuthHeader = {'Authorization': 'token'}
TestPassword = "mypassord"
TestEmail = "test.email@gmail.com"
TestUser = "myname"
TestEmail2 = "test2.email@gmail.com"
TestUser2 = "myname2"

DBNAME = os.path.join(os.path.dirname(__file__), "temp", "test_users.db")
OUTPUT = os.path.join(os.path.dirname(__file__), "output")

