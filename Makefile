poetry.install:
	poetry install

poetry.config.native:
	poetry config virtualenvs.create false

poetry.config.venv:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.path .

config.env:
	cp .env.sample .env

test:
	python -m unittest $(args)

fmt:
	black .
	make fmt.check

fmt.check:
	black --check .
	flake8

coverage:
	coverage run -m unittest
	coverage report
	coverage xml

package.build:
	python setup.py sdist bdist_wheel
	
