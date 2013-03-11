

import os
from nose.tools import ok_, eq_
import json
import mock
import unittest
from tsuru import offtheshelf
from tsuru.configdb import ConfigDb
from tsuru.configs import DefaultTarget


class ConfigDbTestCase(unittest.TestCase):

    def setUp(self):
        self.dbn = "./temp/test.db"
        ConfigDb(self.dbn)

    def tearDown(self):        
        if os.path.exists(self.dbn):
            os.remove(self.dbn)

    def test_init(self):
        with offtheshelf.openDB(self.dbn) as db:
            targets = db.get_collection("targets")
            x = targets.find({'name': 'local', 'default': True, 'url': DefaultTarget})
            assert x != None
            assert len(x)==1


if __name__ == '__main__':
    unittest.main()    



    
