
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
IRemoveUser = "Remove user successfully!"
ILogin = "Successfully logged in!"
QRemoveUser = "Are you sure you want to remove your user from tsuru? (y/n) "
QHaveLoggedIn = "It looks like you have logged in, Do you realy want to login again? (y/n) "

TestAuthHeader = {'Authorization': 'token'}
TestPassword = "mypassord"
TestEmail = "test.email@gmail.com"
TestUser = "myname"

class TestUsersTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = DBNAME
        if os.path.exists(self.dbn):
            os.remove(self.dbn)
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
    def test_CreateUser(self, post, getpass):
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        data = {
            "email": TestEmail,
            "password": TestPassword
        }
        am.createUser(TestUser, TestEmail)
        out, err = capture.reset()
        #getpass.assert_called_with("Please input your password: ")
        getpass.assert_called_with("Confirm: ")
        post.assert_called_with("target/users", data=json.dumps(data))
        self.assertEquals(out.strip(), ICreateUser % TestEmail)

    @mock.patch("__builtin__.raw_input", return_value="Y")
    @mock.patch("requests.delete")
    def test_RemoveUserWithLoginAndYesConfirm(self, delete, raw_input):
        self.loggedin()
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.removeUser()
        out, err = capture.reset()
        raw_input.assert_called_with(QRemoveUser)
        delete.assert_called_with("target/users", headers=TestAuthHeader)
        self.assertEquals(out.strip(), IRemoveUser)

    @mock.patch("__builtin__.raw_input", return_value="N")
    @mock.patch("requests.delete")
    def test_RemoveUserWithLoginAndNoConfirm(self, delete, raw_input):
        self.loggedin()
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.removeUser()
        out, err = capture.reset()
        raw_input.assert_called_with(QRemoveUser)
        delete.not_called()
        self.assertEquals(out.strip(), "Abort.")

    @mock.patch("requests.delete")
    def test_RemoveUserWithoutLogin(self, delete):
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.removeUser()
        out, err = capture.reset()
        delete.not_called()
        self.assertEquals(out.strip(), ELoginFirst)

'''
    @mock.patch("getpass.getpass", return_value=TestPassword)
    @mock.patch("requests.post")
    @mock.patch("requests.Response.json", return_value="token")
    def test_Login(self, json, post, getpass):
        data = {
            "password": TestPassword
        }
        am = AuthManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.login(TestUser, TestEmail)
        out, err = capture.reset()
        post.assert_called_with("target/users/{0}/tokens".format(TestEmail),
                                data=json.dumps(data))
        self.assertEquals(out.strip(), ILogin)
        # confirm the cfgdb's content
        # with offtheshelf.openDB(self.dbn) as db:
        #     users = db.get_collection("users")
        #     x = users.find({'name': TestUser, 'email': TestEmail, 'default': True})
        #     assert x != None
        #     self.assertEquals(1, len(x))
        #     self.assertEquals("token", x[0]['token'])
'''

