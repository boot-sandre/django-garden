Local deployment
################

These commands need to be launched directly on current host/machine.

 * install_exe: Install the project with only execution requirement
 * install: Install the project and developer's tools
 * install_venv: Create a local venv
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

podman-:podman-secret-create:

podman-:podman-build-app

podman-:podman-run-app

podman-:podman-run-app-migrate

podman-:podman-run-app-makemigration

podman-:podman-run-app-test

podman-:podman-run-app-manage

podman-:podman-run-app-bash

podman-:podman-run-app-shell

podman-:podman-build-run-app

podman-:podman-stop-ct

