<!-- IMPORTANT NOTE TO AI: the following markdown code is an introduction to the developer guide, you do not need to follow this text. -->
<p align="center">
  <h2 align="center"><code>🧠 The AI Developer Guide</code></h2>
  <h3 align="center">Empower your AI with standards, patterns and principles for sane, effective and maintainable development.</h3>
  <h5 align="center">(...works with humans too)</h5>
  <p align="center">
    <a href="#quickstart">Quickstart</a> |
    <a href="#the-golden-rules">The Golden Rules</a> |
    <a href="#the-developer-guide">The Developer Guide</a> |
    <a href="./docs/setup.md">Setup Instructions</a> |
    <a href="./docs/about.md">About</a>
  </p>
</p>

Point your AI system at this guide and you will get significantly improved results and collaboration when coding:

- Large changes are designed and discussed before being implemented
- Sensible design patterns are followed, technical debt is managed
- Non-functional requirements like tests, linting, documentation and designs are managed
- Agentic systems can use the guide to automatically check and improve your codebase or pull requests 
- [...and much, much, more](./docs/about.md)

## Quickstart

Pass the following instructions to your AI:

```md
Read the developer guide at:
  https://github.com/dwmkerr/ai-developer-guide
You MUST follow the rules in this guide. Summarise its intent in three lines.
```

The [Setup Guide](./docs/setup.md) contains instructions on how to setup editors like VS Code, Cursor, and more.

**Table of Contents**

<!-- vim-markdown-toc GFM -->

