# -*- coding: utf-8 -*-

'''
python setup.py build  # 编译
python setup.py sdist  # zip格式包
python setup.py bdist  # zip格式包
python setup.py bdist_wininst # exe格式包
python setup.py bdist_rpm # rpm格式包
python setup.py bdist_egg # egg格式包
'''
# Hack to prevent stupid error on exit of `python setup.py test`. (See
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html.)
try:
    import multiprocessing
except ImportError:
    pass

from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages, Command
import sys

from tsuru import __version__

class PyTest(Command):
    '''Use this class will do not need to install pytest first.
    '''
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

class PyTest2(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)
               

with open("README.md") as f:
    README = f.read()

with open("History.md") as f:
    CHANGES = f.read()

with open('requirements.txt') as reqs:
    install_requires = []
    for line in reqs.read().split('\n'):
        if line and not line.startswith("--"):
            install_requires.append(line)

with open("entry_points.txt") as f:
    ENTRY_POINTS = f.read()

setup(
    name="tsuru",
    version=__version__,
    packages=find_packages(),

    description="Python bindings to tsuru REST API",
    long_description=README + '\n' + CHANGES,
    author="Michael",
    author_email="hfeeki@gmail.com",
    keywords = ("tsuru", "paas", "cloud"),  
    platforms = "Independant", 

    install_requires=install_requires,
    tests_require=['pytest'],
    cmdclass = {'test': PyTest2},
    test_suite='tests',
    entry_points=ENTRY_POINTS,
)
