# Sentence Transformers Demo

A demonstration project showcasing the use of the `sentence-transformers` Python package for encoding text into embeddings and calculating semantic similarity.

## Overview

This project demonstrates how to:

- Load and initialize a sentence transformer model
- Encode queries and documents into embeddings
- Calculate semantic similarity between queries and documents

The code supports both HuggingFace model names (which will be auto-downloaded) and local model paths.

## Prerequisites

- Python 3.13 or higher
- `uv` package manager
- Git LFS (if downloading models from HuggingFace)

### Installing uv

If you don't have `uv` installed, you can install it using:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS with Homebrew:

```bash
brew install uv
```

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd sentence-transformer-basics
```

2. Install dependencies using `uv`:

```bash
uv sync
```

This will create a virtual environment and install all required dependencies defined in `pyproject.toml`.

## Usage

### Running the Application

Run the demo with a HuggingFace model name (will auto-download):

```bash
EMBEDDING_MODEL_OR_PATH="sentence-transformers/all-MiniLM-L6-v2" uv run main.py
```

Or with a local model path:

```bash
EMBEDDING_MODEL_OR_PATH="/path/to/your/local/model" uv run main.py
```

### Example Output

The demo will:

1. Display model details (prompts, embedding dimension, similarity function)
2. Encode sample queries about China's capital and gravity
3. Encode related documents
4. Calculate and display similarity scores between queries and documents

### Downloading Models Locally

For large models or to avoid repeated downloads, you can download models locally first:

1. Install Git LFS:

```bash
git lfs install
```

2. Clone the model repository:

```bash
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
```

3. Use the local path when running:

```bash
EMBEDDING_MODEL_OR_PATH="./all-MiniLM-L6-v2" uv run main.py
```

## Development

### Code Formatting

Format the code using Ruff:

```bash
uv run ruff format
```

### Linting

Lint the code to check for style issues:

```bash
uv run ruff check
```

To automatically fix linting issues:

```bash
uv run ruff check --fix
```

### Type Checking

Run type checking with mypy:

```bash
uv run mypy .
```

## Project Structure

- `main.py` - Main demonstration script showing sentence-transformers usage
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Locked dependency versions for reproducible builds

## Dependencies

- `sentence-transformers>=5.0.0` - The main library for encoding text into embeddings
- Development dependencies include `mypy`, `ruff`, and `python-lsp-server`

## How It Works

The demo:

1. Initializes a SentenceTransformer model using the path/name from the environment variable
2. Encodes sample queries using `model.encode_query()`
3. Encodes sample documents using `model.encode_document()`
4. Calculates similarity scores between queries and documents using `model.similarity()`
5. Displays the similarity matrix showing how well each query matches each document

This is useful for applications like semantic search, document retrieval, and question-answering systems.
