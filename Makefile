# simple makefile to simplify repetetive build env management tasks under posix

PYTHON ?= python
NOSETESTS ?= nosetests
CTAGS ?= ctags

all: clean inplace test

clean-pyc:
	find atlastools -name "*.pyc" | xargs rm -f

clean-so:
	find atlastools -name "*.so" | xargs rm -f

clean-build:
	rm -rf build

clean-ctags:
	rm -f tags

clean: clean-build clean-pyc clean-so clean-ctags

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

ctags:
	# make tags for symbol based navigation in emacs and vim
	# Install with: sudo apt-get install exuberant-ctags
	$(CTAGS) -R *

update-distribute:
	curl -O http://python-distribute.org/distribute_setup.py

check-rst:
	python setup.py --long-description | rst2html.py > __output.html
	rm -f __output.html
