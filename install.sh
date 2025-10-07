#!/bin/bash

set -euo pipefail

# Check if path argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path> [port]"
    echo "  path: Directory where the ai-snippet-mcp script will be installed"
    echo "  port: Optional fixed port number (default: random port)"
    exit 1
fi

INSTALL_PATH="$1"
FIXED_PORT="${2:-}"

# Validate that the path exists and is a directory
if [ ! -d "$INSTALL_PATH" ]; then
    echo "Error: '$INSTALL_PATH' does not exist or is not a directory"
    exit 1
fi

# Get the absolute path to this git project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Create the ai-snippet-mcp script
SCRIPT_PATH="$INSTALL_PATH/ai-snippet-mcp"

cat > "$SCRIPT_PATH" << 'EOF'
#!/bin/bash

set -euo pipefail

PROJECT_ROOT="PROJECT_ROOT_PLACEHOLDER"
CONTAINER_NAME="ai-snippet-mcp"
FIXED_PORT="FIXED_PORT_PLACEHOLDER"

# Function to check if container is running
is_container_running() {
    podman ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$" 2>/dev/null
}

# Function to get container port
get_container_port() {
    podman port "$CONTAINER_NAME" 8000 2>/dev/null | cut -d: -f2 || echo ""
}

# Function to get image git commit
get_image_commit() {
    podman image inspect "$CONTAINER_NAME" --format '{{.Labels.git_commit}}' 2>/dev/null || echo ""
}

# Function to get current repo git commit
get_repo_commit() {
    git rev-parse HEAD
}

# Function to stop container if running
stop_container() {
    if is_container_running; then
        echo "Stopping existing container..." >&2
        podman stop "$CONTAINER_NAME" >/dev/null 2>&1
    fi
}

# Function to start container and get port
start_container() {
    echo "Starting container..." >&2
    local port_arg
    
    if [ -n "$FIXED_PORT" ]; then
        # Use fixed port
        port_arg="-p ${FIXED_PORT}:8000"
        echo "Using fixed port: $FIXED_PORT" >&2
    else
        # Use random port
        port_arg="-P"
        echo "Using random port assignment" >&2
    fi
    
    podman run --rm -d --name "$CONTAINER_NAME" $port_arg "$CONTAINER_NAME" >/dev/null
    
    # Wait a moment for container to start
    sleep 2
    
    # Verify container is running and get the assigned port
    if ! is_container_running; then
        echo "Error: Container failed to start" >&2
        exit 1
    fi
    
    local port
    if [ -n "$FIXED_PORT" ]; then
        port="$FIXED_PORT"
    else
        port=$(get_container_port)
        if [ -z "$port" ]; then
            echo "Error: Could not determine container port" >&2
            exit 1
        fi
    fi
    
    echo "$port"
}

# Change to project directory
cd "$PROJECT_ROOT"

# Check for local changes
if [ -n "$(git status --porcelain)" ]; then
    echo "Warning: Local changes detected, skipping git pull" >&2
else
    # Get current commit hash
    OLD_COMMIT=$(git rev-parse HEAD)

    # Pull latest changes
    echo "Pulling latest changes..." >&2
    git pull >/dev/null 2>&1

    # Get new commit hash after pull
    NEW_COMMIT=$(git rev-parse HEAD)
    if [ "$OLD_COMMIT" != "$NEW_COMMIT" ]; then
        echo "Repository updated from $OLD_COMMIT to $NEW_COMMIT" >&2
    fi
fi

# Check if image needs to be rebuilt by comparing repo commit with image label
REPO_COMMIT=$(get_repo_commit)
IMAGE_COMMIT=$(get_image_commit)

if [ -z "$IMAGE_COMMIT" ] || [ "$REPO_COMMIT" != "$IMAGE_COMMIT" ]; then
    CHANGES_DETECTED=true
    echo "Git commit mismatch - repo: $REPO_COMMIT, image: ${IMAGE_COMMIT:-none}" >&2
else
    CHANGES_DETECTED=false
fi

# Check if container is already running
if is_container_running; then
    if [ "$CHANGES_DETECTED" = "true" ]; then
        echo "Changes detected, rebuilding and restarting container..." >&2
        stop_container
        echo "Building image..." >&2
        podman build --label "git_commit=$REPO_COMMIT" -t "$CONTAINER_NAME" . >/dev/null
        PORT=$(start_container)
    else
        echo "Container already running, using existing instance..." >&2
        if [ -n "$FIXED_PORT" ]; then
            PORT="$FIXED_PORT"
        else
            PORT=$(get_container_port)
            if [ -z "$PORT" ]; then
                echo "Error: Could not determine existing container port" >&2
                exit 1
            fi
        fi
    fi
else
    # Container not running, need to start it
    # Check if image exists or if we need to build
    if ! podman image exists "$CONTAINER_NAME" || [ "$CHANGES_DETECTED" = "true" ]; then
        echo "Building image..." >&2
        podman build --label "git_commit=$REPO_COMMIT" -t "$CONTAINER_NAME" . >/dev/null
    fi
    PORT=$(start_container)
fi

# Output the MCP configuration JSON
cat << JSON
{
  "mcpServers": {
    "ai-snippets": {
      "type": "http", 
      "url": "http://localhost:${PORT}/mcp",
      "auth": {}
    }
  }
}
JSON
EOF

# Replace the placeholders with actual values
sed -i.bak "s|PROJECT_ROOT_PLACEHOLDER|$PROJECT_ROOT|g" "$SCRIPT_PATH" && rm "$SCRIPT_PATH.bak"
sed -i.bak "s|FIXED_PORT_PLACEHOLDER|$FIXED_PORT|g" "$SCRIPT_PATH" && rm "$SCRIPT_PATH.bak"

# Make the script executable
chmod +x "$SCRIPT_PATH"

echo "ai-snippet-mcp script installed to: $SCRIPT_PATH"
if [ -n "$FIXED_PORT" ]; then
    echo "Configured to use fixed port: $FIXED_PORT"
else
    echo "Configured to use random port assignment"
fi
echo ""
echo "Usage:"
echo "  claude --mcp-config \"\$(ai-snippet-mcp)\""