
import json
from tsuru.libs import mock
from tsuru.libs import nose
from nose.tools import with_setup, eq_
import unittest
from tsuru.configdb import ConfigDb
from tsuru.cmds.apps import AppManager
import os

DBNAME = os.path.join(os.path.dirname(__file__), "temp", "test.db")

class AppsTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = DBNAME
        self.cfgdb = ConfigDb(self.dbn)

    def tearDown(self):
        if os.path.exists(self.dbn):
            os.remove(self.dbn)        

    def loggedin(self):
        self.cfgdb.add_user("test", "test@gmail.com", "token", True)        
    
    @mock.patch("requests.get")
    @with_setup(setup=loggedin)
    def test_list(self, get):
        t = self.cfgdb.get_default_target()
        eq_(t['name'], 'local')
        eq_(t['url'], 'http://127.0.0.1:8080')
        self.cfgdb.add_user("test", "test@gmail.com", "token", True)
        am = AppManager("target", self.dbn)
        am.list()
        get.assert_called_with("target/apps", headers={'Authorization':'token'})

    '''
    @mock.patch("requests.get")
    def test_list_apps(self, get):
        cl = client.Client("target")
        cl.apps.list()
        get.assert_called_with("target/apps")

    @mock.patch("requests.get")
    def test_get_app(self, get):
        cl = client.Client("target")
        cl.apps.get("appname")
        get.assert_called_with("target/apps/appname")

    @mock.patch("requests.delete")
    def test_remove_app(self, delete):
        cl = client.Client("target")
        cl.apps.remove("appname")
        delete.assert_called_with("target/apps/appname")

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