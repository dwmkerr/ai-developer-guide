# Shell Scripts

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


