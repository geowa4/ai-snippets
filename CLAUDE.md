# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a collection of AI code snippets, where each snippet is a self-contained example. The repository follows this architecture:

- `snippets/`: Individual snippet directories, each with their own `pyproject.toml`, `main.py`, and README
- `mcp-server/`: MCP (Model Context Protocol) server that provides access to snippets via standardized interface
- Each snippet is designed to be simple and focused on a single AI/ML concept

## Common Development Commands

### Creating a New Snippet

```bash
cd snippets
uv init <name-of-snippet>                           # Create new snippet directory
cd <name-of-snippet>
uv add --dev mypy python-lsp-server ruff watchdog   # Add standard dev dependencies
```

### Individual Snippet Development

```bash
cd snippets/<snippet-name>
uv sync                 # Install dependencies for the snippet
uv run main.py          # Run the snippet
```

### MCP Server Development

```bash
cd mcp-server
uv sync                 # Install dependencies
uv run main.py          # Run MCP server directly
```

### Code Quality Tools

All Python projects use these tools (available in dev dependencies):

```bash
uv run ruff check       # Lint with ruff
uv run ruff format      # Format code with ruff
```

### Container Development

```bash
podman build -t ai-snippet-mcp .                   # Build container using Containerfile
podman run --rm -it -p 8000:8000 ai-snippet-mcp    # Run container
```

## Key Technologies

- **Python 3.13+**: All snippets require Python 3.13 or later
- **uv**: Used for dependency management across all projects
- **Ruff**: Linting and formatting with strict rule set (`select = ["ALL"]`)

### AI/ML Frameworks

- **LangChain**: Core framework with extensions (community, ollama, qdrant, chroma)
- **Sentence Transformers**: Text embedding models
- **OpenAI**: OpenAI API integration
- **Pydantic AI**: AI framework with Pydantic integration
- **Pydantic Graph**: Graph-based AI workflows

### Vector Databases

- **ChromaDB**: Vector database for embeddings
- **Qdrant**: Alternative vector database

### MCP and Document Processing

- **FastMCP**: MCP server implementation framework
- **Docling**: PDF to markdown conversion
- **HTTPX**: Modern HTTP client
- **python-dotenv**: Environment variable management

## MCP Server Configuration

The MCP server can be used with Claude via the included `mcp-http.json` configuration file. Server runs on `localhost:8000` by default and provides tools to list and query snippets.

## Environment Variables

MCP Server supports:

- `SNIPPET_DIRECTORY`: Path to snippets (default: `../snippets`)
- `LOG_LEVEL`: Logging level (default: `WARNING`)
- `HOST`: Server host (default: `127.0.0.1`)
- `PORT`: Server port (default: `8000`)
