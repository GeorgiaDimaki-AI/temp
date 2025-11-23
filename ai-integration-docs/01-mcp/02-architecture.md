# MCP Architecture & Technical Design

## Protocol Design

MCP is built on **JSON-RPC 2.0**, a well-established remote procedure call protocol that provides:
- Standardized message format
- Request/response linking
- Error handling
- Bidirectional communication

### Why JSON-RPC 2.0?

**Advantages:**
1. **Proven standard**: Used in VS Code, Ethereum, and many distributed systems
2. **Simple**: Easy to implement in any language
3. **Flexible**: Supports sync and async patterns
4. **Debuggable**: Human-readable JSON messages
5. **Extensible**: Easy to add new methods without breaking changes

## Architecture Overview

MCP follows a **client-server architecture** with three core components:

```
┌─────────────────────────────────────────┐
│          MCP HOST (AI Application)      │
│         (Claude Desktop, VS Code)       │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      MCP CLIENT (Internal)      │   │
│  │  Manages server connections     │   │
│  └──────────────┬──────────────────┘   │
└─────────────────┼──────────────────────┘
                  │ JSON-RPC 2.0
                  │ (Transport Layer)
                  │
┌─────────────────▼──────────────────────┐
│         MCP SERVER (External)          │
│    Exposes Tools, Resources, Prompts   │
│  (Database, API, File System, etc.)    │
└────────────────────────────────────────┘
```

### Components Deep Dive

#### 1. MCP Host

The user-facing AI application (e.g., Claude Desktop, IDEs)

**Responsibilities:**
- Coordinates connections to multiple servers
- Manages security and permissions
- Mediates ALL AI-resource interactions
- Handles user approval workflows
- Aggregates capabilities from all servers

**Examples:**
- Claude Desktop
- Visual Studio Code
- Cursor IDE
- Replit
- Custom applications

#### 2. MCP Client

Component within the host that manages communication

**Key characteristics:**
- Each client maintains **1:1 connection** with a single server
- Handles protocol compliance
- Routes messages appropriately
- Manages connection lifecycle
- Discovers server capabilities

**Why 1:1 mapping?**
- Security isolation between servers
- Independent lifecycle management
- Clear responsibility boundaries
- Prevents cross-contamination

#### 3. MCP Server

External program exposing capabilities

**Key characteristics:**
- Runs as isolated, independent process
- Communicates exclusively via JSON-RPC
- Exposes tools, resources, and/or prompts
- Stateless or stateful (implementation choice)
- Can be local (STDIO) or remote (HTTP)

## Layered Design

MCP operates through two integrated layers:

### Protocol Layer (Data Layer)

**Purpose**: Defines what clients and servers can exchange

**Responsibilities:**
- Implements JSON-RPC 2.0 messaging
- Handles lifecycle management
- Manages capability negotiation
- Defines message types and schemas

**Message Types:**
1. **Requests**: Messages with IDs expecting responses
2. **Responses**: Replies to requests
3. **Notifications**: One-way messages, no response expected
4. **Errors**: Error responses for failed requests

### Transport Layer

**Purpose**: Manages how messages are sent

**Responsibilities:**
- Connection lifecycle management
- Message serialization
- Error handling
- Multiple transport mechanism support

**Supported Transports:**
- STDIO (Standard Input/Output)
- Streamable HTTP (current standard)
- SSE (Server-Sent Events) - deprecated

## Communication Patterns

### Message Exchange

#### Request Message

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate-bmi",
    "arguments": {
      "weightKg": 70,
      "heightM": 1.75
    }
  }
}
```

#### Response Message

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "BMI: 22.86 (Normal weight)"
      }
    ]
  }
}
```

#### Notification Message

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///data/report.pdf"
  }
}
```

#### Error Message

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": {
      "method": "invalid/method"
    }
  }
}
```

### Connection Lifecycle

```
┌─────────────────────────────────────────────┐
│ 1. INITIALIZATION                           │
│    Client → Server: initialize request      │
│    (protocol version, capabilities)         │
└─────────────┬───────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ 2. RESPONSE                                 │
│    Server → Client: initialize response     │
│    (server capabilities, protocol version)  │
└─────────────┬───────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ 3. CONFIRMATION                             │
│    Client → Server: initialized             │
│    (notification, no response)              │
└─────────────┬───────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ 4. OPERATION                                │
│    - Discover tools/resources/prompts       │
│    - Execute tools                          │
│    - Read resources                         │
│    - Get prompts                            │
└─────────────┬───────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ 5. UPDATES (Optional)                       │
│    Server → Client: capability changes      │
│    (notifications for dynamic updates)      │
└─────────────────────────────────────────────┘
```

