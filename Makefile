SHELL := /bin/bash -O extglob

# Dev

ENV_DEV := .env_dev

$(ENV_DEV):
	virtualenv $(@)
	$(@)/bin/pip install -e .

.PHONY: test
test: | $(ENV_DEV) credentials.json
	$(ENV_DEV)/bin/twtrgrep -m 1 .

credentials.json:
	$(info Run python ./auth_setup.py to generate credentials)
	$(error $(@) not found)
