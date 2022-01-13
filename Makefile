.PHONY: sim

CWD=${CURDIR}

ifeq ($(OS), Windows_NT)
VENV=.venv_windows
PYTHON=py
VENVBIN=./${VENV}/Scripts
else ifneq ("$(wildcard /.dockerenv)","")
VENV=.venv_docker
PYTHON=python3
VENVBIN=./${VENV}/bin
else
VENV=.venv_osx
PYTHON=python3
VENVBIN=./${VENV}/bin
endif




sim: setup_${VENV}
	${VENVBIN}/${PYTHON} robot.py coverage sim
	${VENVBIN}/${PYTHON} robot.py sim

run:
	${PYTHON} robot.py run

${VENV}:
	${PYTHON} -m venv ${VENV}

lint:
	# From CI pipeline. We are more strict in our local check
	# --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293
	${VENVBIN}/flake8 . --count --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293,W503 --show-source --statistics --exclude */tests/pyfrc*,utils/yaml/*,.venv*/,venv*/

test: setup_${VENV} lint
	${VENVBIN}/${PYTHON} robot.py test

coverage: setup_${VENV} test
	${VENVBIN}/${PYTHON} robot.py coverage test

setup_${VENV}: ${VENV}
	${VENVBIN}/pip install --upgrade pip setuptools
	${VENVBIN}/pip install --pre -r ${CWD}/requirements.txt
	$(file > setup_${VENV})

clean:
	rm -f setup setup_${VENV}

realclean: clean
	rm -fr ${VENV}

docker: docker_build
	docker run --rm -ti -v $$(PWD):/src raptacon2022_build bash

docker_build:
	docker build . --tag raptacon2022_build

deploy:
	${PYTHON} robot.py deploy --no-resolve --robot 10.32.0.2
