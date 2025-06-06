default: help

.PHONY: help
help: # Show help for each of the Makefile recipes
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: init
init: # Install dependencies
	npm install

.PHONY: lint
lint: # Lint code
	npm run lint

.PHONY: lint-fix
lint-fix: # Lint and fix
	npm run lint:fix

.PHONY: test
test: # Run unit tests and output coverage to artifacts/coverage
	mkdir -p artifacts/coverage
	npm run test

.PHONY: build
start: # Build the code for distribution
	npm run start

.PHONY: build
build: # Build the code for distribution
	npm run build