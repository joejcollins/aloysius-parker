# Consistent set of make tasks.
.DEFAULT_GOAL:= help  # because it's is a safe task.

clean:  # Remove all build, test, coverage and Python artifacts.
	rm -rf .venv
	rm -rf *.egg-info
	find . -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

PIPTOOLS_COMPILE = .venv/bin/python -m piptools compile

compile:  # Compile the requirements files using pip-tools.
	rm -f requirements.*
	$(PIPTOOLS_COMPILE) --output-file=requirements.txt
	echo "# Add the entire project as a package." >> requirements.txt
	echo "-e ." >> requirements.txt
	$(PIPTOOLS_COMPILE) --allow-unsafe --extra=dev --output-file=requirements.dev.txt
	echo "# Add the entire project as a package." >> requirements.dev.txt
	echo "-e ." >> requirements.dev.txt

docker:  # Build the dev image.
	docker build \
		-t ghcr.io/zengenti/flask-forge-dev:latest \
		-f Dockerfile.dev \
		.
	echo $$REPO_AND_PACKAGES_TOKEN | docker login ghcr.io -u joejcollins --password-stdin
	docker push ghcr.io/zengenti/flask-forge-dev:latest

.PHONY: docs  # because there is a directory called docs.
docs:  # Build the documentation from the comments and documents.
	export TZ=UTC
	sphinx-apidoc -o docs/flask_forge src/flask_forge
	sphinx-autobuild docs docs/_build/html

flask:  # Run the Flask API server.
	.venv/bin/python -m flask --app 'src/flask_forge/main.py' run

format:  # Format the code with black.
	.venv/bin/python -m black --config pyproject.toml .

.PHONY: help
help: # Show help for each of the makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

kill: # Kill the servers on ports 5000 to 5005 if they are still running.
	lsof -i tcp:5000-5005 | awk 'NR!=1 {print $$2}' | xargs kill 2>/dev/null || true

lint:  # Lint the code with ruff, yamllint and ansible-lint.
	.venv/bin/python -m ruff check ./src ./tests
	.venv/bin/sourcery login --token $$SOURCERY_TOKEN
	.venv/bin/sourcery review ./src ./tests --check --no-summary

mypy:  # Type check the code with mypy.
	.venv/bin/python -m mypy ./src ./tests

report:  # Report the python version and pip list.
	whoami
	.venv/bin/python --version
	.venv/bin/python -m pip list -v

venv:  # Install the requirements for Python.
	python -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools
	.venv/bin/python -m pip install -r requirements.txt

venv-dev:  # Install the development requirements for Python.
	python -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools
	.venv/bin/python -m pip install -r requirements.dev.txt

test:  # Run the tests.
	.venv/bin/python -m pytest ./tests
