# Variable to export is loaded from .env* file

# WARNING: prohibit all confidential variable.
# They have to be provided by podman secret volume
# with a dedicated command to load them from .env_secret 

include .env
# include .env_dev
# include .env_prod
# include .env_test

# WARNING: it will export all and can overwrite
# variables with a similar name in your environment.
# It was not an obligation to export but we want reuse 
# these variables in child processus
export

# Makefile local env var
#---------------------------#
PY_MINOR=10
pyv=3.$(PY_MINOR)
VENV_NAME=.venv_$(PY_MINOR)
VENV=$(CURDIR)/$(VENV_NAME)
python=$(VENV)/bin/python
pip=$(VENV)/bin/python -m pip
pytest=$(VENV)/bin/pytest
black=$(VENV)/bin/black
flake8=$(VENV)/bin/flake8

help:
	@echo "##############################"
	@echo "$(APP_NAME):$(APP_VERSION)"
	@echo "##############################"
	@echo
	@echo $(APP_DESCRIPTION)
	@echo
	@echo "Sources: $(APP_REPOSITORY)"
	@echo
	@echo "Django settings: $(DJANGO_SETTINGS_MODULE)"
	@echo
	@echo "Please read README.rst to know commands"
	@echo "~~~~~~~~~~~~~~~~"
	@echo

install_venv:
	python$(pyv) -m venv $(VENV_NAME)
	$(python) -m ensurepip
	$(pip) install -U pip wheel setuptools

install_py:
	$(pip) install -r requirements.d/execution.txt

install_py_dev:
	$(pip) install -r requirements.d/developers.txt

install_var:
	mkdir -p /var/db

MESSAGE_VENV_NF="venv $(VENV_NAME) found. Please run make install_venv"

check_venv:
	[ -d "${VENV_NAME}" ] && echo "$(MESSAGE_VENV_NF)" || (echo "venv $(VENV_NAME) NOT FOUND." && exit 1)

install: check_venv install_var install_py

install_dev: check_venv install_var install_py install_py_dev

clean_venv:
	rm -rf $(VENV_NAME)

clean_py:
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*.py[o|c]" -delete

clean_var:
	rm -rf var

clean: clean_venv clean_py

full_clean: clean clean_var

django-serve:
	$(python) manage.py runserver localhost:${GARDEN_EXPOSED_PORT} --settings=garden.core.settings

django-migrate:
	$(python) manage.py migrate --settings=garden.core.settings

django-makemigrations: 
	$(python) manage.py makemigrations --settings=garden.core.settings

django-test:
	$(pytest)

django-superuser:
	$(python) manage.py createsuperuser --settings garden.core.settings

black:
	$(black) garden 

flake8:
	git ls-files | grep py$$ | xargs $(flake8) > flake8.log
	cat flake8.log | cut -d ":" -f 1 | uniq -c | sort -hr
	wc -l flake8.log

code_quality: black 
# flake8

test_qa_dev: clean install_venv install_var install_dev code_quality django-test
test_qa_exe: clean install_venv install_var install django-migrate django-serve

test-qa: test_qa_dev test_qa_exe

##################
# Docker/ Podman #
##################

podman-garden-create-secret:
	podman secret create ${GARDEN_SECRET_NAME} .env_private

podman-garden-create-volumes:
	podman volume create --ignore ${GARDEN_VOLUME_VAR}
	podman volume create --ignore ${GARDEN_VOLUME_PARTS}

podman-garden-superuser:
	podman run -it --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest createsuperuser
# Build podman image of the project and store it on your local repository

podman-garden-build:
	podman build -t ${GARDEN_APP_NAME}:${GARDEN_VERSION} -t ${GARDEN_APP_NAME}:latest .

# Run podman image already built and store it on your local repository
podman-garden-run: podman-stop-ct
	podman run -it --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE}  -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} -p ${GARDEN_EXPOSED_PORT}:${GARDEN_EXPOSED_PORT} ${GARDEN_APP_NAME}:latest runserver 0.0.0.0:${GARDEN_EXPOSED_PORT}

podman-garden-static: podman-stop-ct
	podman run --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest collectstatic -c --noinput --no-color

podman-garden-migrate: podman-stop-ct
	podman run --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest migrate

podman-garden-makemigration: podman-stop-ct
	podman run --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest makemigrations

podman-garden-test: podman-stop-ct
	podman run --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest test

podman-garden-manage: podman-stop-ct
	podman run --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest

podman-garden-bash: podman-stop-ct
	podman run -it --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} --entrypoint bash ${GARDEN_APP_NAME}:latest

podman-garden-shell: podman-stop-ct
	podman run -it --env DJANGO_SETTINGS_MODULE=${GARDEN_SETTINGS_MODULE} -v ${GARDEN_VOLUME_VAR}:/app/var:rw -v ${GARDEN_VOLUME_PARTS}:/app/parts:rw --secret ${GARDEN_SECRET_NAME} ${GARDEN_APP_NAME}:latest shell

# Join build/run process to ensure work on new version
podman-build-run-app: podman-build-app podman-run-app

podman-stop-ct:
	podman stop --all
