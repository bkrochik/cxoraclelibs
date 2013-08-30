SHELL := /bin/bash
UNAME := $(shell uname)

install:
	@sudo sh install.sh

test:
	@python tests/$(name).py
