
import os, sys
from nose.tools import ok_, eq_
import json
from tsuru.libs import mock
import unittest
import pytest
from tsuru import itsuru

OUTPUT = os.path.join(os.path.dirname(__file__), "output")

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

# content of module.py
def help():
    sys.argv = ["tsuru", "help"]
    console = itsuru.ITsuru()
    console.main(argv=sys.argv)

def cmd_welcome():
    sys.argv = ["tsuru", "welcome"]
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

#@pytest.mark.parametrize(("filename_expected", "function_to_test"), [
#    ("help.out", help),
#    ("help_target.out", help_target),
#])
@pytest.mark.parametrize(("filename_expected", "function_to_test"), 
     need_tested_funcs)
def test_itsuru_funcoutput(capfd, filename_expected, function_to_test):
    function_to_test()
    resout, reserr = capfd.readouterr()
    fn = os.path.join(OUTPUT, filename_expected)
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            f.write(resout)
    expected = open(fn, "r").read()
    assert resout == expected

class iShellTestCase(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

