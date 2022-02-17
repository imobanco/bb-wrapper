pip.install:
	pip install --upgrade --requirement requirements-dev.txt

pip.install.build:
	pip install --upgrade --requirement requirements-build.txt

poetry.install:
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.path .
	poetry install

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

docs.start:
	sphinx-quickstart

docs.autodoc:
	sphinx-apidoc --force --output-dir docs/ .

docs.build:
	sphinx-build docs/ docs/build/
	touch docs/build/.nojekyll

package.build:
	python setup.py sdist bdist_wheel
	
