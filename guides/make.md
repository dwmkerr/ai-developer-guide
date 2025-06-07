# Makefiles

We use makefiles throughout the project to standardize workflows across different platforms. This gives:

- **Consistency**: Common interface across all components regardless of underlying technology
- **Simplicity**: Hide platform-specific commands (npm, pip, etc.) behind standard targets

We have:

1. **Service-level Makefiles**: Each service has its own makefile with common targets (`setup`, `dev`, `clean`)
2. **Project-level Makefile**: Root makefile uses Docker Compose to orchestrate all services

You can always run `make help` for instructions on what recipes are available.

Makefiles are not the same as shell scripts. We don't use color, we limit to a few lines only, we rarely check variables. In general, anything that is complex can be passed to a shell script.

Makefiles ALWAYS have a `.PHONY` and a default `help` recipe. `.PHONY` always comes before the recipe name. Each recipe is documented with a one line comment like so:

```make
default: help

.PHONY: help
help: # Show help for each of the Makefile recipes
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: init
init: # set up and validate the local development environment
	./scripts/init.sh
```

Makefile recipes should be very small - a few commands only.

Makefiles give a 'platform independent' way to run commands, this means regardless of the programming language we will often have recipes like:

- `make init` - setup and validate the local development environment
- `make dev` - run a module in local development mode (e.g. live reload)
- `make lint` - validate formatting
- `make test` - test the code

This approach gives consistency, discoverability of commands, and helps users who are not familiar with a platforms toolchain still get quickly started and also see how key commands work.

We use makefiles throughout the project to standardize workflows across different platforms. This gives:

In a monorepo we have module level makefiles for working in one module. So `ui/makefile` would have a `dev` recipe that starts the UI only in development mode.

In a monorepo we have a project level makefile that is for working with the whole project - so `makefile` would have a `dev` recipe that starts ALL modules in development mode. This might call the module makefiles (e.g. a `make lint` recipe could just call each projects' `make lint`) or it might work differently, for example `make dev` might use docker compose to run a whole project.


