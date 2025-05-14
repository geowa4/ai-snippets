#!/usr/bin/env python3

"""Run an MCP server to discover and load snippets."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP

NO_MATCHING_SNIPPET_TEMPLATE = (
    "No snippet matched '{name}'. "
    "Call `get_snippet_summaries` to get a list of snippets matching your query."
)


@dataclass
class AppContext:
    """Stores context needed manage snippets."""

    snippets_path: Path
    summaries: dict[str, str]


@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    snippets_path = Path(
        os.getenv("SNIPPET_DIRECTORY", Path(__file__).parent.parent / "snippets"),
    )
    summaries = {s.parent.name: s.read_text() for s in snippets_path.glob("**/SUMMARY.md")}
    yield AppContext(snippets_path=snippets_path, summaries=summaries)


mcp = FastMCP("AI Snippet Server", lifespan=app_lifespan)


@mcp.tool()
def get_snippet_summaries(query: str, ctx: Context) -> str:  # noqa: D417
    """Return a list of all snippet names matching the query.

    You MUST call this function before `get_python_code_snippet` to obtain related snippets.

    Args:
      query: A brief query stating the goal to achieve while.

    Returns:
      Snippet names and their summaries including language, tools, and other technologies.

    """
    print(f"TODO: use query '{query}'")
    return "\n\n".join(
        [
            f"<snippet>\nSnippet Name: {name}\n\n---\n\n{summary}\n</snippet>"
            for name, summary in ctx.request_context.lifespan_context.summaries.items()
        ],
    )


@mcp.tool()
def get_python_code_snippet(name: str, ctx: Context) -> str:  # noqa: D417
    """Get the Python snippet by name.

    You MUST call `get_snippet_summaries` first to obtain the exact snippet name.

    Args:
      name: The name of the snippet.

    Returns:
      The Python code snippet.

    """
    app_ctx: AppContext = ctx.request_context.lifespan_context
    code = app_ctx.snippets_path / name / "main.py"
    if not code.exists():
        return NO_MATCHING_SNIPPET_TEMPLATE.format(name=name)
    return code.read_text()


@mcp.tool()
def tell_me_more(name: str, ctx: Context) -> str:  # noqa: D417
    """Tell more about the named snippet by returning its summary and README.

    Optional tool to get more information about the snippet.

    Args:
      name: The name of the snippet.

    Returns:
      The summary and README of the snippet.

    """
    return ctx.request_context.lifespan_context.summaries.get(
        name,
        NO_MATCHING_SNIPPET_TEMPLATE.format(name=name),
    )
