BASE ?= $(shell pwd)

TESTS=tests
DOCS=docs
PROJECT=gp

PYTHON=pipenv run python
PIP=pipenv run python -m pip
EXEC=main.py


.PHONY: clean docs run debug test setup init
clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

docs:
	test -d ${DOCS} || mkdir ${DOCS}
	${PYTHON} -m pydoc -w ./
	mv *.html ${DOCS}

run:
	${PYTHON} -O ${EXEC}

debug:
	${PYTHON} ${EXEC}

test:
	${PYTHON} -m unittest discover ${TESTS}

setup:
	test -d ${ENV} || virtualenv -p python3 --no-site-packages ${ENV}
	${PYTHON} -m pip install -r requirements.txt

