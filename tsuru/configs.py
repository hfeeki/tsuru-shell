# -*- coding: utf-8 -*-

import os

HOME = os.getenv('HOME')
WORK_HOME = os.path.join(HOME, ".tsuru")

TARGET_FN = os.path.join(HOME, '.tsuru_target')
TOKEN_FN = os.path.join(HOME, '.tsuru_token')
CUSER_FN = os.path.join(HOME, '.tsuru_current_user')
#KEY_FN = os.path.join(HOME, '.ssh/id_rsa.pub')
KEY_FN = os.path.join(HOME, '.ssh/tsuru_id_rsa.pub')

DefaultTarget = "http://127.0.0.1:8080"
DefaultUser = "Guest"
DefaultDbName = os.path.join(WORK_HOME, "configs.db")

IDENT = 4 * " "

