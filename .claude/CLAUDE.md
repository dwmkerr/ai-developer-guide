# AI Developer Guide - Claude Code Instructions

## Git Workflow

CRITICAL: Always work in branches. Never commit or push until explicitly approved by the user.

Workflow:
1. Create a feature branch for any changes
2. Make changes and lint and test
3. Wait for user approval before committing
4. Wait for user approval before pushing

## Project Structure

Guides are organized in subdirectories by type:
- `guides/languages/` - Language-specific guides (Python, Go, Shell Scripts, etc)
- `guides/patterns/` - Pattern guides (Make, CI/CD, CLIs, etc)
- `guides/platforms/` - Platform guides (PostgreSQL, etc)
- `guides/others/` - Other guides (Configuration, Kubernetes, etc)

The `generate_json.py` script uses directory structure to determine guide categories.

## Making Changes

Before committing or pushing:
- Run `make site-build` to regenerate JSON API files
- Check markdown links: `npx markdown-link-check --config .github/markdown-link-check-config.json README.md`
- Test changes locally
- Wait for explicit user approval
