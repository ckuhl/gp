BASE ?= $(shell pwd)
TESTS=tests
ENV=env
PYTHON3=env/bin/python3
PIP=env/bin/pip
DOCS=docs
PROJECT=gp

EXEC=run.py

.PHONY: clean docs run debug test setup init
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

docs:
	test -d ${DOCS} || mkdir ${DOCS}
	${PYTHON3} -m pydoc -w ./
	mv *.html ${DOCS}

run:
	${PYTHON3} -O ${EXEC}

debug:
	${PYTHON3} ${EXEC}

test:
	${PYTHON3} -m unittest discover ${TESTS}

setup:
	test -d ${ENV} || virtualenv -p /usr/bin/python3 --no-site-packages ${ENV}
	${PIP} install -r requirements.txt
	${PIP} install --upgrade pip
	${PIP} install --upgrade setuptools

