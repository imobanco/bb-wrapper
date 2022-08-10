poetry.install:
	poetry install

poetry.config.native:
	poetry config virtualenvs.create false

poetry.config.venv:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.path .

bump.version:
	poetry version $(shell git describe --tags --abbrev=0)
	sed "s/__version__ = '0.0.0'/__version__ = '$(shell git describe --tags --abbrev=0 | sed "s/v//")'/" -i bb_wrapper/_version.py

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

package.build: bump.version
	poetry build

pypi.test:
	poetry config repositories.testpypi https://test.pypi.org/legacy/

package.publish.test:
	poetry publish -r testpypi

install.test:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bb-wrapper