### Capability Negotiation

During initialization, both parties declare their capabilities:

#### Server Capabilities

```json
{
  "capabilities": {
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "tools": {
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "logging": {}
  }
}
```

#### Client Capabilities

```json
{
  "capabilities": {
    "sampling": {},
    "experimental": {
      "multimodalContent": true
    }
  }
}
```

**Benefits:**
- Prevents runtime errors
- Enables graceful degradation
- Allows feature detection
- Supports protocol evolution

## Transport Mechanisms

### 1. STDIO (Standard Input/Output)

**Best for**: Local integrations, CLI tools, development

#### How It Works

```
┌──────────────────┐
│   MCP CLIENT     │
│   (in process)   │
└────────┬─────────┘
         │ spawn()
         ▼
┌──────────────────┐
│   MCP SERVER     │
│  (child process) │
└──────────────────┘
         │
    STDIN/STDOUT
         │
    JSON-RPC 2.0
```

**Process:**
1. Client spawns server as child process
2. Client writes to server's STDIN
3. Server responds via STDOUT
4. Server writes logs to STDERR

**Characteristics:**
- **Latency**: Microseconds (in-process communication)
- **Setup**: Simple, no network configuration
- **Security**: OS-level process isolation
- **Scope**: Local machine only
- **Lifecycle**: Server lives with client process

**Example Configuration** (Claude Desktop):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/files"
      ]
    }
  }
}
```

### 2. Streamable HTTP (Modern Standard)

**Best for**: Remote services, web applications, cloud deployments

#### How It Works

```
┌──────────────────┐
│   MCP CLIENT     │
│                  │
└────────┬─────────┘
         │ HTTP POST
         │ (per message)
         ▼
┌──────────────────┐
│   MCP SERVER     │
│   (HTTP server)  │
└──────────────────┘
         │
    SSE Stream
         │
   (for push)
```

**Process:**
1. Every JSON-RPC message sent as HTTP POST
2. Server responds inline or via SSE stream
3. Supports both request-response and server-initiated communication

**Characteristics:**
- **Stateless**: Each request is independent
- **Infrastructure-friendly**: Works with proxies, load balancers, CDNs
- **Scalable**: Easy horizontal scaling
- **Flexible**: Supports long-lived and ephemeral connections
- **Standard**: Uses existing HTTP ecosystem

**Advantages over SSE transport:**
- No requirement for long-lived connections
- Simpler session management
- Better for serverless environments
- Works with more infrastructure

**Example:**

```typescript
// Server configuration
const server = new McpServer({
  transport: 'streamable-http',
  port: 3000,
  path: '/mcp'
});

// Client connection
const client = new McpClient({
  url: 'https://api.example.com/mcp',
  headers: {
    'Authorization': 'Bearer token'
  }
});
```

### 3. SSE (Server-Sent Events) - DEPRECATED

**Status**: Legacy transport, replaced by Streamable HTTP

**Why deprecated:**
- Required maintaining two separate endpoints
- Complicated session management
- More complex error handling
- Harder to deploy and scale

## Core Primitives

### Server-Side Primitives

#### 1. Resources

**Definition**: Read-only data sources that provide contextual information

**Purpose**:
- Supply context to the LLM
- Enable RAG (Retrieval Augmented Generation)
- Expose data without mutation

**Key features:**
- URI-based addressing
- Support for templates
- MIME type specification
- Text or binary content

**Example use cases:**
- File contents
- Database schemas
- API documentation
- Configuration data
- Knowledge base articles

**Implementation:**

```python
@server.list_resources()
async def list_resources():
    return [
        {
            "uri": "file:///docs/api.md",
            "name": "API Documentation",
            "mimeType": "text/markdown",
            "description": "REST API reference"
        }
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "file:///docs/api.md":
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/markdown",
                    "text": "# API Documentation\n..."
                }
            ]
        }
```

**URI Templates:**

```python
{
    "uri": "user://{user_id}/profile",
    "name": "User Profile",
    "mimeType": "application/json"
}

