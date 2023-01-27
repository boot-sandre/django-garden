*********
* HOWTO *
*********

Start in legacy/Host env
########################

QA commands::
        
        make test-qa
        make clean

First run local host commands::

        make install_venv
        make install_dev
        make django-test
        make django-migrate
        make django-run&
        wget http://0.0.0.0:8080/test/ -O /tmp/index.html
        cat /tmp/index.html
        make clean

Start with podman
#################

************
* Makefile *
************

QA commands::

        make podman-secret-create
        make podman-build-app
        make podman-run-app-test

First run local host commands::

        make podman-secret-create
        make podman-build-run-app

Legacy/Host deployment
######################

These commands need to be launched directly on current host/machine.

 * install_exe: Install the project with only execution requirement
 * install: Install the project and developer's tools
 * install_venv: Create a local venv
 * install_var: Create directory structure of local ./var
 * install_py: Install python requirements/dependency

 * clean_venv: Clean/Destruct local venv
 * clean_py: Clean/Destruct pyc, pyo, pycache files
 * clean: Clean local project installation

 * django-serve: Start django
 * django-migrate: Migrate django database
 * django-makemigrations: Create django database migrations
 * django-test: Run project unittest suite

 * black: Re-format python code style
 * flake8: Check syntax of python code
 * code_quality: Launch tools to fix/check code syntax
 * test_qa: Launch tools to fix/check/test the project from a cleaned installation

##################
# Docker/ Podman #
##################

These commands might need to be played with podman.

podman-secret-create:

podman-build-app

podman-run-app

podman-run-app-migrate

podman-run-app-makemigration

podman-run-app-test

podman-run-app-manage

podman-run-app-bash

podman-run-app-shell

podman-build-run-app

podman-stop-ct

