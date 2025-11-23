# MCP Code Examples

This document provides practical, working code examples for implementing MCP servers and clients in Python and TypeScript.

## Table of Contents

1. [Python Server Examples](#python-server-examples)
2. [TypeScript Server Examples](#typescript-server-examples)
3. [Python Client Examples](#python-client-examples)
4. [TypeScript Client Examples](#typescript-client-examples)
5. [Configuration Examples](#configuration-examples)
6. [Real-World Integration Examples](#real-world-integration-examples)

## Python Server Examples

### Example 1: Simple Calculator Server

```python
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("calculator-server", json_response=True)

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide a by b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Run with STDIO transport (for local use)
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Example 2: Database Server

```python
from mcp.server.fastmcp import FastMCP
import sqlite3
from typing import List, Dict, Any
import json

mcp = FastMCP("database-server")

# Database connection
DB_PATH = "data.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def query_database(sql: str) -> List[Dict[str, Any]]:
    """
    Execute a read-only SQL query.

    Args:
        sql: SELECT query to execute

    Returns:
        List of dictionaries representing rows

    Raises:
        ValueError: If query is not a SELECT statement
    """
    # Safety: only allow SELECT
    if not sql.strip().upper().startswith('SELECT'):
        raise ValueError("Only SELECT queries are allowed")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        return results
    finally:
        conn.close()

@mcp.tool()
def get_table_schema(table_name: str) -> Dict[str, Any]:
    """
    Get schema information for a table.

    Args:
        table_name: Name of the table

    Returns:
        Dictionary with table schema details
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        return {
            "table": table_name,
            "columns": [
                {
                    "name": col[1],
                    "type": col[2],
                    "not_null": bool(col[3]),
                    "primary_key": bool(col[5])
                }
                for col in columns
            ]
        }
    finally:
        conn.close()

@mcp.resource("schema://tables")
def list_tables() -> str:
    """List all tables in the database"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        return json.dumps({"tables": tables}, indent=2)
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Example 3: File System Server

```python
from mcp.server.fastmcp import FastMCP
from pathlib import Path
from typing import List, Optional
import os
import mimetypes

mcp = FastMCP("filesystem-server")

# Base directory for file operations
BASE_DIR = Path("/workspace")

def safe_path(path: str) -> Path:
    """
    Ensure path is within BASE_DIR.

    Args:
        path: Requested file path

    Returns:
        Resolved absolute path

    Raises:
        ValueError: If path escapes BASE_DIR
    """
    requested = (BASE_DIR / path).resolve()
    if not str(requested).startswith(str(BASE_DIR)):
        raise ValueError("Path outside allowed directory")
    return requested

@mcp.tool()
def read_file(path: str) -> str:
    """
    Read contents of a file.

    Args:
        path: Relative path to file

    Returns:
        File contents as string
    """
    file_path = safe_path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")

    return file_path.read_text()

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    Write content to a file.

    Args:
        path: Relative path to file
        content: Content to write

    Returns:
        Success message
    """
    file_path = safe_path(path)

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content)

    return f"Successfully wrote {len(content)} characters to {path}"

@mcp.tool()
def list_directory(path: str = ".") -> List[Dict[str, Any]]:
    """
    List contents of a directory.

    Args:
        path: Relative path to directory (default: current)

    Returns:
        List of files and directories with metadata
    """
    dir_path = safe_path(path)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not dir_path.is_dir():
        raise ValueError(f"Not a directory: {path}")

    items = []
    for item in dir_path.iterdir():
        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "size": item.stat().st_size if item.is_file() else None,
            "modified": item.stat().st_mtime
        })

    return items

@mcp.resource("file://{path}")
def get_file_resource(path: str) -> dict:
    """
    Expose file as MCP resource.

    Args:
        path: Relative file path

    Returns:
        Resource dictionary with file metadata and content
    """
    file_path = safe_path(path)

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    mime_type, _ = mimetypes.guess_type(str(file_path))

    return {
        "uri": f"file://{path}",
        "name": file_path.name,
        "mimeType": mime_type or "application/octet-stream",
        "text": file_path.read_text() if mime_type and mime_type.startswith('text') else None
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Example 4: API Integration Server

```python
from mcp.server.fastmcp import FastMCP
import aiohttp
import os
from typing import Dict, Any, Optional

mcp = FastMCP("github-api-server")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"

async def github_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None
) -> Dict[str, Any]:
    """Make authenticated request to GitHub API"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            f"{GITHUB_API}{endpoint}",
            headers=headers,
            json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

@mcp.tool()
async def create_issue(
    repo: str,
    title: str,
    body: str,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a GitHub issue.

    Args:
        repo: Repository in format "owner/repo"
        title: Issue title
        body: Issue description
        labels: Optional list of label names

    Returns:
        Created issue details
    """
    data = {
        "title": title,
        "body": body
    }

    if labels:
        data["labels"] = labels

    result = await github_request(
        "POST",
        f"/repos/{repo}/issues",
        data=data
    )

    return {
        "number": result["number"],
        "url": result["html_url"],
        "state": result["state"]
    }

@mcp.tool()
async def list_issues(
    repo: str,
    state: str = "open",
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    List issues for a repository.

    Args:
        repo: Repository in format "owner/repo"
        state: Issue state (open, closed, all)
        limit: Maximum number of issues to return

    Returns:
        List of issues
    """
    endpoint = f"/repos/{repo}/issues?state={state}&per_page={limit}"
    issues = await github_request("GET", endpoint)

    return [
        {
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "url": issue["html_url"],
            "labels": [label["name"] for label in issue["labels"]]
        }
        for issue in issues
    ]

@mcp.resource("repo://{owner}/{repo}")
async def get_repository_info(owner: str, repo: str) -> str:
    """Get repository information as a resource"""
    data = await github_request("GET", f"/repos/{owner}/{repo}")

    return json.dumps({
        "name": data["name"],
        "description": data["description"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data["language"],
        "url": data["html_url"]
    }, indent=2)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=3000)
```

## TypeScript Server Examples

### Example 1: Weather Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create server
const server = new Server(
  {
    name: "weather-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Define tool
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a city",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "City name (e.g., 'San Francisco, CA')",
            },
            units: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              description: "Temperature units",
              default: "celsius",
            },
          },
          required: ["city"],
        },
      },
      {
        name: "get_forecast",
        description: "Get weather forecast for next 5 days",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "City name",
            },
            days: {
              type: "number",
              description: "Number of days (1-5)",
              minimum: 1,
              maximum: 5,
              default: 3,
            },
          },
          required: ["city"],
        },
      },
    ],
  };
});

// Implement tool execution
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_weather") {
    const { city, units = "celsius" } = args as {
      city: string;
      units?: string;
    };

    // Call weather API (simplified)
    const weatherData = await fetchWeatherData(city);

    const temp =
      units === "fahrenheit"
        ? celsiusToFahrenheit(weatherData.temperature)
        : weatherData.temperature;

    return {
      content: [
        {
          type: "text",
          text: `Weather in ${city}: ${weatherData.condition}, ${temp}°${
            units === "fahrenheit" ? "F" : "C"
          }`,
        },
      ],
    };
  }

  if (name === "get_forecast") {
    const { city, days = 3 } = args as { city: string; days?: number };

    const forecast = await fetchForecast(city, days);

    const forecastText = forecast
      .map((day: any) => `${day.date}: ${day.condition}, ${day.temp}°C`)
      .join("\n");

    return {
      content: [
        {
          type: "text",
          text: `${days}-day forecast for ${city}:\n${forecastText}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Helper functions
async function fetchWeatherData(city: string) {
  // Simplified - replace with actual API call
  return {
    temperature: 22,
    condition: "Sunny",
    humidity: 60,
    windSpeed: 15,
  };
}

async function fetchForecast(city: string, days: number) {
  // Simplified - replace with actual API call
  return Array.from({ length: days }, (_, i) => ({
    date: new Date(Date.now() + i * 86400000).toLocaleDateString(),
    temp: 20 + Math.random() * 10,
    condition: ["Sunny", "Cloudy", "Rainy"][Math.floor(Math.random() * 3)],
  }));
}

function celsiusToFahrenheit(celsius: number): number {
  return (celsius * 9) / 5 + 32;
}

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Example 2: Task Management Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  createdAt: Date;
}

// In-memory task storage
const tasks: Map<string, Task> = new Map();
let taskCounter = 1;

const server = new Server(
  {
    name: "task-manager",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Register tools
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "create_task",
        description: "Create a new task",
        inputSchema: {
          type: "object",
          properties: {
            title: { type: "string", description: "Task title" },
            description: { type: "string", description: "Task description" },
            priority: {
              type: "string",
              enum: ["low", "medium", "high"],
              description: "Task priority",
              default: "medium",
            },
          },
          required: ["title"],
        },
      },
      {
        name: "update_task",
        description: "Update an existing task",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Task ID" },
            status: {
              type: "string",
              enum: ["todo", "in_progress", "done"],
              description: "New status",
            },
            title: { type: "string", description: "New title" },
            description: { type: "string", description: "New description" },
            priority: {
              type: "string",
              enum: ["low", "medium", "high"],
              description: "New priority",
            },
          },
          required: ["id"],
        },
      },
      {
        name: "list_tasks",
        description: "List all tasks, optionally filtered by status",
        inputSchema: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["todo", "in_progress", "done", "all"],
              description: "Filter by status",
              default: "all",
            },
          },
        },
      },
      {
        name: "delete_task",
        description: "Delete a task",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Task ID" },
          },
          required: ["id"],
        },
      },
    ],
  };
});

// Implement tool handlers
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "create_task": {
      const { title, description = "", priority = "medium" } = args as any;

      const task: Task = {
        id: `task-${taskCounter++}`,
        title,
        description,
        status: "todo",
        priority,
        createdAt: new Date(),
      };

      tasks.set(task.id, task);

      return {
        content: [
          {
            type: "text",
            text: `Created task ${task.id}: ${task.title}`,
          },
        ],
      };
    }

    case "update_task": {
      const { id, ...updates } = args as any;

      const task = tasks.get(id);
      if (!task) {
        return {
          content: [{ type: "text", text: `Task ${id} not found` }],
          isError: true,
        };
      }

      Object.assign(task, updates);

      return {
        content: [
          {
            type: "text",
            text: `Updated task ${id}`,
          },
        ],
      };
    }

    case "list_tasks": {
      const { status = "all" } = args as any;

      let filteredTasks = Array.from(tasks.values());

      if (status !== "all") {
        filteredTasks = filteredTasks.filter((t) => t.status === status);
      }

      const taskList = filteredTasks
        .map(
          (t) =>
            `[${t.id}] ${t.title} - ${t.status} (${t.priority})\n  ${t.description}`
        )
        .join("\n\n");

      return {
        content: [
          {
            type: "text",
            text: taskList || "No tasks found",
          },
        ],
      };
    }

    case "delete_task": {
      const { id } = args as any;

      if (!tasks.has(id)) {
        return {
          content: [{ type: "text", text: `Task ${id} not found` }],
          isError: true,
        };
      }

      tasks.delete(id);

      return {
        content: [
          {
            type: "text",
            text: `Deleted task ${id}`,
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Expose tasks as resources
server.setRequestHandler("resources/list", async () => {
  return {
    resources: Array.from(tasks.values()).map((task) => ({
      uri: `task://${task.id}`,
      name: task.title,
      description: `Task: ${task.status}`,
      mimeType: "application/json",
    })),
  };
});

server.setRequestHandler("resources/read", async (request) => {
  const { uri } = request.params;

  const taskId = uri.replace("task://", "");
  const task = tasks.get(taskId);

  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  return {
    contents: [
      {
        uri,
        mimeType: "application/json",
        text: JSON.stringify(task, null, 2),
      },
    ],
  };
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Python Client Examples

### Example: Basic Client Usage

```python
from mcp.client import Client
from mcp.client.stdio import StdioServerConnection
import asyncio

async def main():
    # Connect to MCP server
    async with StdioServerConnection(
        command="python",
        args=["calculator_server.py"]
    ) as connection:
        # Create client
        client = Client(connection)

        # Initialize connection
        await client.initialize()

        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")

        # Call a tool
        result = await client.call_tool(
            "add",
            arguments={"a": 5, "b": 3}
        )
        print(f"\n5 + 3 = {result.content[0].text}")

        # Call another tool
        result = await client.call_tool(
            "multiply",
            arguments={"a": 7, "b": 6}
        )
        print(f"7 × 6 = {result.content[0].text}")

        # List resources
        resources = await client.list_resources()
        print("\nAvailable resources:")
        for resource in resources.resources:
            print(f"  - {resource.uri}: {resource.name}")

        # Read a resource
        if resources.resources:
            resource_data = await client.read_resource(
                uri=resources.resources[0].uri
            )
            print(f"\nResource content:")
            print(resource_data.contents[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example: Client with Error Handling

```python
from mcp.client import Client
from mcp.client.stdio import StdioServerConnection
from mcp.types import McpError
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def safe_tool_call(client: Client, tool_name: str, **kwargs):
    """Execute tool with error handling"""
    try:
        result = await client.call_tool(tool_name, arguments=kwargs)
        return result.content[0].text
    except McpError as e:
        logger.error(f"MCP error calling {tool_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error calling {tool_name}: {e}")
        return None

async def main():
    try:
        async with StdioServerConnection(
            command="python",
            args=["database_server.py"]
        ) as connection:
            client = Client(connection)
            await client.initialize()

            # Safe tool calls
            result = await safe_tool_call(
                client,
                "query_database",
                sql="SELECT * FROM users LIMIT 5"
            )

            if result:
                print(f"Query result: {result}")

            # Handle invalid input
            result = await safe_tool_call(
                client,
                "query_database",
                sql="DELETE FROM users"  # Will be rejected
            )

            if result is None:
                print("Operation rejected as expected")

    except Exception as e:
        logger.error(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## TypeScript Client Examples

### Example: Client with HTTP Transport

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { HttpClientTransport } from "@modelcontextprotocol/sdk/client/http.js";

async function main() {
  // Create HTTP transport
  const transport = new HttpClientTransport({
    url: "https://api.example.com/mcp",
    headers: {
      Authorization: `Bearer ${process.env.API_KEY}`,
    },
  });

  // Create client
  const client = new Client(
    {
      name: "my-client",
      version: "1.0.0",
    },
    {
      capabilities: {},
    }
  );

  // Connect
  await client.connect(transport);

  // List and call tools
  const tools = await client.listTools();
  console.log("Available tools:", tools);

  const result = await client.callTool({
    name: "get_weather",
    arguments: {
      city: "San Francisco, CA",
      units: "fahrenheit",
    },
  });

  console.log("Weather:", result.content[0].text);

  // List and read resources
  const resources = await client.listResources();
  console.log("Available resources:", resources);

  if (resources.resources.length > 0) {
    const resource = await client.readResource({
      uri: resources.resources[0].uri,
    });
    console.log("Resource content:", resource.contents[0].text);
  }
}

main().catch(console.error);
```

## Configuration Examples

### Claude Desktop Configuration

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
`%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents"
      ]
    },
    "database": {
      "command": "python",
      "args": ["-m", "mcp_server_sqlite", "--db", "data.db"],
      "env": {
        "DB_READONLY": "true"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "custom-api": {
      "command": "python",
      "args": ["my_server.py"]
    }
  }
}
```

### VS Code Configuration

`.vscode/mcp.json`

```json
{
  "servers": {
    "project-tools": {
      "command": "node",
      "args": ["./mcp-server.js"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Real-World Integration Examples

### Example: Complete CRM Integration

```python
from mcp.server.fastmcp import FastMCP
import aiohttp
import os
from typing import List, Dict, Optional

mcp = FastMCP("crm-integration")

CRM_API_URL = os.getenv("CRM_API_URL")
CRM_API_KEY = os.getenv("CRM_API_KEY")

async def crm_request(method: str, endpoint: str, data: Optional[Dict] = None):
    """Make authenticated CRM API request"""
    headers = {
        "Authorization": f"Bearer {CRM_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            f"{CRM_API_URL}{endpoint}",
            headers=headers,
            json=data
        ) as response:
            response.raise_for_status()
            return await response.json()

@mcp.tool()
async def search_customers(query: str, limit: int = 10) -> List[Dict]:
    """Search for customers by name or email"""
    result = await crm_request(
        "GET",
        f"/customers/search?q={query}&limit={limit}"
    )
    return result["customers"]

@mcp.tool()
async def get_customer_orders(customer_id: str) -> List[Dict]:
    """Get all orders for a customer"""
    result = await crm_request("GET", f"/customers/{customer_id}/orders")
    return result["orders"]

@mcp.tool()
async def create_support_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "medium"
) -> Dict:
    """Create a support ticket for a customer"""
    data = {
        "customer_id": customer_id,
        "subject": subject,
        "description": description,
        "priority": priority
    }

    result = await crm_request("POST", "/tickets", data=data)
    return result

@mcp.resource("customer://{customer_id}")
async def get_customer_profile(customer_id: str) -> str:
    """Get full customer profile"""
    customer = await crm_request("GET", f"/customers/{customer_id}")

    return json.dumps({
        "id": customer["id"],
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "lifetime_value": customer["lifetime_value"],
        "total_orders": customer["total_orders"],
        "status": customer["status"]
    }, indent=2)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=3001)
```

These examples demonstrate the core patterns for building MCP servers and clients. The key principles are:

1. **Clear interfaces**: Well-defined tools with comprehensive documentation
2. **Error handling**: Robust validation and error messages
3. **Security**: Input validation, authentication, safe paths
4. **Type safety**: Use type hints and schemas
5. **Resource efficiency**: Proper connection management and cleanup
