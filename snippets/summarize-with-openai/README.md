# Summarize with OpenAI

A Python utility that uses OpenAI models to generate executive summaries from incident reports.

## Overview

This tool processes Markdown incident reports stored in the `incident-reports` directory and produces concise executive summaries in the `incident-summaries` directory. It leverages the OpenAI API through the pydantic-ai library to generate summaries following specific format guidelines.

## Features

- Automatically processes all `.md` files in the `incident-reports` directory
- Creates executive summaries in 2-3 sentences with active voice
- Configurable to use different OpenAI models
- Follows established format guidelines for consistency

## Requirements

- Python 3.13 or higher
- uv package manager

## Installation

Clone the repository and install dependencies using uv:

```bash
git clone <repository-url>
cd summarize-with-openai
uv pip install -e .
```

## Usage

1. Add your incident report markdown files to the `incident-reports` directory
2. Set the OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   export OPENAI_BASE_URL="http://localhost:1234/v1"
   export MODEL_NAME="gemma-3-27b-it"
   ```
3. Run the main script:
   ```bash
   uv run main.py
   ```

Summaries will be generated in the `incident-summaries` directory with the same filenames as the original reports.

## Development

- Run code formatting and linting:
  ```bash
  uv run ruff check
  ```

- Run type checking:
  ```bash
  uv run mypy
  ```

## Prompt Configuration

The prompt template used for summarization can be modified in the `prompt` file.
