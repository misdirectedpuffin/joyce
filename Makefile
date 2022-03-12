clean:
	find . | grep -E "(__pycache__|.py[co]$\)" | xargs rm -rf
	rm -f .coverage
	rm -rf coverage build htmlcov dist **/*.egg*

format:
	black ./src ./tests --line-length 79 --exclude migrations

ensure-format:
	black ./src ./tests --line-length 79 --check --diff --exclude migrations

docker-freeze:
	# This means we do not have to install psycopg2 or postgres libs locally.
	docker exec web /usr/local/bin/pip freeze > requirements.txt

freeze:
	pip freeze > requirements.txt

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

build:
	python setup.py bdist_wheel

lint:
	find ./src ./tests -name '*.py' -not -path "*migrations*" | xargs pylint --rcfile=setup.cfg

unit:
	python -m pytest tests/ -vvv

test: format lint unit

.PHONY: install install-dev lint unit test