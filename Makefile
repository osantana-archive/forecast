PYTHON ?= python

.PHONY: all check clean clean-pyc clean-patchfiles clean-backupfiles clean-generated pylint reindent test covertest build convert-utils

all: clean-pyc clean-backupfiles check test

clean: clean-pyc clean-patchfiles clean-backupfiles clean-generated

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-patchfiles:
	find . -name '*.orig' -exec rm -f {} +
	find . -name '*.rej' -exec rm -f {} +

clean-backupfiles:
	find . -name '*~' -exec rm -f {} +
	find . -name '*.bak' -exec rm -f {} +

pylint:
	@pylint --rcfile pylintrc forecast

test: build
	python setup.py test

build:
	@$(PYTHON) setup.py build

