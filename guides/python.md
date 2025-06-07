# Python

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


