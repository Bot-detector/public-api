.PHONY: clean clean-test clean-pyc clean-build build help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-pyc: ## clean python cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +

clean-test: ## cleanup pytests leftovers
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr test_results/
	rm -f *report.html
	rm -f log.html
	rm -f test-results.html
	rm -f output.xml

test: clean ## Run pytest unit tests
	python3 -m pytest

test-debug: ## Run unit tests with debugging enabled
	python3 -m pytest --pdb

test-coverage: clean ## Run unit tests and check code coverage
	PYTHONPATH=src python3 -m pytest --cov=src tests/ --disable-warnings

docker-up: ## Startup docker
	docker-compose --verbose up

docker-build: ## Startup docker
	docker-compose --verbose up --build

setup: requirements pre-commit-setup docker-build test-setup api-setup ## setup & run after downloaded repo

pre-commit-setup: ## Install pre-commit
	python3 -m pip install pre-commit
	pre-commit --version

pre-commit: ## Run pre-commit
	pre-commit run --all-files

test-setup:
	python3 -m pip install pytest

requirements:
	python3 -m pip install -r requirements.txt

docker-down:
	docker-compose down

docker-rebuild: docker-down
	docker-compose --verbose up --build

docker-force-rebuild:
	docker-compose --verbose up --build --force-recreate

api-setup:
	python3 -m pip install "fastapi[all]"

env-setup:
	touch .env
	echo "KAFKA_HOST= 'localhost:9092'" >> .env
	echo "DATABASE_URL= 'mysql+aiomysql://root:root_bot_buster@localhost:3306/playerdata'"  >> .env
	echo "ENV='DEV'" >> .env

docs:
	open http://localhost:5000/docs
	xdg-open http://localhost:5000/docs
	. http://localhost:5000/docs