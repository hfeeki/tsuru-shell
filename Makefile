clean:
	@find . -name "*.pyc" -delete

deps:
	@pip install -r requirements.txt --use-mirrors

test: deps clean
	@nosetests -s . && flake8 .

build: 
	@python setup.py build

install: test build
	@python setup.py install
