

import os
from nose.tools import ok_, eq_, istest, nottest, assert_equal
from nose.tools import assert_not_equal, assert_raises
import mock
import unittest
from tsuru import offtheshelf
from tsuru.configdb import ConfigDb
from tsuru.configs import DefaultTarget


class ConfigDbTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = "./temp/test.db"
        self.cfgdb = ConfigDb(self.dbn)

    def tearDown(self):        
        if os.path.exists(self.dbn):
            os.remove(self.dbn)

    def test_init(self):
        '''Test the ConfigDb() or __init__ . 
        After called this function, it should exists a default target record.
        '''
        with offtheshelf.openDB(self.dbn) as db:
            targets = db.get_collection("targets")
            x = targets.find({'name': 'local', 'default': True, 'url': DefaultTarget})
            assert x != None
            eq_(1, len(x))

    def test_get_targets(self):
        ts = self.cfgdb.get_targets()
        eq_(1, len(ts))
        t = ts[0]
        eq_('local', t['name'])
        eq_(True, t['default'])
        eq_(DefaultTarget, t['url'])

    def test_get_default_target(self):
        t = self.cfgdb.get_default_target()
        assert t != None
        eq_('local', t['name'])
        eq_(True, t['default'])
        eq_(DefaultTarget, t['url'])

    def test_set_default_target(self):
        self.cfgdb.add_target("test", "http://localhost:7000")
        self.cfgdb.set_default_target('test')
        t = self.cfgdb.get_default_target()
        assert t != None
        eq_('test', t['name'])

    def test_add_target(self):
        ts = self.cfgdb.get_targets()
        eq_(1, len(ts))
        eq_(True, ts[0]['default'])
        self.cfgdb.add_target("test", "http://localhost:7000")
        ts = self.cfgdb.get_targets()
        eq_(2, len(ts))

    def test_remove_target(self):
        self.cfgdb.add_target("test", "http://localhost:7000")
        self.cfgdb.add_target("test2", "http://localhost:6000")
        ts = self.cfgdb.get_targets()
        eq_(3, len(ts))
        self.cfgdb.remove_target("test")
        ts = self.cfgdb.get_targets()
        eq_(2, len(ts))
        
    def test_get_default_user(self):
        x = self.cfgdb.get_default_user()
        eq_(None, x)

    def test_add_user(self):
        self.cfgdb.add_user("tester", "abc@gmail.com", "token", True)
        x = self.cfgdb.get_default_user()
        assert_not_equal(None, x)
        eq_('tester', x['name'])
        eq_('abc@gmail.com', x['email'])

    def test_remove_user(self):
        pass

    def test_x(self):
        assert_equal(1, "Not Implemented")


if __name__ == '__main__':
    unittest.main()    



    
