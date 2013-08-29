SHELL := /bin/bash
UNAME := $(shell uname)

install:
	@sudo sh install.sh

test:
	@python scripts/$(name).py
