# Claude Agent File Search

A Python utility that uses the Claude Agent SDK to intelligently find files in a directory that best match a user's query.

## Overview

This tool leverages Claude's reasoning capabilities to analyze file contents and determine which file best represents a user's query. Unlike simple text search, Claude can understand context, intent, and semantic meaning to find the most relevant file.

## Features

- Semantic file search using Claude's language understanding
- Analyzes file contents, not just filenames
- Provides reasoning for why a file matches the query
- Simple command-line interface
- Built on the Claude Agent SDK

## Requirements

- Python 3.13 or higher
- uv package manager
- Claude API key (set as `ANTHROPIC_API_KEY` environment variable)

## Installation

Navigate to the snippet directory and install dependencies:

```bash
cd snippets/claude-agent-file-search
uv sync
```

## Usage

Set your Claude API key:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Run the tool with a directory and query:

```bash
uv run main.py <directory> <query>
```

### Examples

Find authentication-related code:
```bash
uv run main.py ./src "authentication logic"
```

Find configuration files:
```bash
uv run main.py ./config "database connection settings"
```

Find documentation about a feature:
```bash
uv run main.py ./docs "how to deploy the application"
```

## How It Works

1. Claude receives your query and the target directory
2. Using the Glob tool, Claude lists files in the directory
3. Claude reads relevant files to understand their contents
4. Based on semantic analysis, Claude determines the best match
5. The tool outputs the file path and reasoning

## Development

Run code formatting and linting:
```bash
uv run ruff check
uv run ruff format
```

Run type checking:
```bash
uv run mypy main.py
```

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Claude API key (required)
- `ANTHROPIC_BASE_URL`: Optional custom API endpoint

## Limitations

- Performance depends on the number of files and their size
- Best suited for focused searches within specific directories
- Requires valid Claude API credentials
