
import os
import mock
import unittest
import py
import json
from tsuru.configdb import ConfigDb
from tsuru.cmds.users import AuthManager

DBNAME = os.path.join(os.path.dirname(__file__), "temp", "test.db")

ELoginFirst = 'Please login first!'
IRemoveApp = "Successfully remove an app."
ICreateApp = "Successfully created an app."
IAddUnit = "Successfully add units to an app."
IRemoveUnit = "Successfully remove units from an app."
ICreateUser = "User '%s' successfully created!"

TestAuthHeader = {'Authorization': 'token'}
TestPassword = "mypassord"
TestEmail = "test.email@gmail.com"
TestUser = "myname"

class TestUsersTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = DBNAME
        self.cfgdb = ConfigDb(self.dbn)

    def tearDown(self):
        if os.path.exists(self.dbn):
            os.remove(self.dbn)

            # now @with_setup(loggedin) can not working?
        # nose can not working with unittest.Testcase or it's subclass
    def loggedin(self):
        self.cfgdb.add_user(TestUser, TestEmail, "token", True)

    @mock.patch("getpass.getpass", return_value=TestPassword)
    @mock.patch("requests.post")
    def test_CreateUserWithLogin(self, getpass, post):
        self.loggedin()
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        data = {
            "email": TestEmail,
            "password": TestPassword
        }
        am.createUser(TestUser, TestEmail)
        out, err = capture.reset()
        getpass.return_value.assert_called_with("Please input your password: ")
        post.assert_called_with("target/users",
                                data=json.dumps(data),
                                headers=TestAuthHeader)
        #self.assertEquals(out.strip(), ICreateUser % TestEmail)
