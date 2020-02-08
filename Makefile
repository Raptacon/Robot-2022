.PHONY: sim

VENV=./venv
VENVBIN=${VENV}/bin/


sim: setup
	${VENVBIN}python3 robot.py coverage sim
	${VENVBIN}python3 robot.py sim

venv:
	python3 -m venv ${VENV}

codecheck:
	${VENVBIN}flake8 --exclude venv,tests

test: setup codecheck
	${VENVBIN}python3 robot.py test

coverage: setup test
	${VENVBIN}python3 robot.py coverage test

setup: venv
	#${VENVBIN}pip3 --no-cache-dir install -r requirements.txt
	${VENVBIN}pip3 install --pre -r requirements.txt
	touch setup

clean:
	rm -f setup

realclean:
	rm -fr venv setup

docker: docker_build
	docker run --rm -ti -v $$(PWD):/src raptacon2020_build bash 

docker_build:
	docker build . --tag raptacon2020_build
