.PHONY: all

SHELL=/bin/bash -e

.DEFAULT_GOAL := help

DCF_LOCAL = docker-compose

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint:
	poetry run python -m flake8 ./
	poetry run python -m mypy ./

format:
	poetry run python -m isort ./
	poetry run black --fast ./

build: ## build dev images
	${DCF_LOCAL} build

up: ## start docker dev environment
	${DCF_LOCAL} up -d
	${DCF_LOCAL} ps

up-no-detach: ## start docker dev environment
	${DCF_LOCAL} up

down: ## stop docker dev environment
	${DCF_LOCAL} down --remove-orphans

purge: ## stop docker dev environment and remove orphans and volumes
	${DCF_LOCAL} down --volumes --remove-orphans

exec-app: # execute app container in bash
	${DCF_LOCAL} exec app bash

migrate: ## migrate dev
	${DCF_LOCAL} exec app python manage.py migrate --noinput

makemigrations: ## makemigrations dev
	${DCF_LOCAL} exec app python manage.py pgmakemigrations

collectstatic: ## collectstatic dev
	${DCF_LOCAL} exec app python manage.py collectstatic --noinput

createsuperuser:
	${DCF_LOCAL} exec app python manage.py createsuperuser

logs:  ## show logs for app container
	${DCF_LOCAL} logs -f app

test: # run tests
	${DCF_LOCAL} exec app pytest

pre-commit-enable: ## Enable pre-commit
	poetry run pre-commit install

pre-commit-disable: ## Disable pre-commit
	poetry run pre-commit uninstall