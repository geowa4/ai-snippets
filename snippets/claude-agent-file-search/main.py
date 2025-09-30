"""Find the best file match for a user query using Claude Agent SDK."""

import asyncio
from pathlib import Path

import click
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)


async def find_best_file(directory: Path, query: str) -> None:
    """Use Claude to find the file that best matches the query."""
    if not directory.exists() or not directory.is_dir():
        msg = f"{directory} does not exist or is not a directory."
        raise click.ClickException(msg)

    system_prompt = f"""You are a file search assistant.
The user will provide a query, and you need to find the file in {directory}
that best matches their query.

You have access to Read and Glob tools to explore the directory and read
file contents.

Your task:
1. Use Glob to list files in the directory
2. Read relevant files to understand their contents
3. Determine which file best matches the user's query
4. Respond with ONLY the relative path to the best matching file,
   followed by a brief explanation of why it matches

Format your response as:
FILE: <relative-path-to-file>
REASON: <brief explanation>"""

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=["Read", "Glob"],
        cwd=str(directory.resolve()),
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(query)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        click.echo(block.text, nl=False)


@click.command()
@click.argument("query")
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=lambda: Path(__file__).parent / "test-files",
    help="Directory to search (defaults to test-files/)",
)
def main(query: str, directory: Path) -> None:
    """Find the file that best matches QUERY in the specified directory.

    By default, searches in the test-files/ directory.

    Examples:
      uv run main.py "authentication logic"

      uv run main.py "database configuration" -d /path/to/search

    """
    asyncio.run(find_best_file(directory, query))


if __name__ == "__main__":
    main()
