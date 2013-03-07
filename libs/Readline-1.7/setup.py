# Setup for Python Alternative Readline for Windows
# This file mostly written by Alex Martelli; I like it.

from distutils.core import setup, Extension
import sys

# version of this Readline package
this_version = "1.7"

# Determine Python version (tested on 2.0 and later)
v = sys.version_info
python_version = v[0] * 100 + v[1] * 10 + v[2]

# turn keyword-arguments into a directory object
def dict_of(**kws): return kws

# the minimal info, which Python 2.0's distutils can digest
setup_args = dict_of(name="Readline",
          version=this_version,
          description="Alternative Python Readline for Windows",
          long_description="Alternative Python Readline for Windows",
          author="Chris Gonnerman",
          author_email="chris.gonnerman@newcenturycomputers.net",
          url="http://newcenturycomputers.net/projects/readline.html",
          py_modules=["readline"],
          ext_modules=[Extension("_rlsetup", ["_rlsetup.c"])],
    )

# provide more metadata if we have Python 2.1 (better distutils)
if python_version > 200:
    setup_args.update(dict_of(
          platforms="Win32",
          keywords="input history editing readline commandline",
    ))

# and finally call the distutils' setup
setup(**setup_args)

