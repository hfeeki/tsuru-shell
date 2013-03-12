# -*- coding: utf-8 -*-

'''
python setup.py build  # 编译
python setup.py sdist  # zip格式包
python setup.py bdist  # zip格式包
python setup.py bdist_wininst # exe格式包
python setup.py bdist_rpm # rpm格式包
python setup.py bdist_egg # egg格式包
'''

from setuptools import setup, find_packages
from tsuru import __version__

with open("README.md") as f:
    README = f.read()

with open("History.md") as f:
    CHANGES = f.read()

with open('requirements.txt') as reqs:
    install_requires = []
    for line in reqs.read().split('\n'):
        if line and not line.startswith("--"):
            install_requires.append(line)

entry_points="""
[console_scripts]
tsuru = tsuru.itsuru:main 
"""            

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
    tests_require=['unittest2'],
    test_suite='tsuru.tests',
    entry_points=entry_points
)
