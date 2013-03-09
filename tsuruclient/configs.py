

import os

HOME = os.getenv('HOME')
TARGET_FN = os.path.join(HOME, '.tsuru_target')
TOKEN_FN = os.path.join(HOME, '.tsuru_token')
#KEY_FN = os.path.join(HOME, '.ssh/id_rsa.pub')
KEY_FN = os.path.join(HOME, '.ssh/tsuru_id_rsa.pub')

DefaultTarget = "http://tsuru.plataformas.glb.com:8080"

IDENT = 4 * " "