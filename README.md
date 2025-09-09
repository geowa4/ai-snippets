# ai-snippets

A place to store code and other snippets I've used in my AI projects.

No single snippet is allowed to be complex or else it is not a snippet.
Assume all code was created with assistance from some LLM or coding agent.

## MCP Server

This repository includes an MCP (Model Context Protocol) server that provides access to all snippets through a standardized interface.

### Running with Container

Build and run the containerized MCP server:

```bash
podman build -t ai-snippet-mcp .
podman run --rm -it -p 8000:8000 ai-snippet-mcp:latest
```

Once running, you can use the MCP server with the configuration in `mcp-http.json`.

```bash
claude --mcp-config /path/to/ai-snippets/mcp-http.json
```
