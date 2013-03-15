# -*- coding: utf-8 -*-

# conftest.py
# just a demo
__author__ = 'michael'

class DataBase(object):
    def __init__(self, dbn):
        self.dbn = dbn
    def insert(self):
        pass
    def destroy(self):
        pass
    def query(self, x):
        pass

db = DataBase("test.db")

def setup_fixtures():
    db.insert()
    return db

def teardown_fixtures(db):
    db.destroy()

def py_test_funcarg__db(request):
    return request.cached_setup(
        setup = setup_fixtures,
        teardown = teardown_fixtures,
        scope = "module")

# test_db.py
# the db is test fixture
def test_db(db):
    assert(len(db.query(x=3)) >= 1)