# Client can request:
# - user://123/profile
# - user://456/profile
```

#### 2. Tools

**Definition**: Executable functions that the AI can invoke

**Purpose**:
- Perform actions on behalf of the user
- Execute computations
- Interact with external systems

**Key features:**
- JSON Schema for input validation
- Structured output
- Synchronous execution
- Error handling

**Example use cases:**
- Database queries
- API calls
- File operations
- Calculations
- Web scraping

**Implementation:**

```python
@server.tool()
async def search_database(
    query: str,
    limit: int = 10
) -> dict:
    """
    Search the database for matching records.

    Args:
        query: Search query string
        limit: Maximum number of results (default: 10)

    Returns:
        Dictionary with search results
    """
    results = db.search(query, limit=limit)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Found {len(results)} results"
            }
        ],
        "isError": False
    }
```

**Input Schema** (auto-generated from function signature):

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query string"
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of results",
      "default": 10
    }
  },
  "required": ["query"]
}
```

#### 3. Prompts

**Definition**: Reusable interaction templates

**Purpose**:
- Guide model behavior
- Provide structured workflows
- Enable parameterizable templates

**Key features:**
- Named templates
- Argument support
- Message composition
- Context injection

**Example use cases:**
- Code review templates
- Bug report formats
- Analysis frameworks
- Query templates

**Implementation:**

```python
@server.list_prompts()
async def list_prompts():
    return [
        {
            "name": "code_review",
            "description": "Review code for quality and issues",
            "arguments": [
                {
                    "name": "language",
                    "description": "Programming language",
                    "required": True
                },
                {
                    "name": "focus",
                    "description": "Review focus area",
                    "required": False
                }
            ]
        }
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "code_review":
        language = arguments["language"]
        focus = arguments.get("focus", "all aspects")

        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Please review this {language} code,
                        focusing on {focus}. Check for:
                        1. Code quality and best practices
                        2. Potential bugs or errors
                        3. Performance improvements
                        4. Security vulnerabilities"""
                    }
                }
            ]
        }
```

### Client-Side Primitives

#### 1. Sampling

**Definition**: Allows servers to request LLM completions

**Purpose**:
- Enable nested AI calls
- Support agentic behaviors
- Create AI-powered tools

**Flow:**

```
Server → Client: "I need an LLM completion"
Client → LLM: Sends prompt
LLM → Client: Returns completion
Client → Server: Forwards result
```

**Example:**

```python
# Server requests sampling
async def analyze_text(text: str):
    # Server asks client to run LLM inference
    analysis = await request_sampling(
        messages=[
            {
                "role": "user",
                "content": f"Analyze sentiment of: {text}"
            }
        ]
    )
    return analysis
```

#### 2. Elicitation

**Definition**: Requests user input or confirmation

**Purpose**:
- Maintain human-in-the-loop control
- Support permission workflows
- Enable interactive flows

**Example:**

```python
# Server requests user confirmation
async def delete_file(path: str):
    # Ask user for permission
    approved = await elicit_user_input(
        prompt=f"Delete {path}?",
        type="confirmation"
    )

    if approved:
        os.remove(path)
        return "File deleted"
    else:
        return "Operation cancelled"
```

#### 3. Logging

**Definition**: Sends diagnostic messages to the client

**Purpose**:
- Support debugging
- Enable monitoring
- Provide visibility

**Levels:**
- debug
- info
- warning
- error
- critical

**Example:**

```python
async def process_data(data: str):
    await log("info", "Processing started")

    try:
        result = expensive_operation(data)
        await log("debug", f"Result: {result}")
        return result
    except Exception as e:
        await log("error", f"Failed: {e}")
        raise
```

## Security Architecture

### Security Principles

#### 1. Host as Security Broker

The host mediates ALL interactions between AI and resources:

```
AI Model → Host → MCP Client → MCP Server → Resource
         ↑
    Security Gate
    - Authentication
    - Authorization
    - Audit logging
```

**No direct model-to-server communication**

#### 2. 1:1 Client-Server Mapping

Each resource type gets dedicated, isolated communication:

**Benefits:**
- Clear security boundaries
- Independent permission models
- Isolated credential management
- Prevents cross-contamination

#### 3. Capability-Based Security

Servers declare capabilities, hosts decide what to allow:

```python
# Server declares
capabilities = {
    "tools": ["read_file", "write_file", "delete_file"]
}

# Host allows subset
allowed_tools = ["read_file"]  # No write/delete
```

### Authentication & Authorization

#### OAuth 2.1 Foundation

MCP added OAuth 2.1 support in March 2025:

**Features:**
- Standardized authorization framework
- Mandatory PKCE (Proof Key for Code Exchange)
- Protection against authorization code interception
- Refresh token rotation

**Flow:**

