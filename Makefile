PYTHON ?= python
NOSETESTS ?= nosetests

all: clean inplace test

clean-pyc:
	find atlastools -name "*.pyc" -exec rm {} \;

clean-so:
	find atlastools -name "*.so" -exec rm {} \;

clean-build:
	rm -rf build

clean: clean-build clean-pyc clean-so

in: inplace # just a shortcut
inplace:
	$(PYTHON) setup.py build_ext -i

install:
	$(PYTHON) setup.py install

install-user:
	$(PYTHON) setup.py install --user

sdist: clean
	$(PYTHON) setup.py sdist --release

register:
	$(PYTHON) setup.py register --release

upload: clean
	$(PYTHON) setup.py sdist upload --release

test-code: in
	$(NOSETESTS) -s atlastools --nologcapture

test: test-code

trailing-spaces:
	find atlastools -name "*.py" | xargs perl -pi -e 's/[ \t]*$$//'

check-rst:
	python setup.py --long-description | rst2html.py > __output.html
	rm -f __output.html
