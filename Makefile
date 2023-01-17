.PHONY: docs test help
.DEFAULT_GOAL := help

SHELL := /bin/bash

ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

export ROOTDIR:=$(shell pwd)
export CURRENT_VERSION:=$(shell cat ${ROOTDIR}/virus_total_telegram_bot/_meta.py  | sed -En "s/^__version__\s*=\s*[ubrf]*['\"]([^'\"]+)['\"].*$$/\1/p")
export CURRENT_USER:=$(shell id -u ${USER}):$(shell id -g ${USER})

# Docker configuration
export IMAGE_NAME:=$(or $(IMAGE_NAME), virus_total_telegram_bot)
export IMAGE_VERSION:=$(or $(IMAGE_VERSION), $(CURRENT_VERSION))

help:
	@echo -e "You can run tasks with:\n\n$$ make \033[36m<task name>\033[0m\n\nwhere \033[36m<task name>\033[0m is one of the following:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# Environment

env-create: ## (re)create a development environment using tox
	tox -e virus_total_telegram_bot --recreate
	@echo -e "\r\nYou can activate the environment with:\r\n\r\n$$ source ./.tox/virus_total_telegram_bot/bin/activate\r\n"

env-compile: ## compile requirements.txt / requirements-dev.txt using pip-tools
	@pip-compile --no-emit-index-url --no-header --no-emit-trusted-host --output-file requirements.txt requirements.in
	@pip-compile --no-emit-index-url --no-header --no-emit-trusted-host --output-file requirements-dev.txt requirements-dev.in

# Development

install: ## install the package
	pip install --no-cache-dir $(PIP_ARGS) .

uninstall: ## uninstall the package
	pip uninstall -y $(PIP_ARGS) virus_total_telegram_bot || true

develop: uninstall ## install the package in development mode
	pip install --editable $(PIP_ARGS) .

lint: ## static code analysis with pylint
	pylint --rcfile virus_total_telegram_bot/.pylintrc virus_total_telegram_bot

lint-tests: ## static test code analysis with pylint
	pylint --rcfile tests/.pylintrc tests

code-style: ## check code style against PEP8 conventions
	pycodestyle virus_total_telegram_bot

code-maintainability: ## calculates a maintainability index using radon
	radon mi -s virus_total_telegram_bot

code-locs: ## display metrics (LOCs, number of comments, etc.)
	radon raw --summary virus_total_telegram_bot

code-complexity: ## check cyclomatic complexity using radon
	xenon --max-absolute B --max-modules A --max-average A virus_total_telegram_bot

code-metrics: ## check cyclomatic complexity and print LOCs and maintainability index
	@echo -e "Code complexity:\n" && $(MAKE) code-complexity && \
	echo -e "\nMaintainability:\n" && $(MAKE) code-maintainability && \
	echo -e "\nMetrics:\n" && $(MAKE) code-locs

test: ## run tests with pytest and calculate coverage
	py.test --cov virus_total_telegram_bot --cov-report term --cov-fail-under 80 \
		    --cov-report html:docs/_build/coverage/$(or $(REPORT_NAME), $(or $(TOX_ENV_NAME), pytest)) \
		    --cov-report xml:docs/_build/coverage/$(or $(REPORT_NAME), $(or $(TOX_ENV_NAME), pytest))/coverage.xml \
		    --html=docs/_build/test-reports/$(or $(REPORT_NAME), $(or $(TOX_ENV_NAME), pytest))/index.html \
			--junitxml=docs/_build/test-reports/$(or $(REPORT_NAME), $(or $(TOX_ENV_NAME), pytest))/junit.xml \
			-o junit_suite_name=$(or $(REPORT_NAME), $(or $(TOX_ENV_NAME), pytest))

security: ## check source code for vulnerabilities
	@[ "${REPORT_FORMAT}" ] && ( mkdir -p docs/_build/security && bandit -v -r -f ${REPORT_FORMAT} -o docs/_build/security/index.html virus_total_telegram_bot &> /dev/null ) || true
	bandit -v -r virus_total_telegram_bot

check-dependencies: ## check dependencies for vulnerabilities using safety
	safety check --full-report

docs: ## generate project docs
	rm -rf site && mkdir -p site/reference/api
	python docs/generate_openapi.py
	mkdocs build

docs-serve: ## starts a server with the docs using mkdocs
	mkdocs serve

# Package & Publish

version: ## get the current package version
	@echo $(CURRENT_VERSION)

version-bump: ## bump the version on the specified PART
	bump2version --current-version $(CURRENT_VERSION) $(PART)

version-bump-tag: ## bump and tag the version on the specified PART
	bump2version --commit --tag --current-version $(CURRENT_VERSION) $(PART)

version-set: ## set the version to the specified VERSION
	bump2version --current-version $(CURRENT_VERSION) --new-version $(VERSION) minor

version-set-tag: ## set and commit the version to the specified VERSION
	bump2version --commit --tag --current-version $(CURRENT_VERSION) --new-version $(VERSION) minor

dist: clean-build clean-pyc ## build wheel package (compiled)
	python setup.py bdist_wheel --cythonize

dist-dev: clean-build clean-pyc ## build wheel package (source code)
	python setup.py bdist_wheel

sdist: clean-build clean-pyc ## build a source distribution (sdist)
	python setup.py sdist

publish: ## publish packages to the repository
	@echo -e "TODO"

