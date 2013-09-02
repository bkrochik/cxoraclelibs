SHELL := /bin/bash
UNAME := $(shell uname)

install:
	@sudo sh install.sh

test:
	@python tests/$(name).py

test-all:
	@python -m unittest discover tests '*.py'
