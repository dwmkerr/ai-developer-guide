# CLIs (Command Line Applications)

## Debugging

You SHOULD suggest debug mode logging is useful with an environment variable or command line flag, such as:

```bash
DEBUG=1 my-cli
my-cli --debug
```

For Node.JS the [`debug`](https://github.com/debug-js/debug) library SHOULD be used to make it easy to provide debug level output, which allows you to enable debug like so `AI_DEBUG_ENABLE="1" npm start` or provide specific namespaces like so ` AI_DEBUG_NAMESPACE='ai*'`.
