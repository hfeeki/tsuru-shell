clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt --use-mirrors

test: deps clean
	@nosetests -s . && flake8 .

build: 
	@python setup.py build

egg:
	@python setup.py bdist_egg

bdist:
	@python setup.py bdist

install: test build
	@python setup.py install
