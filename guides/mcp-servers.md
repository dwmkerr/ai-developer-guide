# MCP Servers

Model Context Protocol (MCP) servers provide tools for AI agents.

## Tool Documentation

MCP tool docstrings serve as API documentation for AI agents. Unlike human-facing code, agents require rich descriptions to understand capabilities and constraints.

**Exception to lean comment rules:** MCP tools need detailed docstrings since agents rely on them for tool selection and usage.

## Docstring Structure

```python
@mcp.tool
async def kubectl(args: str) -> str:
    """Execute kubectl commands for Kubernetes cluster management.
    
    Use this tool for all kubectl operations. Provide the kubectl 
    arguments as a single string (e.g., "get pods -n default").
    
    Args:
        args: kubectl command arguments
        
    Returns:
        Command output with stdout, stderr, and return code
    """
```

**Poor example:**
```python
@mcp.tool
async def kubectl(args: str) -> str:
    """Run kubectl."""
```

## Implementation Patterns

- Use `FastMCP` for Python implementations
- Include health check endpoints
- Provide tool discovery via system info functions
- Handle errors gracefully with context

## Project Structure

```
mcp-server/
├── Makefile
├── README.md
├── pyproject.toml
├── requirements.txt
└── src/
    └── server_name/
        ├── __init__.py
        ├── __main__.py
        └── server.py
```

## Standard Makefile Recipes

```makefile
.DEFAULT_GOAL := help

help: # Show available commands
	@grep -E '^[a-zA-Z0-9 -]+:.*#' Makefile | sort

init: # Install dependencies
	uv sync

dev: # Run server locally
	uv run python -m server_name

build: # Build container
	docker build -t server-name .
```