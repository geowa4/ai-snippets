# MCP Server

An MCP (Model Context Protocol) server that provides access to AI code snippets through a standardized interface.

## Development

Install dependencies:

```bash
uv sync
```

Run the server directly:

```bash
uv run main.py
```

## Configuration

- `SNIPPET_DIRECTORY`: Path to snippets directory (default: `../snippets`)
- `LOG_LEVEL`: Logging level (default: `WARNING`)
- `HOST`: Server host (default: `127.0.0.1`)
- `PORT`: Server port (default: `8000`)

## Tools

The server provides two MCP tools:

- `list_snippets`: List all available code snippets
- `tell_me_more`: Get detailed information about a specific snippet