```
1. User initiates connection
2. MCP client redirects to authorization server
3. User authenticates and grants permissions
4. Client receives authorization code
5. Client exchanges code for access token (with PKCE)
6. Client uses token for MCP server access
7. Token refreshed as needed
```

#### Dynamic Client Registration (DCR)

Runtime credential acquisition without manual pre-registration:

```
1. Client discovers authorization server metadata
2. Client auto-registers with auth server
3. Receives client_id and client_secret
4. Uses credentials for OAuth flow
```

#### Authorization Server Metadata

Automatic endpoint discovery:

```json
GET /.well-known/oauth-authorization-server

{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "registration_endpoint": "https://auth.example.com/register"
}
```

### Security Best Practices

#### Secret Management

✅ **DO:**
- Use environment variables
- Implement secret rotation
- Use specialized secret storage (Vault, AWS Secrets Manager)
- Encrypt secrets at rest

❌ **DON'T:**
- Embed credentials in code
- Commit secrets to version control
- Log secrets
- Share credentials across environments

#### Transport Security

✅ **Required:**
- TLS 1.2 or higher for remote connections
- Certificate validation
- Encrypted communications

#### Logging Security

❌ **NEVER log:**
- Authorization headers
- Access tokens or refresh tokens
- API keys or passwords
- Full query strings (may contain secrets)
- User passwords or PII

✅ **DO log:**
- Request/response metadata
- Tool invocations (without sensitive data)
- Error conditions
- Performance metrics

#### Permission Models

**Principle of Least Privilege:**

```python
# Start restrictive
permissions = {
    "read": True,
    "write": False,
    "delete": False,
    "admin": False
}

# Grant incrementally as needed
```

**User Consent:**
- Require explicit authorization
- Support permission revocation
- Provide transparency (show what tools do)
- Allow granular control

## Design Patterns

MCP simplifies AI integration using established patterns:

### 1. Facade/API Gateway

Provides unified interface to complex subsystems:

```python
# Complex subsystem
database = DatabaseConnection()
cache = RedisCache()
api = ExternalAPI()

# Simple facade
@mcp.tool()
def get_user_data(user_id: str):
    # Coordinates all subsystems
    cached = cache.get(user_id)
    if cached:
        return cached

    db_data = database.fetch(user_id)
    api_data = api.enrich(db_data)

    cache.set(user_id, api_data)
    return api_data
```

### 2. Adapter

Converts incompatible interfaces:

```python
# Legacy system with incompatible interface
class LegacySystem:
    def FetchData(self, ID):  # Non-standard naming
        return legacy_db.Get(ID)

# MCP adapter
@mcp.tool()
def get_data(id: str) -> dict:
    """Standard interface for legacy system"""
    legacy = LegacySystem()
    raw_data = legacy.FetchData(id)
    return normalize(raw_data)  # Convert to standard format
```

### 3. Sidecar

Isolated process per integration:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ MCP Server  │     │ MCP Server  │     │ MCP Server  │
│  (Database) │     │   (Email)   │     │    (API)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                    ┌──────┴──────┐
                    │  MCP Host   │
                    │   (Claude)  │
                    └─────────────┘
```

**Benefits:**
- Independent scaling
- Isolated failures
- Separate deployment cycles
- Resource isolation

### 4. Orchestrator

Coordinates multiple services:

```python
@mcp.tool()
async def process_order(order_id: str):
    """Orchestrates order processing across systems"""

    # Coordinate multiple services
    order = await orders.fetch(order_id)
    inventory = await inventory.reserve(order.items)
    payment = await payments.charge(order.total)
    shipping = await shipping.create_label(order)

    return {
        "order": order,
        "inventory": inventory,
        "payment": payment,
        "shipping": shipping
    }
```

## Performance Considerations

### Lazy Loading

Only load capabilities when needed:

```python
# Don't load all tools upfront
# Discover dynamically
tools = await client.list_tools()  # Returns metadata only

# Load tool details on demand
tool_details = await client.get_tool("search_database")
```

### Streaming

For large data transfers:

```python
@server.resource("file://large-dataset.csv")
async def stream_large_file():
    """Stream large file in chunks"""
    async with aio.open("large-dataset.csv") as f:
        async for chunk in f:
            yield chunk
```

### Caching

Reduce redundant operations:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input_data):
    # Cached for repeated calls
    return process(input_data)
```

### Connection Pooling

Reuse connections for remote servers:

```python
# Connection pool for HTTP transport
client = McpClient(
    url="https://api.example.com/mcp",
    pool_size=10,  # Maintain 10 connections
    pool_timeout=30
)
```
