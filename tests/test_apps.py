
import json
from nose.tools import with_setup, eq_
import unittest
import pytest
from tsuru.libs import mock
from tsuru.configdb import ConfigDb
from tsuru.cmds.apps import AppManager
import os, sys
import py

DBNAME = os.path.join(os.path.dirname(__file__), "temp", "test.db")

ELoginFirst = 'Please login first!'
IRemoveApp = "Successfully remove an app."

TestAuthHeader = {'Authorization': 'token'}

# with_setup can not works for unittest.TestCase
class TestAppsTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = DBNAME
        self.cfgdb = ConfigDb(self.dbn)

    def tearDown(self):
        if os.path.exists(self.dbn):
            os.remove(self.dbn)        

    # now @with_setup(loggedin) can not working?
    # nose can not working with unittest.Testcase or it's subclass
    def loggedin(self):
        self.cfgdb.add_user("test", "test@gmail.com", "token", True)       
    
    @mock.patch("requests.get")
    def test_ListAppsWithLogin(self, get):
        t = self.cfgdb.get_default_target()
        eq_(t['name'], 'local')
        eq_(t['url'], 'http://127.0.0.1:8080')
        self.loggedin()
        am = AppManager("target", self.dbn)
        am.list()
        get.assert_called_with("target/apps", headers=TestAuthHeader)

    @mock.patch("requests.get")
    def test_ListAppsWithoutLogin(self, get):
        am = AppManager("target", self.dbn) 
        capture = py.io.StdCaptureFD(in_=False)       
        am.list()
        out, err = capture.reset()
        get.not_called() 
        self.assertEquals(out.strip(), ELoginFirst)

    @mock.patch("requests.get")
    def test_GetAppWithLogin(self, get):
        self.loggedin()
        am = AppManager("target", self.dbn)        
        am.get("myapp")
        get.assert_called_with("target/apps/myapp", headers=TestAuthHeader)

    @mock.patch("requests.get")
    def test_GetAppWithoutLogin(self, get):
        am = AppManager("target", self.dbn)        
        capture = py.io.StdCaptureFD(in_=False)
        am.get("myapp")
        out, err = capture.reset()
        get.not_called()
        self.assertEquals(out.strip(), ELoginFirst)

    @mock.patch("requests.delete")
    def test_RemoveAppWithLogin(self, delete):
        self.loggedin()
        am = AppManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.remove("myapp")
        out, err = capture.reset()
        delete.assert_called_with("target/apps/myapp", headers=TestAuthHeader)
        self.assertEquals(out.strip(), IRemoveApp)

    @mock.patch("requests.delete")
    def test_RemoveAppWithoutLogin(self, delete):
        am = AppManager("target", self.dbn)
        capture = py.io.StdCaptureFD(in_=False)
        am.remove("myapp")
        out, err = capture.reset()        
        delete.not_called()
        self.assertEquals(out.strip(), ELoginFirst)

    '''
    @mock.patch("requests.get")
    def test_get_app(self, get):
        cl = client.Client("target")
        cl.apps.get("appname")
        get.assert_called_with("target/apps/appname")

    @mock.patch("requests.post")
    def test_create_app(self, post):
        cl = client.Client("target")
        data = {
            "name": "appname",
            "framework": "framework",
        }
        cl.apps.create(**data)
        post.assert_called_with("target/apps", data=json.dumps(data))
    '''