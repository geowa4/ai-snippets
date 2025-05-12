#!/usr/bin/env python3

"""Run an MCP server to discover and load snippets."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP


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
    summaries = {
        s.parent.name: s.read_text() for s in snippets_path.glob("**/SUMMARY.md")
    }
    yield AppContext(snippets_path=snippets_path, summaries=summaries)


mcp = FastMCP("AI Snippet Server", lifespan=app_lifespan)


@mcp.tool()
def get_snippet_summaries(ctx: Context) -> list[str]:
    """Return a list of all snippet names."""
    return "\n\n".join(
        [
            f"<snippet>\nSnippet Name: {name}\n\n---\n\n{summary}\n</snippet>"
            for name, summary in ctx.request_context.lifespan_context.summaries.items()
        ],
    )


@mcp.tool()
def get_python_code_snippet(name: str, ctx: Context) -> int:
    """Get the Python snippet by name."""
    code = ctx.request_context.lifespan_context.snippets_path / name / "main.py"
    return code.read_text()


# Add a dynamic greeting resource
@mcp.tool()
def get_summary(name: str, ctx: Context) -> str:
    """Get the summary by name."""
    return ctx.request_context.lifespan_context.summaries.get(
        name,
        f"No summary matched {name}",
    )
