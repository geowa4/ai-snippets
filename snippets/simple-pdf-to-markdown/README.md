# Simple PDF to Markdown Converter

A Python utility that converts PDF documents to Markdown format using the Docling library.
This tool provides a straightforward way to extract text content from PDFs and convert it into readable Markdown.

## Purpose

This project demonstrates a simple approach to converting PDF files to Markdown format.
It's particularly useful for:

- Extracting text content from PDF documents
- Converting PDF documentation to Markdown
- Migrating PDF content to markdown-based systems
- Creating text-based versions of PDF files for better searchability

## Technologies Used

- **Python 3.13+** - Programming language
- **Docling** - PDF to Markdown conversion library
- **uv** - Fast Python package manager

### Development Tools

- **mypy** - Static type checking
- **ruff** - Linting and code formatting
- **python-lsp-server** - Language server protocol for IDE support
- **watchdog** - File system monitoring

## Installation

1. Make sure you have Python 3.13 or higher installed:

   ```bash
   python --version
   ```

2. Install uv if you haven't already:

   ```bash
   pip install uv
   ```

3. Clone the repository and navigate to the project directory:

   ```bash
   cd simple-pdf-to-markdown
   ```

4. Install dependencies using uv:

   ```bash
   uv sync
   ```

## Usage

To convert the included sample PDF to Markdown:

```bash
uv run main.py
```

To convert your own PDF file:

1. Replace `sample.pdf` with your PDF file or modify the code in `main.py` to point to your file:

   ```python
   pdf = Path("your-file.pdf")
   ```

2. Run the converter:

   ```bash
   uv run main.py
   ```

The Markdown content will be printed to the console. You can redirect it to a file if needed:

```bash
uv run main.py > output.md
```

## Project Structure

```
simple-pdf-to-markdown/
├── .python-version     # Python version specification
├── README.md           # Project documentation
├── main.py             # Main script for PDF to Markdown conversion
├── pyproject.toml      # Project configuration and dependencies
├── sample.pdf          # Sample PDF file for testing
└── uv.lock             # Locked dependency versions
```
