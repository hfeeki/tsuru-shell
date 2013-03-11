# -*- coding: utf-8 -*-

import os
import offtheshelf 
from utils import Singleton
from configs import DefaultDbName

@Singleton
class ConfigDb(object):

    #def __new__(cls):
    #    return object.__new__(cls)

    def __init__(self, name=DefaultDbName):
        self.dbname = name
        dbexists = False
        if os.path.exists(os.path.join(os.getcwd(), DefaultDbName)):
            dbexists = True
        #self.db = offtheshelf.openDB(name)
        #self._createTables()
        if not dbexists:
            self._insertInitData()

    def _insertInitData(self):
        with offtheshelf.openDB(self.dbname) as db:
            targets = db.get_collection("targets")
            targets.insert({"name": "local", 
                            "url": "http://127.0.0.1:8080",
                            "default": True})
            #users = db.get_collection("users")
            #users.insert({'name': 'Guest','email': None, 'token': None, 'default': True})
        return

    def get_targets(self):
        with offtheshelf.openDB(self.dbname) as db:
            tcoll = db.get_collection("targets")
            return tcoll.find() 

    def get_default_target(self):
        with offtheshelf.openDB(self.dbname) as db:
            tcoll = db.get_collection("targets")
            x = tcoll.find({'default': True})
            if len(x) > 0:
                return x[0]
            else:
                return None

    def set_default_target(self, name):
        with offtheshelf.openDB(self.dbname) as db:
            tcoll = db.get_collection("targets")
            # clear the old default target
            tcoll.update({'default': False})
            # set the new default target
            tcoll.update({'default': True}, {'name': name.lower()})        

    def add_target(self, name, url, is_default=False):
        with offtheshelf.openDB(self.dbname) as db:
            tcoll = db.get_collection("targets")
            tcoll.upsert({'name':name, 'url': url, 'default': False},
                {'name': name})
        if is_default:
            self.set_default_target(name)

    def remove_target(self, name):
        with offtheshelf.openDB(self.dbname) as db:
            tcoll = db.get_collection("targets")
            tcoll.delete({'name': name})        

    def add_user(self, name, email, token=None, is_default=False):
        '''Add or update a user's info.
        '''
        with offtheshelf.openDB(self.dbname) as db:
            coll = db.get_collection("users")
            coll.upsert({'name':name, 'email': email, 'default': False, 'token': token},
                {'name': name})
        if is_default:
            self.set_default_user(name)        

    def remove_user(self, name=None, email=None, token=None):
        with offtheshelf.openDB(self.dbname) as db:
            coll = db.get_collection("users")
            cond = {}
            if token:
                cond['token'] = token
            if email:
                cond['email'] = email
            if name:
                cond['name'] = name
            coll.delete(cond)        

    def set_default_user(self, name):  
        with offtheshelf.openDB(self.dbname) as db:
            coll = db.get_collection("users")
            # clear the old default target
            coll.update({'default': False})
            # set the new default target
            coll.update({'default': True}, {'name': name.lower()})        

    def get_default_user(self):
        with offtheshelf.openDB(self.dbname) as db:
            coll = db.get_collection("users")
            x = coll.find({'default': True})
            if len(x) > 0:
                return x[0]
            else:
                return None        

    def get_default_token(self):
        x = self.get_default_user()
        if x and x['token']:
            return x['token']
        else:
            return None

    def is_user_loggedin(self, name):
        with offtheshelf.openDB(self.dbname) as db:
            coll = db.get_collection("users")
            x = coll.find({'name': name})
            if x and x['token'] and len(x['token'])>0:
                return True
            else:
                return False    


cfgdb = ConfigDb.Instance()