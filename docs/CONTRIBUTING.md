# Contributor Guide

Run `make` to see available recipes:

```
$ make

check-tokens: check the tokens in each file used by AI
cicd: run the CI/CD workflow locally.
help: show help for each of the Makefile recipes
site-build: build the the MCP server site
site-run: run a simple HTTP server for the site
```

## CI/CD

Test the CI/CD jobs with:

```bash
act -P ubuntu-24.04=ghcr.io/catthehacker/ubuntu:act-latest
```

Or:

```make
make cicd
```

## MCP

Check the [MCP Server README](../mcp/ai-developer-guide-mcp/README.md)
