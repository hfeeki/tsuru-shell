
import os
import mock
import unittest
import py
import json
import pytest
from tsuru.libs import offtheshelf
from tsuru.configdb import ConfigDb
from tsuru.cmds.users import AuthManager

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
dbn = DBNAME
cfgdb = None

def setup_fixtures():
    dbn = DBNAME
    if os.path.exists(dbn):
        os.remove(dbn)
    cfgdb = ConfigDb(dbn)

def teardown_fixtures(db):
    db.destroy()

def py_test_funcarg__db(request):
    return request.cached_setup(
        setup = setup_fixtures,
        teardown = teardown_fixtures,
        scope = "module")

def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    global dbn, cfgdb
    if os.path.exists(dbn):
        os.remove(dbn)
    cfgdb = ConfigDb(dbn)

def teardown_function(function):
    """ teardown any state that was previously setup with a setup_function
    call.
    """
    global dbn, cfgdb
    if os.path.exists(dbn):
        os.remove(dbn)

def loggedin():
    global dbn, cfgdb
    cfgdb.add_user(TestUser, TestEmail, "token", True)


@mock.patch("getpass.getpass", return_value=TestPassword)
@mock.patch("requests.post")
def test_CreateUser(post, getpass, capsys):
    am = AuthManager("target", dbn)
    #capture = py.io.StdCaptureFD(in_=False)
    data = {
        "email": TestEmail,
        "password": TestPassword
    }
    am.createUser(TestUser, TestEmail)
    out, err = capsys.readouterr()
    #getpass.assert_called_with("Please input your password: ")
    getpass.assert_called_with("Confirm: ")
    post.assert_called_with("target/users", data=json.dumps(data))
    assert(out.strip(), ICreateUser % TestEmail)

@mock.patch("__builtin__.raw_input", return_value="Y")
@mock.patch("requests.delete")
def test_RemoveUserWithLoginAndYesConfirm(delete, raw_input, capsys):
    loggedin()
    am = AuthManager("target", dbn)
    #capture = py.io.StdCaptureFD(in_=False)
    am.removeUser()
    out, err = capsys.readouterr()
    raw_input.assert_called_with(QRemoveUser)
    delete.assert_called_with("target/users", headers=TestAuthHeader)
    assert(out.strip(), IRemoveUser)

@mock.patch("__builtin__.raw_input", return_value="N")
@mock.patch("requests.delete")
def test_RemoveUserWithLoginAndNoConfirm(delete, raw_input, capsys):
    loggedin()
    am = AuthManager("target", dbn)
    am.removeUser()
    out, err = capsys.readouterr()
    raw_input.assert_called_with(QRemoveUser)
    delete.not_called()
    assert(out.strip(), "Abort.")

@mock.patch("requests.delete")
def test_RemoveUserWithoutLogin(delete, capsys):
    am = AuthManager("target", dbn)
    am.removeUser()
    out, err = capsys.readouterr()
    delete.not_called()
    assert(out.strip(), ELoginFirst)

@mock.patch("__builtin__.raw_input", return_value="Y")
@mock.patch("getpass.getpass", return_value=TestPassword)
@mock.patch("requests.post")
def test_LoginSucess(post, getpass, raw_input, capsys):
    class Response:
        '''It is the post()'s return value'''
        def __init__(self):
            self.ok = True
        def json(self):
            return {"token": "token"}

    data = {
        "password": TestPassword
    }
    am = AuthManager("target", dbn)
    post.return_value = Response()
    am.login(TestUser, TestEmail)
    out, err = capsys.readouterr()
    post.assert_called_with("target/users/{0}/tokens".format(TestEmail),
                            data=json.dumps(data))
    assert(out.strip(), ILogin)
    # confirm the cfgdb's content
    with offtheshelf.openDB(dbn) as db:
        users = db.get_collection("users")
        x = users.find({'name': TestUser, 'email': TestEmail, 'default': True})
        assert x != None
        assert(1, len(x))
        #assert("token", x[0]['token'])

