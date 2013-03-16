
import os, sys
import unittest
import pytest
from tsuru import itsuru
from tsuru.configdb import ConfigDb
from constants import *

TSRUR_CMDS = [ 
    ("app_create", "ac"),
    ("app_env_get", "aeg"),
    ("app_env_set", "aes"),
    ("app_env_unset", "aeu"),
    ("app_info", "ai"),
    ("app_list", "al"),
    ("app_remove", "ar"),
    ("app_unit_add", "aua"),
    ("app_unit_remove", "aur"),
    ("change_password", "cp"),
    ("exit", "q", "quit", "x"),
    ("", "?", "help"),
    ("login", 'lgi'), 
    ("logout", 'lgo'), 
    ("service_add", "sa"), 
    ("service_bind", "sb"),
    ("service_doc", "sd"), 
    ("service_info", "si"),
    ("service_list", "sl"), 
    ("service_status", "ss", "sst"),
    ("service_unbind", "sub"), 
    ("shell", "!", "sh"), 
    ("status", "s", "st"),
    ("target_add", "ta"),
    ("target_default_get", "dt", "tdg"),
    ("target_default_set", "tds"),
    ("target_get", "t", "target"),
    ("target_remove", "tr"),
    ("team_create", "tc"),
    ("team_list", "tl"),
    ("team_remove",), # must have a comma after "team_remove"
    ("team_user_add", "tua"),
    ("team_user_remove", "tur"),
    ("user_create", "uc"),
    ("user_current", "cu"),
    ("user_key_add", "uka"),
    ("user_key_remove", "ukr"),
    ("user_list", "ul"),
    ("user_remove", "ur"),
    ("welcome", "w", "wel")
]

SKIPTESTHELP = True
CONSOLE = itsuru.ITsuru()

dbn = DBNAME
cfgdb = None

def parseargs(subcmd):
    if type(subcmd) is str:
        argv=["tsuru", "%s" % subcmd]
    elif type(subcmd) in [tuple, list]:
        argv = ['tsuru']
        for x in subcmd:
            argv.append(x)
    return argv

def xtsuru(subcmd):
    global CONSOLE
    console = CONSOLE
    arg = parseargs(subcmd)
    console.main(argv=arg)

# content of module.py
def help():
    sys.argv = ["tsuru", "help"]
    console = itsuru.ITsuru()
    console.main(argv=sys.argv)

def generate_help_cmd(cmd=None):
    
    def help_cmd():
        if cmd == "" or cmd is None:
            argv = ["tsuru", "help"] 
        else:
            argv = ["tsuru", "help", cmd]
        console = itsuru.ITsuru()
        console.main(argv=argv)

    if cmd == "" or cmd is None:
        outfn = "help.out"
    else:
        outfn = "help_%s.out" % cmd
    return outfn, help_cmd

def generate_test_help_funcs(cmds):
    rs = [] # like [("help.out", help), ...]
    for alias in cmds:
        if type(alias) is tuple:
            for x in alias:
                rs.append(generate_help_cmd(x))
        elif type(alias) is str:
            rs.append(generate_help_cmd(alias))
    return rs

need_tested_funcs = [
    #("welcome.out", cmd_welcome),
    
] + generate_test_help_funcs(TSRUR_CMDS) 

@pytest.mark.skipif("SKIPTESTHELP==True")
@pytest.mark.parametrize(("filename_expected", "function_to_test"), 
     need_tested_funcs)
def test_itsuru_funcoutput(capsys, filename_expected, function_to_test):
    function_to_test()
    resout, reserr = capsys.readouterr()
    fn = os.path.join(OUTPUT, filename_expected)
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            f.write(resout)
    expected = open(fn, "r").read()
    assert resout == expected

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

# def test_welcome(capsys):
#     xtsuru("welcome")
#     out, err = capsys.readouterr()
#     expect = open(os.path.join(OUTPUT, "welcome.out")).read().strip()
#     assert out.strip() == expect

def test_GetTargets(capsys):
    xtsuru("target")
    out, err = capsys.readouterr()
    assert out.rstrip() == u"   local     http://127.0.0.1:8080"

def test_AddTarget(capsys):
    xtsuru("target_add test http://127.0.0.1:5000 -d")
    xtsuru("target")
    out, err = capsys.readouterr()
    expected = """   local     http://127.0.0.1:8080
 * test      http://127.0.0.1:5000"""
    assert out.strip() == expected

def test_RemoveTarget(capsys):
    pass
