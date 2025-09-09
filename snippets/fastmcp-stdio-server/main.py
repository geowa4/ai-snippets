"""Example FastMCP server using stdio transport for MCP client communication."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.context import Context


@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[dict]:
    """Manage application lifecycle with context."""
    # Initialize any resources here
    context = {"initialized": True}
    yield context


mcp = FastMCP("Example MCP Server", lifespan=app_lifespan)


@mcp.tool()
def echo(message: str) -> str:
    """Echo back the provided message.

    Args:
        message: The message to echo back

    Returns:
        The same message that was provided

    """
    return f"Echo: {message}"


@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        The sum of a and b

    """
    return a + b


@mcp.tool()
def get_server_info(ctx: Context) -> str:
    """Get information about this MCP server.

    Returns:
        Server information including transport type and status

    """
    lifespan_context = ctx.request_context.lifespan_context
    return (
        "FastMCP Server Information:\n"
        f"- Transport: stdio\n"
        f"- Status: {'Active' if lifespan_context.get('initialized') else 'Inactive'}\n"
        f"- Available tools: echo, add_numbers, get_server_info"
    )


if __name__ == "__main__":
    # Use stdio transport for MCP client communication
    mcp.run(transport="stdio")
