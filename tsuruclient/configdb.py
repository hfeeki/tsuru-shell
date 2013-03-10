# -*- coding: utf-8 -*-

import os
import sqlite3
from utils import Singleton
from configs import DefaultDbName

@Singleton
class ConfigDb(object):

    #def __new__(cls):
    #    return object.__new__(cls)

    def __init__(self, name=DefaultDbName):
        dbexists = False
        if os.path.exists(os.path.join(os.getcwd(), DefaultDbName)):
            dbexists = True
        self.db = sqlite3.connect(name)
        self._createTables()
        if not dbexists:
            self._insertInitData()

    def _createTables(self):
        c = self.db.cursor()
        try:
            c.execute("""create table if not exists 
                targets(name varchar(50) primary key,
                        url varchar(500),
                        is_default integer default 0)
            """)
            c.execute("""create table if not exists
                users(name varchar(25) unique, 
                      email varchar(50) primary key,
                      is_default integer default 0,
                      token varchar(500))
            """)        
            self.db.commit()
        finally:
            c.close()

    def _insertInitData(self):
        c = self.db.cursor()
        try:
            sql = "insert into targets(name, url, is_default) values('default', 'http://127.0.0.1:8080', 1)"
            c.execute(sql)
            self.db.commit()
        finally:
            c.close()

    def get_targets(self):
        c = self.db.cursor()
        try:        
            c.execute("select * from targets")
            x = c.fetchall()
            return x
        finally:
            c.close()   

    def get_default_target(self):
        c = self.db.cursor()
        try:        
            c.execute("select * from targets where is_default=1")
            x = c.fetchone()
            if len(x) > 0:
                return x # just fetch first one
            else:
                return None
        finally:
            c.close()   

    def set_default_target(self, name):
        c = self.db.cursor()
        try:
            # clear the old default target
            sql = "update targets set is_default=0 where is_default=1"
            c.execute(sql)        
            # set the new default target
            sql = "update targets set is_default=1 where name='%s'" % (name.lower())
            c.execute(sql)            
        finally:
            c.close()

    def add_target(self, name, url, is_default=False):
        c = self.db.cursor()
        try:        
            if is_default:
                # clear all old default target
                sql = "update targets set is_default=0 where is_default=1"
                c.execute(sql)
                self.db.commit()
            xd = 1 if is_default else 0
            sql = "insert into targets(name, url, is_default) values('%s', '%s', %d)" % (name.lower(), url.lower(), xd)
            c.execute(sql)      
            self.db.commit()      
        finally:
            c.close()

    def remove_target(self, name=None, url=None):
        c = self.db.cursor()
        try:            
            cond = None
            if name and url:
                cond = "name='%s' and url='%s'" % (name.lower(), url.lower())
            elif name:
                cond = "name='%s'" % name.lower()
            elif url:
                cond = "url='%s'" % url.lower()                            
            sql = "delete from targets where '%s'" % cond
            c.execute(sql)
        finally:
            c.close()

    def add_user(self, name, email, token="", is_default=False):
        c = self.db.cursor()
        try:
            xd = 1 if is_default else 0
            sql = """insert into 
                users(name, email, token, is_default) 
                values('%s', '%s', '%s', %d)""" % (name.lower(), email.lower(), token, xd)
            c.execute(sql)
        finally:
            c.close()

    def remove_user(self, name=None, email=None, token=None):
        c = self.db.cursor()
        try:
            cond = None
            if token:
                cond = "token='%s'" % (token)
            elif email:
                cond = "email='%s'" % (email)
            elif name:
                cond = "name='%s'" % name            
            sql = "delete from users where '%s'" % cond
            c.execute(sql)
        finally:
            c.close()

    def set_default_user(self, name=None, email=None):        
        c = self.db.cursor()
        try:        
            # we need check the default user is the only one
            sql = "update users set is_default=0 where is_default=1"
            c.execute(sql)
            # set the new default user
            if email:
                sql = "update users set is_default=1 where email='%s'" % (email)
            elif name:
                sql = "update users set is_default=1 where name='%s'" % (name)
            c.execute(sql)
        finally:
            c.close()

    def get_default_user(self):
        c = self.db.cursor()
        try:        
            c.execute("select * from users where is_default=1")
            x = c.fetchone()
            if len(x) > 0:
                return x[0] # just fetch first one
            else:
                return None
        finally:
            c.close() 



cfgdb = ConfigDb.Instance()