@mock.patch("__builtin__.raw_input", return_value="Y")
@mock.patch("getpass.getpass", return_value=TestPassword)
@mock.patch("requests.post")
def test_LoginFailed(post, getpass, raw_input, capsys):
    class Response:
        '''It is the post()'s return value'''
        def __init__(self):
            self.ok = False
            self.content = "Error!!"
        def json(self):
            return {"token": "token"}

    data = {
        "password": TestPassword
    }
    am = AuthManager("target", dbn)
    post.return_value = Response()
    am.login(TestUser, TestEmail)
    out, err = capsys.readouterr()
    post.assert_called_with("target/users/{0}/tokens".format(TestEmail),
                            data=json.dumps(data))
    assert(out.strip(), ELogin % post.return_value.content)

@mock.patch("__builtin__.raw_input", return_value="Y")
@mock.patch("getpass.getpass", return_value=TestPassword)
@mock.patch("requests.post")
def test_LoginSucessWithLoginAndYesConfirm(post, getpass, raw_input, capsys):
    class Response:
        '''It is the post()'s return value'''
        def __init__(self):
            self.ok = True
        def json(self):
            return {"token": "token"}
    loggedin()
    data = {
        "password": TestPassword
    }
    am = AuthManager("target", dbn)
    post.return_value = Response()
    am.login(TestUser, TestEmail2)
    out, err = capsys.readouterr()
    raw_input.assert_called_with(QHaveLoggedIn)
    post.assert_called_with("target/users/{0}/tokens".format(TestEmail2),
                            data=json.dumps(data))
    assert(out.strip(), ILogin)
    # confirm the cfgdb's content
    with offtheshelf.openDB(dbn) as db:
        users = db.get_collection("users")
        x = users.find({'name': TestUser, 'email': TestEmail2, 'default': True})
        assert x != None
        assert(1, len(x))
        #assert("token", x[0]['token'])

@mock.patch("__builtin__.raw_input", return_value="N")
@mock.patch("getpass.getpass", return_value=TestPassword)
@mock.patch("requests.post")
def test_LoginSucessWithLoginAndNoConfirm(post, getpass, raw_input, capsys):
    class Response:
        '''It is the post()'s return value'''
        def __init__(self):
            self.ok = True
        def json(self):
            return {"token": "token"}
    loggedin()
    data = {
        "password": TestPassword
    }
    am = AuthManager("target", dbn)
    post.return_value = Response()
    am.login(TestUser, TestEmail2)
    out, err = capsys.readouterr()
    #out, err = capsys.reset()
    raw_input.assert_called_with(QHaveLoggedIn)
    post.not_called()
    assert(out.strip(), "Abort.")

def test_LogoutSucess(capsys):
    loggedin()
    am = AuthManager("target", dbn)
    am.logout()
    out, err = capsys.readouterr()
    assert(out.strip(), ILogout)
    # confirm the cfgdb's content
    # with offtheshelf.openDB(self.dbn) as db:
    #     users = db.get_collection("users")
    #     x = users.find({'name': TestUser, 'email': TestEmail, 'default': True})
    #     assert x != None
    #     self.assertEquals(1, len(x))
    #     self.assertEquals("token", x[0]['token'])

def test_LoginStatus(capsys):
    am = AuthManager("target", dbn)
    am.status()
    out, err = capsys.readouterr()
    assert out.strip(), "You're not logged in!"
    loggedin()
    am.status()
    capsys.readouterr()
    assert out.strip(), "You: %s have logged into %s !" % (TestUser, "target")

def test_GetCurrentUser(capsys):
    am = AuthManager("target", dbn)
    x = am.getCurrentUser()
    out, err = capsys.readouterr()
    assert out.strip(), "There is no default user."
    #assert x, None
    loggedin()
    x = am.getCurrentUser()
    out, err = capsys.readouterr()
    assert out.strip(), "Current user is: %s, email: %s" % (TestUser, TestEmail)
    assert type(x), type({})
    assert x['name'], TestUser


