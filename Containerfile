FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy Python project files
COPY mcp-server/pyproject.toml mcp-server/uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy only embedder.py first for embedding generation
COPY mcp-server/embedder.py ./

# Copy snippets directory for embedding generation
COPY snippets/ ./snippets/

# Generate embeddings during build
RUN uv run embedder.py ./snippets

# Copy rest of MCP server source code
COPY mcp-server/*.py ./

# Runtime stage
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy virtual environment and dependencies from builder
COPY --from=builder /app/.venv /app/.venv

# Copy MCP server source code
COPY --from=builder /app/*.py ./

# Copy snippets directory
COPY --from=builder /app/snippets ./snippets

# Copy generated embeddings
COPY --from=builder /root/.chroma /root/.chroma

# Set environment variables
ENV SNIPPET_DIRECTORY=/app/snippets
ENV PATH="/app/.venv/bin:$PATH"
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose port for HTTP transport
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["uv", "run", "main.py"]
