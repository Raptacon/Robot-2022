.PHONY: sim

<<<<<<< HEAD
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
=======
VENV=./venv
VENVBIN=${VENV}/bin/


sim: setup
	${VENVBIN}python3 robot.py coverage sim
	${VENVBIN}python3 robot.py sim

venv:
	python3 -m venv ${VENV}
>>>>>>> Robot-2020/aimbot

lint:
	# From CI pipeline. We are more strict in our local check
	# --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293 
<<<<<<< HEAD
	${VENVBIN}/flake8 . --count --ignore W293,E501 --show-source --statistics --exclude venv,*/tests/pyfrc*

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
	docker run --rm -ti -v $$(PWD):/src raptacon2021_build bash 

docker_build:
	docker build . --tag raptacon2021_build

deploy:
	${PYTHON} robot.py deploy --no-resolve --robot 10.32.0.2
=======
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
>>>>>>> Robot-2020/aimbot
