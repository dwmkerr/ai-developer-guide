# MCP Servers

Model Context Protocol (MCP) servers provide tools for AI agents.

## Tool Documentation

MCP tool docstrings serve as API documentation for AI agents. Unlike human-facing code, agents require rich descriptions to understand capabilities and constraints.

**Exception to lean comment rules:** MCP tools need detailed docstrings since agents rely on them for tool selection and usage.

Specify input and output structures clearly. For command execution tools, return structured JSON with stdout, stderr, and status code.

## Docstring Structure

```python
@mcp.tool
async def kubectl(args: str) -> str:
    """Execute kubectl commands for Kubernetes cluster management.
    
    Use this tool for all kubectl operations. Provide the kubectl 
    arguments as a single string (e.g., "get pods -n default").
    
    Args:
        args: kubectl command arguments (string)
        
    Returns:
        JSON string with structure:
        {
            "stdout": "command output",
            "stderr": "error output", 
            "statusCode": 0
        }
    """
```

**Poor example:**
```python
@mcp.tool
async def kubectl(args: str) -> str:
    """Run kubectl.
    
    Returns:
        Output: <stdout>
    """
```