# Docker

docker-run: ## run the specified command on docker (defaults to /bin/bash)
	docker-compose -f docker/dev/docker-compose.yml run --rm -u $(CURRENT_USER) virus_total_telegram_bot $(or $(COMMAND),  $(MAKE) $(TARGET))

docker-shell: ## drop the user into a shell inside a docker container
	docker-compose -f docker/dev/docker-compose.yml run --rm -u $(CURRENT_USER) virus_total_telegram_bot

docker-lint: ## lint the Dockerfile using hadolint (on Docker)
	@echo -e "TODO"

docker-build: ## build the production docker image
	@docker build --pull -f docker/prod/Dockerfile \
		--build-arg BUILD_DATE=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg VERSION=$(CURRENT_VERSION) \
		--build-arg REVISION=$(REVISION) \
		-t $(IMAGE_NAME):$(IMAGE_VERSION) .

docker-pull: ## pull the docker image from the remote registry
	docker pull $(IMAGE_NAME):$(IMAGE_VERSION)

docker-push: ## push the docker image to a remote registry
	docker push $(IMAGE_NAME):$(IMAGE_VERSION)

docker-security: ## scan the docker image for security vulnerabilities
	@mkdir -p ./docs/_build/docker-security
	trivy --ignore-unfixed --exit-code 0 -f template -t "@/opt/trivy/report.tpl" -o ./docs/_build/docker-security/report.html $(IMAGE_NAME):$(IMAGE_VERSION)
	trivy --ignore-unfixed --exit-code 0 -f json -o ./docs/_build/docker-security/report.json $(IMAGE_NAME):$(IMAGE_VERSION)

docker-package: ## package an image as a tar archive
	@mkdir -p ${ROOTDIR}/dist
	docker save -o ${ROOTDIR}/dist/virus_total_telegram_bot-$(IMAGE_VERSION).tar $(IMAGE_NAME):$(IMAGE_VERSION)

# Continuous integration

ci-all: # simulate the complete CI pipeline by running all the ci-* targets
	$(MAKE) clean && \
	$(MAKE) ci-prepare && \
	$(MAKE) ci-test && \
	($(MAKE) ci-coverage || true) && \
	($(MAKE) ci-lint || true) && \
	($(MAKE) ci-code-style || true) && \
	($(MAKE) ci-security || true) && \
	($(MAKE) ci-check-dependencies) && \
	($(MAKE) ci-code-metrics || true) && \
	$(MAKE) ci-docs && \
	$(MAKE) ci-dist-dev && \
	$(MAKE) ci-dist

ci-prepare: clean ## prepares the environment to run on CI (Github)
	tox -e py38,virus_total_telegram_bot

ci-lint: ## lint code & tests on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) lint-tests
	tox -e virus_total_telegram_bot -- $(MAKE) lint

ci-code-style: ## check code style on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) code-style

ci-code-metrics: ## display metrics and check cyclomatic complexity (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) code-metrics

ci-security: ## checks the source code for known security vulnerabilities (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) security REPORT_FORMAT=html

ci-check-dependencies: ## check dependencies for vulnerabilities using safety (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) check-dependencies

ci-test: ## run tests on CI (Github)
	tox -e $(or $(ENV_NAME), $(shell echo "py38")) -- $(MAKE) test REPORT_NAME=$(ENV_NAME)

ci-docs: ## generate docs on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) docs

ci-version-set: ## set the version to the specified VERSION on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) version-set VERSION="${VERSION}"

ci-dist: ## build the wheel package on CI (Github)
	tox -e $(or $(ENV_NAME), $(shell echo "py38")) -- $(MAKE) dist

ci-dist-dev: ## build the wheel package (for development, non cythonized) on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) dist-dev

ci-publish: ## publish built packages to the appropriate repository on CI (Github)
	tox -e virus_total_telegram_bot -- $(MAKE) publish ## publish the packages generated with dist or dist-dev on CI (Github)

ci-release: ci-dist ci-publish ## build and publish the wheel package on CI (Github)

ci-release-dev: ## build and publish the wheel package (for development, non cythonized) on CI (Github)
	@[ "${VERSION}" ] && ( make ci-version-set )
	$(MAKE) ci-dist-dev ci-publish

ci-release-docker: ## lint, build, scan and push the docker image
	@echo -e "TODO"

# Cleanup

clean: clean-build clean-dist clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-all: clean clean-env clean-docker ## remove everything (artifacts, environments & docker)

clean-docs: ## remove auto-generated docs
	rm -fr docs/_build

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find . ! -path './.tox/*' -name '*.egg-info' -exec rm -fr {} +
	find . ! -path './.tox/*' -name '*.egg' -exec rm -f {} +
	find virus_total_telegram_bot -name '*.c' -exec rm -f {} +

clean-dist: ## remove dist packages
	rm -fr dist/

clean-pyc: ## remove Python file artifacts
	find . ! -path './.tox/*' -name '*.pyc' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*.pyo' -exec rm -f {} +
	find . ! -path './.tox/*' -name '*~' -exec rm -f {} +
	find . ! -path './.tox/*' -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -f .coverage

clean-env: ## remove virtual environments (created by tox)
	rm -fr .tox/

clean-docker: ## remove Docker images, containers, etc.
	docker-compose -f docker/dev/docker-compose.yml down --rmi local --volumes --remove-orphans