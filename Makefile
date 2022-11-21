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
#---------------------------#

help: help_local help_podman

help_local:
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
	@echo "Local deployment"
	@echo "~~~~~~~~~~~~~~~~"
	@echo
	@echo "These commands need to be launched directly on current host/machine."
	@echo
	@echo "First on a dev env you will have to do:" 
	@echo " - make install_venv && make install"
	@echo "After without incident you will only have to use make install who will "
	@echo "only check if venv exists before install project dependency"
	@echo "install_venv: Create a local venv"
	@echo "install_py: Install python requirements/dependency"
	@echo "install_exe: Install the project with only execution requirement"
	@echo "install: Install the project and developer's tools"
	@echo "check_venv: Check if the local venv exists"
	@echo
	@echo "clean_venv: Clean/Destruct local venv"
	@echo "clean_py: Clean/Destruct pyc, pyo, pycache files"
	@echo "clean: Clean local project installation" 
	@echo
	@echo "django-serve: Start django"
	@echo "django-migrate: Migrate django database"
	@echo "django-makemigrations: Create django database migrations"
	@echo "django-test: Run project unittest suite"
	@echo
	@echo "black: Re-format python code style"
	@echo "flake8: Check syntax of python code"
	@echo "code_quality: Launch tools to fix/check code syntax"
	@echo "test_qa_dev: clean install_dev test-qa django-test"
	@echo "test_qa_exe: clean install django-migrate django-makemigrations django-serve"
	@echo "test_qa: Launch all code quality check"
	@echo

install_venv:
	python$(pyv) -m venv $(VENV_NAME)
	$(python) -m ensurepip
	$(pip) install -U pip wheel setuptools

install_py:
	$(pip) install -r requirements.d/execution.txt

install_py_dev:
	$(pip) install -r requirements.d/developers.txt

check_venv:
	[ -d "${VENV_NAME}" ] && echo "venv $(VENV_NAME) found." || (echo "venv $(VENV_NAME) NOT FOUND." && exit 1)

install: check_venv install_py

install_dev: check_venv install_py install_py_dev


clean_venv:
	rm -rf $(VENV_NAME)
clean_py:
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*.py[o|c]" -delete
clean: clean_venv clean_py

django-serve:
	$(python) manage.py runserver

django-migrate:
	$(python) manage.py migrate 

django-makemigrations: 
	$(python) manage.py makemigrations

django-test:
	$(pytest) project/ applications/
	

black:
	$(black) project/ applications/

flake8:
	git ls-files | grep py$$ | xargs $(flake8) > flake8.log
	cat flake8.log | cut -d ":" -f 1 | uniq -c | sort -hr
	wc -l flake8.log

code_quality: black 
# flake8

test_qa_dev: clean install_dev code_quality django-test
test_qa_exe: clean install django-migrate django-makemigrations django-serve

test-qa: test_qa_dev test_qa_exe

##################
# Docker/ Podman #
##################

help_podman:
	@echo "##################"
	@echo "# Docker/ Podman #"
	@echo "##################"
	@echo
	@echo "These commands might need to be played with podman."
	@echo
	@echo "podman-:podman-secret-create:"
	@echo
	@echo "podman-:podman-build-app"
	@echo
	@echo "podman-:podman-run-app"
	@echo
	@echo "podman-:podman-run-app-migrate"
	@echo
	@echo "podman-:podman-run-app-makemigration"
	@echo
	@echo "podman-:podman-run-app-test"
	@echo
	@echo "podman-:podman-run-app-manage"
	@echo
	@echo "podman-:podman-run-app-bash"
	@echo
	@echo "podman-:podman-run-app-shell"
	@echo
	@echo "podman-:podman-build-run-app"
	@echo
	@echo "podman-:podman-stop-ct"
	@echo

podman-secret-create:
	podman secret create django-private-settings .env_private

# Build podman image of the project and store it on your local repository
podman-build-app:
	podman build -t ${PODMAN_IMG_NAME} .

# Run podman image already built and store it on your local repository
podman-run-app: podman-stop-ct
	podman run --rm -d --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings -p ${PODMAN_EXPOSED_PORT}:${PODMAN_EXPOSED_PORT} ${PODMAN_IMG_NAME} runserver 0.0.0.0:${PODMAN_EXPOSED_PORT}

podman-run-app-migrate: podman-stop-ct
	podman run --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings ${PODMAN_IMG_NAME} migrate

podman-run-app-makemigration: podman-stop-ct
	podman run --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings ${PODMAN_IMG_NAME} makemigrations

podman-run-app-test: podman-stop-ct
	podman run --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings ${PODMAN_IMG_NAME} test

podman-run-app-manage: podman-stop-ct
	podman run --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings ${PODMAN_IMG_NAME}

podman-run-app-bash: podman-stop-ct
	podman run -i --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings --entrypoint bash ${PODMAN_IMG_NAME}

podman-run-app-shell: podman-stop-ct
	podman run -i --rm --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} -v django-project:/app/var:rw --secret django-private-settings ${PODMAN_IMG_NAME} shell

# Join build/run process to ensure work on new version
podman-build-run-app: podman-build-app podman-stop-ct podman-run-app

podman-stop-ct:
	podman stop --all
