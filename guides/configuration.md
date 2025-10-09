# Configuration

## Configuration Precedence

Configuration is applied in order, with later sources overriding earlier ones:

1. System configuration (`/etc/gitconfig`)
2. User configuration (`~/.gitconfig`)
3. Local configuration (`.git/config`)
4. Environment variables (`GIT_AUTHOR_NAME=...`)
5. Command line parameters (`git commit --author=...`)

This pattern is used by Git, SSH, and many Unix tools. Use this hierarchy to allow system defaults, user preferences, project settings, runtime environment, and explicit overrides.

## Environment Variables

Environment variables are strings in the OS. Convert them in your application.

Booleans: Use `1` for true. Anything that is not `1` is false. Don't parse "true", "false", "yes", "no" - it is brittle and opinionated.

Required values: Fail fast if required configuration is missing.
