clean:
	@find . -name "*.pyc" -delete
	@rm -rf build dist tsuru.egg-info

deps:
	@pip install -r requirements.txt --use-mirrors

test: clean
	@nosetests -s . && flake8 .

build: 
	@python setup.py build

egg:
	@python setup.py bdist_egg

bdist:
	@python setup.py bdist

install: clean build
	@python setup.py install
