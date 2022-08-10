V=$(shell git describe --tags --abbrev=0 | sed "s/v//")
PYPI_TEST_REPO=https://test.pypi.org/simple/
USERNAME='__token__'
PASSWORD='foo'

poetry.install:
	poetry install

poetry.config.native:
	poetry config virtualenvs.create false

poetry.config.venv:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.path .

bump.version:
	poetry version $(V)
	sed 's/=.*/= "$(V)"/' -i bb_wrapper/__init__.py

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

pypi.repo.test:
	poetry config repositories.testpypi $(PYPI_TEST_REPO)

package.publish.test:
	poetry publish -r testpypi -u $(USERNAME) -p $(PASSWORD)

package.publish:
	poetry publish -u $(USERNAME) -p $(PASSWORD)

package.build_and_publish: package.build package.publish

install.test:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bb-wrapper==$(V)
