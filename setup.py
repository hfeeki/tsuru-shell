from setuptools import setup, find_packages
from tsuruclient import __version__


with open('requirements.txt') as reqs:
    install_requires = []
    for line in reqs.read().split('\n'):
        if line and not line.startswith("--"):
            install_requires.append(line)


setup(
    name="tsuru",
    version=__version__,
    packages=find_packages(),
    description="Python bindings to tsuru REST API",
    author="Michael",
    author_email="hfeeki@gmail.com",
    install_requires=install_requires,
    tests_require=['unittest2'],
    test_suite='tsuruclient.tests',
    entry_points="""
        [console_scripts]
        tsuru = tsuruclient.ishell:main    
    """
)