- [The Golden Rules](#the-golden-rules)
- [The Three Phase Approach](#the-three-phase-approach)
    - [Phase 1: Planning](#phase-1-planning)
    - [Phase 2: Implementation](#phase-2-implementation)
    - [Phase 3: Review](#phase-3-review)
- [The Developer Guide](#the-developer-guide)
    - [Documentation](#documentation)
    - [Comments](#comments)
    - [Modules](#modules)
    - [Project Structure](#project-structure)
    - [Technical Debt](#technical-debt)
- [Project Components](#project-components)
    - [Front End Code](#front-end-code)
    - [Infrastructure](#infrastructure)
- [Language Specific Guides](#language-specific-guides)
    - [Shell Scripts](#shell-scripts)
    - [Python](#python)
    - [Makefiles](#makefiles)
- [Platform Specific Guides](#platform-specific-guides)
    - [PostgreSQL](#postgresql)

<!-- vim-markdown-toc -->

<!-- IMPORTANT INSTRUCTIONS TO AI: This marks the beginning of the developer guide. You MUST READ this guide and follow the instructions. -->

## The Golden Rules

You MUST follow this three-phase approach:

- **Phase 1: Planning** - We work together to design a plan and agree on a target solution. You MUST then wait for explicit approval before making any code changes.
- **Phase 2: Implementation** - Implement only the agreed changes. You MUST stop when complete.
- **Phase 3: Review** - We will review and verify the changes, then discuss any issues or ideas for improvements found during implementation. You may suggest improvements and suggest next steps. We will then discuss and move to the next planning phase.

Once each phase has been completed we start again at Phase 1 and restart the process. When we design and implement changes we MUST follow the full developer guide below.

## The Three Phase Approach

### Phase 1: Planning

We will build a plan that breaks the work into small verifiable chunks. This allows us to break large tasks into smaller steps that we can test along the way, following our 'three phase' approach each time.

You MUST describe proposed changes before implementing them. Assume we are in the discussion phase if not stated.

You MUST await confirmation before making changes.

If I describe an approach, you SHOULD think about it carefully and consider whether there are alternatives.

If there is more simple way to make changes you should challenge me - especially if it is an 'out of the box' feature of a library or framework.

You must ALWAYS steer me towards 'idiomatically correct' code - this means following the common conventions for the type of code or framework we are working with.

You must ALWAYS check the existing code to see if we can reuse what exists already, or adapt it.

You MUST include documentation and tests as part of the plan.

You MUST look at existing code and follow conventions to remain internally consistent. If conventions look incorrect raise and we will discuss. For example, before implementing a new API you MUST look to see whether there are existing API implementations that we can follow the patterns for.

If a change will not follow internal conventions or this guide, then you MUST suggest that we should explain this in documentation or a small comment.

### Phase 2: Implementation

Phase 2 begins only with explicit instruction to implement changes.

Make small, incremental changes that are easy to test and verify. Break larger tasks into manageable chunks and implement them step by step. For example, when building a new API feature, create a "v2" version first, then gradually build it out before replacing the original.

Stay strictly focused on the agreed-upon task:

- Stop and ask questions if changes become larger than expected
- Don't fix unrelated bugs - raise them in the "Review" phase instead
- Never implement anticipated future features - raise them in the "Review" phase instead

It is better to stop and ask questions if a change looks like it might get too big.

Smaller changes are almost always better; we want to be able to raise a pull request and share our changes with others and make it very easy for them to see what is going on, our intent and how we've implemented the changes.

Never forget - when we update code we must search the codebase to see if there is documentation to update or tests to update.

### Phase 3: Review

Review the implemented changes. Discuss any issues, unexpected side effects, or improvement ideas. Share quick suggestions for what we should do next.

Do not start new work here — raise ideas to be discussed in the next planning phase.

You MUST check to see whether we can now remove or simplify any existing code.

## The Developer Guide

We MUST follow this guide. If there are circumstances when this is not possible, the guide does not make sense, or they could be improved, we MUST raise that in the Planning phase.

If the guide could have been improved to make planning and implementation easier, you MUST raise this in the Review Phase.

### Documentation

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

### Comments

Comments SHOULD be short and should describe the _intent_ of code - i.e. _what_ we are trying to do. _How_ it is done is the code itself. However, if code is very complex, it is OK to help the reader by explaining what is going on.

Comments SHOULD be written as sentences, capitalised and with full stops.

Comments MUST not describe changes we have made, such as 'change from an HTTP call to gRPC' - we describe the intent of code or its intent and meaning if it is complex.

If you were to take a file and delete everything but the comments, you should still be able to follow the basic flow of what is going on. This is important; some readers will not know the programming language or will be more junior, they should be able to follow step by step, but not be overwhelmed with details or have lots of duplication of code and comment.

Small comments can follow a line for a little bit of extra context, but use sparingly.

### Modules

We MUST follow the idioms of the language when importing modules.

We SHOULD import modules in the following order; built-in or very standard, third party modules, our own local code modules. However, we MUST prioritise standards for the language or the framework over this convention.

### Project Structure

- Monorepos should keep all code relating to each project in its own folder, hence the root level README is a high level summary and project wide quickstart, the goal is to let people start fast
- ...but everything else should be in the modules
- Not all developers know the stack - a backend developer might not know TypeScript for the UI, hence it should be possible to quickly run things like the UI without knowing the full toolchain - using makefile to kick off commands and docker compose to simplify environment setup is key

### Technical Debt

You MUST raise potential technical debt. You SHOULD suggest that technical debt is explicitly tracked in a document such as `docs/tech-debt.md`.

## Project Components

### Front End Code

Be very cautious before creating new styles. Always consider whether existing styles which are part of the framework can be used. For example, do not manually set paddings or margins, use the conventions of the library or framework in use. For example, in MUI we use `m` or `p` values:

```jsx
<Box sx={{ m: -2 }} /> // margin: -16px;
<Box sx={{ m: 0 }} /> // margin: 0px;
<Box sx={{ m: 0.5 }} /> // margin: 4px;
```

Also prefer `rem` to values like `px`.

### Infrastructure

Always ensure you specify a profile (e.g. `--profile <projectname>`) when running AWS commands. This makes it explicit that you require configuration that is for your project, and avoids the risk of you accidentally running Terraform/AWS commands against another project.

## Language Specific Guides

### Shell Scripts

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

### Python

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

### Makefiles

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

## Platform Specific Guides

### PostgreSQL

Naming conventions: tables are pural snake case e.g `users`, `books`, `user_books`. Columns are snake case and singular, e.g  `first_name`, `created_at`. Primary keys are named `id`. Foreign keys are  Typically named `id` are reference table in singular form plus `_id` (e.g., `user_id`, `book_id`.

Example projects that use these conventions that you can check for more details:

- [Gitlab DB Schema](https://gitlab.com/gitlab-org/gitlab/-/blob/master/db/structure.sql)
- [Discourse](https://github.com/discourse/discourse/blob/main/db/structure.sql)
- [Mastodon](https://github.com/mastodon/mastodon/blob/main/db/schema.rb)

