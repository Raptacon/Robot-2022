.PHONY: sim

VENV=./venv

venv:
	python3 -m venv ${VENV}

sim: venv
	${VENV}/bin/python3 robot.py coverage sim
	${VENV}/bin/python3 robot.py sim

test: venv
	${VENV}/bin/python3 robot.py test

coverage: venv test
	${VENV}/bin/python3 robot.py coverage test

setup: venv
	${VENV}/bin/pip3 install -r requirements.txt

clean:

realclean:
	rm -fr venv
