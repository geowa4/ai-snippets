# ai-snippets

A place to store code and other snippets I've used in my AI projects.

No single snippet is allowed to be complex or else it is not a snippet.
Assume all code was created with assistance from some LLM or coding agent.

## MCP Server

This repository includes an MCP (Model Context Protocol) server that provides access to all snippets through a standardized interface.

### Automated Installation (Recommended)

Use the `install.sh` script to install the MCP server manager to your PATH:

```bash
# Random port assignment (recommended)
./install.sh /usr/local/bin

# Fixed port (optional)
./install.sh /usr/local/bin 8080
```

This creates an `ai-snippet-mcp` script that automatically manages the container lifecycle. Use it with Claude Code:

```bash
claude --mcp-config "$(ai-snippet-mcp)"
```

The script will:

- Pull the latest changes from git (if no local modifications)
- Rebuild the container only when necessary
- Start the container on a random available port (or fixed port if specified)
- Return the MCP configuration for any editor

You can also run `ai-snippet-mcp` directly to get just the MCP configuration JSON.

### Manual Container Management

Alternatively, build and run the containerized MCP server manually:

```bash
podman build -t ai-snippet-mcp .
podman run --rm -it -p 8000:8000 ai-snippet-mcp:latest
```

Once running, you can use the MCP server with the static configuration in `mcp-http.json`.
