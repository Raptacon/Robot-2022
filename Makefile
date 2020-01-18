.PHONY: sim

VENV=./venv


sim: setup
	${VENV}/bin/python3 robot.py coverage sim
	${VENV}/bin/python3 robot.py sim

venv:
	python3 -m venv ${VENV}

test: setup
	${VENV}/bin/python3 robot.py test

coverage: setup test
	${VENV}/bin/python3 robot.py coverage test

setup: venv
	${VENV}/bin/pip3 install -r requirements.txt
	touch setup

clean:

realclean:
	rm -fr venv setup
