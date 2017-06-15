#-*- Makefile -*-

ifdef DEBUG
# Tests debug mode enabled (SKIPPER_INTERACTIVE must be set for this to work)
DEBUGGER=--debugger
MULTIPROCESS=
else
# Tests debug mode disabled
DEBUGGER=
MULTIPROCESS=-N 4
endif

# Service version based on git revision
VERSION=$(shell git rev-parse HEAD)

PWD=`pwd`
RPM_BUILD_ROOT ?= $(PWD)/build/rpmbuild

all: flake8 pylint coverage subsystem rpm

flake8:
	flake8 srv1 tests

pylint: srv1-client/srv1_client/client.py
# Create the reports directory
	mkdir -p reports/
	PYLINTHOME=reports/ pylint -r n srv1 tests

coverage: unittest
# Create a coverage report and validate the given threshold
	coverage html --fail-under=40 -d reports/coverage

unittest: srv1-client/srv1_client/client.py
# Create the reports directory
	mkdir -p reports/
	coverage erase
	nose2 --config=tests/ut/nose2.cfg --verbose --project-directory . $(DEBUGGER) $(MULTIPROCESS) $(TEST)

dist/srv1-*.tar.gz: setup.py $(shell find srv1) $(shell find etc)
# Generate srv1 tarball, then cleanup
	python setup.py sdist
	rm -rf dist/*.src.rpm dist/*.egg

srv1-client/dist/srv1-client-*.tar.gz: srv1-client/setup.py srv1-client/srv1_client/client.py $(shell find srv1) srv1-client/api-docs/srv1.json
	cd srv1-client/ && python setup.py sdist

subsystem: build
	mkdir -p logs/ reports/
	touch logs/srv1.stratolog

	CONFIG=tests/subsystem/nose2.cfg \
	PYTHONPATH=PYTHONPATH:./srv1-client \
	nose2 --config=tests/subsystem/nose2.cfg --verbose --project-directory . $(DEBUGGER) $(TEST)

build: dist/srv1-*.tar.gz srv1-client/dist/srv1-client-*.tar.gz
	skipper build srv1
	docker tag srv1:$(VERSION) srv1:last_build

rpm: $(shell find deploy -type f)
	rpmbuild -bb -vv --define "_srcdir $(PWD)" --define "_topdir $(RPM_BUILD_ROOT)" deploy/srv1-deploy.spec

srv1-client/srv1_client/client.py: $(shell find srv1/* | grep -v \.pyc) client_generator.py
	python client_generator.py $@

srv1-client/api-docs/srv1.json: $(shell find srv1/resources/*)
	mkdir -p srv1-client/api-docs
	python -m hammock.doc srv1.resources.api.v2 --json > $@

clean:
	rm -rf dist reports *.egg-info build logs .eggs
	rm -rf srv1-client/srv1_client/client.py srv1-client/dist srv1-client/*.egg-info srv1-client/api-docs/
	find -name "*.pyc" -delete
	find -name "*~" -delete

push: build
	skipper push srv1

deploy: push
	skipper run deploy $(NORTHBOUND_IP) srv1 $(VERSION) --image-name srv1
