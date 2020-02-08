.PHONY: sim

VENV=./venv
VENVBIN=${VENV}/bin/


sim: setup
	${VENVBIN}python3 robot.py coverage sim
	${VENVBIN}python3 robot.py sim

venv:
	python3 -m venv ${VENV}

lint:
	# From CI pipeline. We are more strict in our local check
	# --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293 
	${VENVBIN}flake8 . --count --ignore W293,E501 --show-source --statistics --exclude venv,*/tests/pyfrc*

test: setup lint
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
