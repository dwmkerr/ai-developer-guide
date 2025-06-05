# AI Developer Guide MCP Server

An MCP (Model Context Protocol) server that provides LLMs with access to the AI Developer Guide content, including core development principles and specialized deep dives.

## Installation

```bash
npm install -g @dwmkerr/ai-developer-guide-mcp
```

## Usage

### Start the MCP Server
```bash
ai-developer-guide-mcp start
```

### Test API Connectivity
```bash
ai-developer-guide-mcp test
```

### Monitoring and Logging

The server logs all activity to stderr (standard error) following MCP conventions. This means:

- **When running manually**: Logs appear directly in your terminal
- **When used with MCP clients**: Logs are captured by the client (e.g., Cursor's MCP console)
- **No file permissions needed**: No log files to manage or worry about

Logs include timestamps and detailed information about:
- Server startup and initialization
- Tool requests (list_tools, fetch_main_guide, etc.)
- API calls and response times
- Error messages and debugging information

## Example LLM Interactions

Once connected to your LLM (like Claude in Cursor), you can ask questions like these:

### **Getting Started**
> "What are the main principles in the AI Developer Guide?"

The LLM will use `fetch_main_guide` to get the core development principles and Plan/Implement/Review approach.

### **Language-Specific Guidance**
> "Show me Python best practices for AI-assisted development"
> 
> "What are the shell scripting guidelines from the developer guide?"

The LLM will use `fetch_deep_dive` with category `languages` and topics like `python` or `shell-scripts`.

### **Tool and Pattern Guidance**
> "How should I structure my Makefiles according to the guide?"
> 
> "What CI/CD practices does the guide recommend?"

The LLM will fetch guides for `patterns/make` or `others/cicd`.

### **Discovery and Exploration**
> "What deep dive guides are available?"
> 
> "List all the specialized guides you have access to"

The LLM will use `list_available_guides` to show all categories and topics.

### **Practical Scenarios**
> "I'm setting up a new Python project with PostgreSQL. What guidance does the developer guide provide?"

The LLM will fetch multiple guides (`languages/python` and `platforms/postgresql`) to give comprehensive advice.

> "Help me review this shell script using the developer guide principles"

The LLM will get the main guide for review principles, then the shell scripts deep dive for specific best practices.

## Configuration

### Custom Base URL

You can point the server to your own AI Developer Guide deployment in several ways:

**1. Environment Variable (recommended for persistent configuration):**
```bash
export AI_DEVELOPER_GUIDE_URL="https://your-domain.com/your-guide"
ai-developer-guide-mcp start
```

**2. Command Line Option:**
```bash
ai-developer-guide-mcp start --base-url "https://your-domain.com/your-guide"
```

**3. For Cursor MCP Configuration:**
```json
{
  "mcpServers": {
    "ai-developer-guide": {
      "command": "ai-developer-guide-mcp",
      "args": ["start", "--base-url", "https://your-domain.com/your-guide"]
    }
  }
}
```

**Priority order:** Command line option > Environment variable > Default (dwmkerr's GitHub Pages)

### API Requirements

Your custom guide must expose these endpoints:
- `/api.json` - API index with available guides
- `/api/guide.json` - Main guide content
- `/api/guides/{category}/{topic}.json` - Deep dive guides

The API structure should match the [AI Developer Guide API format](https://dwmkerr.github.io/ai-developer-guide/api.json).

## Available Tools

When connected to an LLM via MCP, the following tools are available:

- **`fetch_main_guide`** - Get the core AI Developer Guide content
- **`fetch_deep_dive`** - Get specialized guides (Python, Shell Scripts, Make, PostgreSQL, etc.)
- **`list_available_guides`** - List all available deep dive topics

## Connecting to Cursor

Add this configuration to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "ai-developer-guide": {
      "command": "ai-developer-guide-mcp",
      "args": ["start"]
    }
  }
}
```

## Development

```bash
# Install dependencies
make init

# Build the code
make build

# Run in development mode
npm run dev

# Test API connectivity
npm run dev -- test

# Test with custom URL
npm run dev -- test --base-url "http://localhost:9090"
```

## License

MIT 