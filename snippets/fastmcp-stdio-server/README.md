# FastMCP Stdio Server

A simple FastMCP server implementation using stdio transport for Model Context Protocol (MCP) client communication. This snippet demonstrates how to create an MCP server that can be integrated with MCP-compatible clients like Claude Desktop.

---

## 🎯 Purpose

This project demonstrates how to build an MCP server that:

1. Uses stdio transport for client communication
2. Implements multiple tools with different parameter types
3. Provides proper logging and lifecycle management
4. Serves as a foundation for building custom MCP servers

---

## 🧱 Technologies Used

- **FastMCP** - Python framework for building MCP servers
- **stdio transport** - Standard input/output communication protocol
- **Python 3.8+** - Required runtime
- **asyncio** - For asynchronous operations and lifecycle management

---

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
pip install fastmcp
```

Or using uv:

```bash
uv add fastmcp
```

### 2. Make the Script Executable (Optional)

```bash
chmod +x main.py
```

---

## 🚀 Usage

### Running as Standalone Server

You can run the server directly for testing:

```bash
python main.py
```

However, MCP servers are typically not run standalone but rather integrated with MCP clients.

### Integration with MCP Clients

#### Claude Desktop Integration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fastmcp-stdio-server": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/fastmcp-stdio-server",
        "run", "main.py"
      ],
    }
  }
}
```

#### Generic MCP Client Integration

The server can be integrated with any MCP-compatible client that supports stdio transport. The client will communicate with the server through standard input/output streams.

---

## 🔧 Available Tools

The server provides three example tools:

### 1. `echo`

- **Purpose**: Echo back any message
- **Parameters**: `message` (string)
- **Returns**: The same message with "Echo: " prefix

### 2. `add_numbers`

- **Purpose**: Add two numbers together
- **Parameters**: `a` (float), `b` (float)
- **Returns**: Sum of the two numbers

### 3. `get_server_info`

- **Purpose**: Get information about the server
- **Parameters**: None
- **Returns**: Server status and configuration details

---

## 📝 Environment Variables

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR). Default: WARNING

---

## 🏗 Architecture

The server follows these key patterns:

### Lifecycle Management

```python
@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[dict]:
    # Initialize resources
    yield context
    # Cleanup resources
```

### Tool Definition

```python
@mcp.tool()
def tool_name(param: type) -> return_type:
    """Tool description for MCP clients."""
    # Tool implementation
```

### Context Access

```python
@mcp.tool()
def tool_with_context(ctx: Context) -> str:
    # Access lifespan context and request information
    lifespan_context = ctx.request_context.lifespan_context
```

---

## 🔍 Key Differences from HTTP Transport

This stdio implementation differs from HTTP-based MCP servers:

- **Communication**: Uses stdin/stdout instead of HTTP requests
- **Integration**: Directly embedded in client processes
- **Performance**: Lower latency due to direct process communication
- **Deployment**: No need for separate server hosting

---

## 📁 Project Structure

```bash
fastmcp-stdio-server/
├── main.py             # Main MCP server implementation
├── README.md           # This documentation
└── SUMMARY.md          # Short summary for AI snippet selection
```

---

## 🚦 Advanced Usage

### Custom Tool Development

Add new tools by decorating functions with `@mcp.tool()`:

```python
@mcp.tool()
def custom_tool(param1: str, param2: int) -> dict:
    """Description of what this tool does."""
    return {"result": f"Processed {param1} with {param2}"}
```

### Enhanced Logging

Configure detailed logging for debugging:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("mcp_server.log"),
        logging.StreamHandler()
    ]
)
```

### Error Handling

Implement robust error handling in tools:

```python
@mcp.tool()
def safe_tool(data: str) -> str:
    try:
        # Tool logic here
        return process_data(data)
    except Exception as e:
        logger.error("Tool failed: %s", e)
        return f"Error: {str(e)}"
```

### Resource Management

Use the lifespan context for managing resources:

```python
@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[dict]:
    # Initialize database connection, load models, etc.
    db = await initialize_database()
    cache = await initialize_cache()
    
    yield {
        "database": db,
        "cache": cache
    }
    
    # Cleanup
    await db.close()
    await cache.close()
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Client Connection Failed**
   - Ensure the script path in client config is absolute
   - Check that Python can execute the script
   - Verify FastMCP is installed

2. **Tools Not Appearing**
   - Check that functions are properly decorated with `@mcp.tool()`
   - Ensure the server starts without errors
   - Verify client configuration syntax

3. **Logging Issues**
   - MCP servers should log to stderr, not stdout
   - stdout is reserved for MCP protocol communication

### Debug Mode

Run with debug logging:

```bash
LOG_LEVEL=DEBUG python main.py
```

---

## 📚 References

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Claude Desktop MCP Integration](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
