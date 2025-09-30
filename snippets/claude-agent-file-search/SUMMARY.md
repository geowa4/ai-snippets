# Claude Agent File Search

This project is built in Python and demonstrates how to use the Claude Agent SDK to perform intelligent, semantic file searches within a directory.
Claude Agent File Search serves as a practical example of leveraging Claude's reasoning capabilities to find files that best match user queries by analyzing file contents and understanding context, rather than relying on simple text matching.

## Technologies Used

- **Python 3.13+** - Core programming language
- **Claude Agent SDK** - Official Anthropic SDK for building AI agents with Claude
- **asyncio** - Asynchronous programming support for SDK interaction
- **pathlib** - Modern file path handling

## Key Features

- **Semantic file search** - Uses Claude's language understanding to match queries to files
- **Content analysis** - Reads and analyzes file contents, not just filenames
- **Tool-based exploration** - Claude autonomously uses Read and Glob tools to explore directories
- **Reasoning explanations** - Provides clear explanations for why a file matches the query
- **Simple CLI interface** - Easy-to-use command-line tool for quick searches
