#!/usr/bin/env python3

"""Run an MCP server to discover and load snippets."""

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.context import Context

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.WARNING),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Common response when no snippet is found
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
    logger.info("Initializing application lifespan: snippets_path=%s", snippets_path)
    summaries = {s.parent.name: s.read_text() for s in snippets_path.glob("**/SUMMARY.md")}
    logger.info("Loaded %d snippet summaries", len(summaries))
    yield AppContext(snippets_path=snippets_path, summaries=summaries)


mcp = FastMCP("AI Snippet Server", lifespan=app_lifespan, auth=None)


@mcp.tool()
def get_snippet_summaries(query: str, ctx: Context) -> str:  # noqa: D417
    """Return a list of all snippet names matching the query.

    You MUST call this function before `get_python_code_snippet` to obtain related snippets.

    Args:
      query: A brief query stating the goal to achieve while.

    Returns:
      Snippet names and their summaries including language, tools, and other technologies.

    """
    logger.info("get_snippet_summaries called with query=%s", query)
    logger.debug("Query terms: %s", query)
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
    logger.info("get_python_code_snippet called with name=%s", name)
    app_ctx: AppContext = ctx.request_context.lifespan_context
    code = app_ctx.snippets_path / name / "main.py"
    if not code.exists():
        logger.warning("Snippet %s not found at path: %s", name, code)
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
    logger.info("tell_me_more called with name=%s", name)
    app_ctx: AppContext = ctx.request_context.lifespan_context
    summary = app_ctx.summaries.get(name)
    readme = app_ctx.snippets_path / name / "README.md"
    if summary is None or not readme.exists:
        logger.warning("Summary and README for snippet %s not found", name)
        return NO_MATCHING_SNIPPET_TEMPLATE.format(name=name)
    try:
        readme_content = readme.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        logger.warning("Encoding error reading README for %s: %s", name, e)
        readme_content = readme.read_text(encoding="utf-8", errors="replace")
    return f"{summary}\n\n---\n\n{readme_content}"


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8000")
    # streamable-http transport serves MCP endpoint at /mcp/ by default
    mcp.run(transport="streamable-http", host=host, port=int(port))
