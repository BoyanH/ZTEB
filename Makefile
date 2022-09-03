.PHONY: all venv hooks install lint analyse test build clean
.IGNORE: analyse

PROJECT_NAME = zteb
VENV_NAME ?= ${PROJECT_NAME}-venv
PYTHON = ${VENV_NAME}/bin/python

all: venv hooks

$(VENV_NAME)/bin/activate: dev-requirements.txt
	python3.8 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -r dev-requirements.txt
venv: $(VENV_NAME)/bin/activate

hooks:
	cp .githooks/* .git/hooks/
	chmod a+x .git/hooks/*

install: venv setup.py
	${PYTHON} setup.py develop

lint: venv
	${PYTHON} -m pylint ${PROJECT_NAME} test -E
	${PYTHON} -m flake8 ${PROJECT_NAME} test

analyse: venv
	${PYTHON} -m pylint ${PROJECT_NAME}
	${PYTHON} -m pylint test --rcfile test/.pylintrc

test: venv
	${PYTHON} -m pytest

build: venv
	${PYTHON} setup.py sdist bdist_wheel

clean:
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete
	rm -rf build dist ${PROJECT_NAME}.egg-info
