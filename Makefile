BASE ?= $(shell pwd)

TESTS=tests
ENV=env
DOCS=docs
PROJECT=gp

PYTHON=env/bin/python3
PIP=env/bin/pip
EXEC=__main__.py


.PHONY: clean docs run debug test setup init
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

docs:
	test -d ${DOCS} || mkdir ${DOCS}
	${PYTHON} -m pydoc -w ./
	mv *.html ${DOCS}

run:
	${PYTHON} -O ${PROJECT}/${EXEC}

debug:
	${PYTHON} ${PROJECT}/${EXEC}

test:
	${PYTHON} -m unittest discover ${TESTS}

setup:
	test -d ${ENV} || virtualenv -p /usr/bin/python3 --no-site-packages ${ENV}
	${PIP} install -r requirements.txt
	${PIP} install --upgrade pip
	${PIP} install --upgrade setuptools

