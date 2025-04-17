# Developer Guide

This guide describes how we design code, write code, think about quality and solve problems.

We MUST follow this guide. If there are circumstances when this is not possible, the guide does not make sense, or they could be improved, we SHOULD raise that in discussions or pull requests, so that we can improve the standards or agree to an exception from the standards for a particular case. Exceptions to the standards should always been explained and documented.

<!-- vim-markdown-toc GFM -->

- [Documentation](#documentation)
- [Comments](#comments)
- [Shell Scripts](#shell-scripts)
- [Makefiles](#makefiles)
- [Makefile Pattern](#makefile-pattern)
- [Python Code](#python-code)
- [Project Structure and Mono Repo Best Practices](#project-structure-and-mono-repo-best-practices)
- [Infrastructure](#infrastructure)
- [Front End Code](#front-end-code)
    - [Styling](#styling)
- [PostgresSQL](#postgressql)

<!-- vim-markdown-toc -->

## Documentation

- One README per project. A mono-repo has a root README showing how to use the entire solution, with project-level READMEs explaining how to work with each component in detail.
- Keep documentation short and simple.
- Do not use lots of examples or snippets that will quickly go out of date.
- Documentation SHOULD typically follow a flow such as "Quickstart" then move into more details, then have more advanced features later on.
- Whenever you are changing the code, double check to see whether you need to update the documentation.

A good example of short-and-simple is this:

    ## Quickstart

    Setup your environment and run the project:

    ```bash
    # Setup your machine. Gives instructions for anything which is missing.
    make init

    # Install all dependencies/build the code.
    make install

    # Run in development mode.
    make dev
    ```

    That's it. The rest of this guide covers more advanced topics like testing, deployment and monitoring.

Note that we don't need every project to follow this exact structure, but this shows how we prefer short and sweet code examples rather than lots of exposition.

Good examples of READMEs:

- A readme for a CLI application - focused on helping the user understand the tool quickly: https://github.com/dwmkerr/terminal-ai/blob/main/README.md

Prefer a `docs` folder for more detailed documentation such as configuration guides, installation guides and advanced features.

Websites generated from Markdown documentation should be used for complex projects, here are two good examples:

- https://www.tensorzero.com/docs/

## Comments

Comments should be short and should describe the _intent_ of code - i.e. _what_ we are trying to do. _How_ it is done is the code itself. However, if code is very complex, it is OK to help the reader by explaining what is going on.

Comments should be written as sentences, capitalised and with full stops.

If you were to take a file and delete everything but the comments, you should still be able to follow the basic flow of what is going on. This is important; some readers will not know the programming language or will be more junior, they should be able to follow step by step, but not be overwhelmed with details or have lots of duplication of code and comment.

Small comments can follow a line for a little bit of extra context, but use sparingly.

## Shell Scripts

**Fundamentals**

Use Bash and the most portable shebang: `#!/usr/bin/env bash`.
Fail fast: `set -e -o pipefail`.
Fail fast: if required parameters or environment variables are not set, fail and explain what is missing.
Don't be too smart: if a required parameter is missing, don't offer a way to input it with `read`.
Variables in shell scripts are lowercase. Only _environment variables_ should be uppercase.
If something isn't set or is missing, don't offer an option to read input, fail instead.
If shell scripts get longer than a page, they're likely too complex and suggest we look at alternatives.

**Output**

Preferred output style is unix-like, e.g:

```
verifying OpenAI credentials...
error: OpenAI key is not set
```

Note that this is lowercase and if we are going to do a long operation we use elipses.

Emojis should be used extremely sparingly, if at all.

For scripts that are doing lots of verifications or checks, it is OK to use the check: `✔` this check should be colored green, it is OK to use escape codes, give them useful names like `${green}`. Be sparing with color.

**Examples**

This snippet is small and simple, lowercase variables, sparing use of color. Not that the error message states EXACTLY what environment variable is not set.

```bash
if [ -z "$OPENAI_API_KEY" ]; then
  echo -e "${red}error${nc}: OPENAI_API_KEY not set"
  exit 1
fi
```

## Makefiles

## Makefile Pattern

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

## Python Code

Follow PEP8 standards. We allow max line lengths to be extended to 120.

Project SHOULD have a `makefile` with recipes:
- `init`: install dependencies
- `lint`: lint code
- `lint:fix`: lint and fix
- `test`: run unit tests and output coverage to `artifacts/coverage`
- `build`: build the code for distribution (optional)
- `deploy`: deploy the code (optional)

Organise code in a `src` directory, tests in a separate `tests` directory.

**Requirements**

To track requirements for development only dependencies, create a `requirements-dev.txt` file which includes `requirements.txt`:

```txt
-r requirements.txt # include regular requirements
pytest==8.3.5 # testing library only needed in dev mode
```

We SHOULD pin requirement version numbers to ensure deterministic resolution of dependencies.

We SHOULD put a comment after each requirement briefly stating what it is for - some developers will be unfamiliar even with common requirements.

**Exception Handling**

There must be exception handling at the 'domain boundary' level. This means that in Python code when we are handling a request we are in the domain of our code, but an exception must be exposed _outside_ of the domain as an HTTP status code. So HTTP handlers must catch and transform exceptions. For a CLI app, the domain is the internal code and its boundary is where we translate and show output in `stderr`, `stdout` and with a status code. We must always have exception handlers in boundaries like this; but remember many libraries will have basic handling of this already.

When we do our own exception handling, it is to make sure that we provide additional context and diagnostic information. It is NOT to make it 'appear' like our code has worked. See these examples:

```python
# This is very bad. Our exception handler provides log information, but masks the fact
# to the caller that our database call failed. We should fail and find the root cause.
try:
    # Load database data...
except Exception as e:
    logger.error(f"Error loading YAML database: {str(e)}")
    # Return a minimal valid structure (VERY BAD - DO NOT DO THIS)
    return {"books": [], "library": []}

# This is good. We provide some logging, and raise a new exception with more context.
except Exception as e:
  logger.error(f"Error loading YAML database: {str(e)}")
  raise RuntimeError(f"Failed to load database: {str(e)}")
```

Remember; in many cases it is OK to not catch exceptions. For example if an HTTP handler loads a file then we don't need to catch file exceptions, if the file is missing then the HTTP handler domain boundary exception handler will catch the exception and log it - file not found errors will be clear from the logs. Catch exceptions when we can provide useful and meaningful context.

Excellent example projects.

- [pytest](https://github.com/pytest-dev/pytest) - Uses `src` for implementation and `testing` for test files
- [Flask](https://github.com/pallets/flask) - Organizes core code in `src/flask` with a separate `tests` directory
- [Requests](https://github.com/psf/requests) - Follows the `src/requests` and `tests` pattern for clean separation

## Project Structure and Mono Repo Best Practices

- This project is a monorepo
- Monorepos should keep all code relating to each project in its own folder, hence the root level README is a high level summary and project wide quickstart, the goal is to let people start fast
- ...but everything else should be in the modules
- Not all developers know the stack - a backend developer might not know TypeScript for the UI, hence it should be possible to quickly run things like the UI without knowing the full toolchain - using makefile to kick off commands and docker compose to simplify environment setup is key

## Infrastructure

- Always ensure you specify a profile (e.g. `--profile <projectname>`) when running AWS commands. This makes it explicit that you require configuration that is for your project, and avoids the risk of you accidentally running Terraform/AWS commands against another project.

## Front End Code

### Styling

Be very cautious before creating new styles. Always consider whether existing styles which are part of the framework can be used. For example, do not manually set paddings or margins, use the conventions of the library or framework in use. For example, in MUI we use `m` or `p` values:

```jsx
<Box sx={{ m: -2 }} /> // margin: -16px;
<Box sx={{ m: 0 }} /> // margin: 0px;
<Box sx={{ m: 0.5 }} /> // margin: 4px;
```

Also prefer `rem` to values like `px`.

## PostgresSQL

Naming conventions: tables are pural snake case e.g `users`, `books`, `user_books`. Columns are snake case and singular, e.g  `first_name`, `created_at`. Primary keys are named `id`. Foreign keys are  Typically named `id` are reference table in singular form plus `_id` (e.g., `user_id`, `book_id`.

Example projects that use these conventions that you can check for more details:

- [Gitlab DB Schema](https://gitlab.com/gitlab-org/gitlab/-/blob/master/db/structure.sql)
- [Discourse](https://github.com/discourse/discourse/blob/main/db/structure.sql)
- [Mastodon](https://github.com/mastodon/mastodon/blob/main/db/schema.rb)

