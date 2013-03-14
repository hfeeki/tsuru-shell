clean:
	@find . -name "*.pyc" -delete
	@rm -rf build dist tsuru.egg-info
	@rm -rf .venv/lib/python2.7/site-packages/tsuru*

deps:
	@pip install -r requirements.txt --use-mirrors

develop:
	@python setup.py develop

test: clean develop
	@python setup.py test

build: 
	@python setup.py build

egg:
	@python setup.py bdist_egg

bdist:
	@python setup.py bdist

install: clean build
	@python setup.py install
