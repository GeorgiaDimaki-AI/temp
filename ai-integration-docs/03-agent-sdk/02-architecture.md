# Agent SDK Architecture & Technical Design

## Core Architecture

The Claude Agent SDK provides a complete agent orchestration framework built on three foundational pillars:

```
┌─────────────────────────────────────────────┐
│           Your Application                  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Claude Agent SDK                    │
│  ┌──────────────────────────────────────┐   │
│  │      Agent Orchestration Loop        │   │
│  │  (Gather → Act → Verify → Repeat)    │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │      Context Management              │   │
│  │  (Auto-compaction, persistence)      │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │      Tool System                     │   │
│  │  (Built-in + Custom + MCP)           │   │
│  └──────────────────────────────────────┘   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Claude API (Sonnet 4.5)             │
└─────────────────────────────────────────────┘
```

## Component Deep Dive

### 1. Agent Core

**Purpose**: Orchestrate agent behavior, manage state, enforce security

**Key Components**:

#### Context Manager
```python
class ContextManager:
    """Manages conversation history and automatic compaction"""

    def __init__(self, max_tokens: int = 200000):
        self.messages = []
        self.max_tokens = max_tokens
        self.token_count = 0

    def add_message(self, message: Message):
        """Add message and compact if needed"""
        self.messages.append(message)
        self.token_count += estimate_tokens(message)

        if self.token_count > self.max_tokens * 0.8:
            self._compact()

    def _compact(self):
        """Summarize older messages to save tokens"""
        # Keep recent messages (last 20% of context)
        recent = self.messages[-20:]

        # Summarize older messages
        older = self.messages[:-20]
        summary = generate_summary(older)

        # Replace with summary
        self.messages = [summary] + recent
        self.token_count = estimate_tokens(self.messages)
```

#### Permission Manager
```python
class PermissionManager:
    """Control what tools agents can use"""

    def __init__(
        self,
        allowed_tools: List[str],
        mode: str = "auto",  # "auto", "ask", "deny"
        working_directory: Path = None
    ):
        self.allowed_tools = set(allowed_tools)
        self.mode = mode
        self.working_directory = working_directory

    def check_permission(
        self,
        tool_name: str,
        tool_input: Dict
    ) -> Tuple[bool, Optional[str]]:
        """Check if tool use is allowed"""

        # Check if tool is in allowed list
        if tool_name not in self.allowed_tools:
            return False, f"Tool {tool_name} not allowed"

        # Check working directory restrictions
        if tool_name in ["Read", "Write", "Edit"]:
            path = Path(tool_input.get("file_path", ""))
            if not self._is_path_safe(path):
                return False, "Path outside working directory"

        # Check mode
        if self.mode == "ask":
            # Would prompt user for confirmation
            return self._ask_user(tool_name, tool_input)

        return True, None

    def _is_path_safe(self, path: Path) -> bool:
        """Ensure path is within working directory"""
        if not self.working_directory:
            return True

        try:
            resolved = path.resolve()
            return str(resolved).startswith(str(self.working_directory))
        except:
            return False
```

#### Session Manager
```python
class SessionManager:
    """Manage agent sessions and lifecycle"""

    def __init__(self):
        self.sessions = {}
        self.active_tasks = {}

    def create_session(
        self,
        session_id: str,
        options: ClaudeAgentOptions
    ) -> Session:
        """Create new agent session"""
        session = Session(
            id=session_id,
            options=options,
            created_at=datetime.utcnow(),
            context=ContextManager(max_tokens=options.max_tokens),
            permissions=PermissionManager(
                allowed_tools=options.allowed_tools,
                mode=options.permission_mode,
                working_directory=options.working_directory
            )
        )

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve existing session"""
        return self.sessions.get(session_id)

    def cleanup_session(self, session_id: str):
        """Clean up session resources"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Cancel any active tasks
            if session_id in self.active_tasks:
                for task in self.active_tasks[session_id]:
                    task.cancel()

            del self.sessions[session_id]
```

### 2. Agent Loop

The core orchestration pattern that drives autonomous behavior:

```python
async def agent_loop(
    session: Session,
    initial_prompt: str
) -> AsyncIterator[Message]:
    """Main agent execution loop"""

    # Add initial user message
    session.context.add_message({
        "role": "user",
        "content": initial_prompt
    })

    turn_count = 0
    max_turns = session.options.max_turns

    while turn_count < max_turns:
        # 1. GATHER CONTEXT
        # Agent has access to conversation history
        # Can use search tools to find relevant information

        # 2. GENERATE RESPONSE
        response = await call_claude_api(
            messages=session.context.messages,
            tools=session.available_tools,
            system=session.options.system_prompt
        )

        # 3. PROCESS TOOL CALLS
        if response.stop_reason == "tool_use":
            for tool_call in response.tool_calls:
                # Execute tool with permission checking
                result = await execute_tool(
                    session=session,
                    tool_call=tool_call
                )

                # Add tool result to context
                session.context.add_message({
                    "role": "tool",
                    "tool_use_id": tool_call.id,
                    "content": result
                })

                yield ToolUseMessage(
                    tool_name=tool_call.name,
                    input=tool_call.input,
                    output=result
                )

            # Continue loop to process tool results
            turn_count += 1
            continue

        # 4. FINAL RESPONSE
        if response.stop_reason == "end_turn":
            session.context.add_message({
                "role": "assistant",
                "content": response.content
            })

            yield TextMessage(content=response.content)

            # Check if task is complete
            if is_task_complete(response):
                break

        turn_count += 1

    # 5. CLEANUP
    if turn_count >= max_turns:
        yield ErrorMessage("Maximum turns reached")
```

### 3. Tool System

Three tiers of tools available to agents:

#### Tier 1: Built-in Tools

**File Operations:**
```python
@builtin_tool
async def Read(file_path: str, offset: int = 0, limit: int = 2000) -> str:
    """Read contents of a file"""
    # Implements safe file reading with:
    # - Path validation
    # - Permission checking
    # - Error handling
    # - Efficient chunking
    pass

@builtin_tool
async def Write(file_path: str, content: str) -> str:
    """Write content to a file"""
    # Implements safe file writing with:
    # - Path validation
    # - Backup creation
    # - Atomic writes
    # - Error recovery
    pass

@builtin_tool
async def Edit(file_path: str, old_string: str, new_string: str) -> str:
    """Edit file by replacing exact string matches"""
    # Implements precise editing with:
    # - Exact match validation
    # - Preview before apply
    # - Rollback capability
    pass
```

**Command Execution:**
```python
@builtin_tool
async def Bash(
    command: str,
    timeout: int = 120000,
    run_in_background: bool = False
) -> str:
    """Execute bash command"""
    # Implements safe execution with:
    # - Command validation
    # - Timeout enforcement
    # - Output capture
    # - Background job management
    pass
```

**Web Access:**
```python
@builtin_tool
async def WebFetch(url: str, prompt: str) -> str:
    """Fetch and process web content"""
    # Fetches URL, converts to markdown, processes with LLM
    pass

@builtin_tool
async def WebSearch(query: str) -> List[SearchResult]:
    """Search the web"""
    # Performs web search, returns structured results
    pass
```

#### Tier 2: Custom Tools (In-Process MCP)

Define Python functions as tools:

```python
from claude_agent_sdk import create_sdk_mcp_server

def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax on an amount

    Args:
        amount: The base amount
        rate: Tax rate as percentage (e.g., 8.5 for 8.5%)

    Returns:
        Total amount including tax
    """
    return amount * (1 + rate / 100)

def query_customer_db(customer_id: str) -> Dict:
    """Query customer database

    Args:
        customer_id: Customer identifier

    Returns:
        Customer record with details
    """
    # Your database logic
    return db.query("SELECT * FROM customers WHERE id = ?", customer_id)

# Create MCP server with your tools
custom_tools = create_sdk_mcp_server(
    name="business-tools",
    tools=[calculate_tax, query_customer_db]
)

# Use in agent
options = ClaudeAgentOptions(
    mcp_servers=[custom_tools]
)
```

#### Tier 3: External MCP Servers

Connect to external MCP servers for complex integrations:

```python
from claude_agent_sdk import ExternalMCPServer

# Connect to external database server
db_server = ExternalMCPServer(
    name="postgres",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres"],
    env={
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
    }
)

# Connect to external API server
api_server = ExternalMCPServer(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
    }
)

options = ClaudeAgentOptions(
    mcp_servers=[db_server, api_server]
)
```

### 4. Hooks System

Deterministic callbacks for validation, logging, and custom logic:

```python
from claude_agent_sdk import (
    PreToolUseHook,
    PostToolUseHook,
    HookMatcher,
    HookContext
)

# Pre-tool hook for validation
async def validate_sql(context: HookContext) -> Dict:
    """Validate SQL queries before execution"""
    if context.tool_name == "query_database":
        sql = context.tool_input.get("sql", "")

        # Block destructive operations
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        sql_upper = sql.upper()

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return {
                    "permission_decision": "deny",
                    "feedback": f"Blocked dangerous SQL: {keyword}"
                }

        # Require LIMIT for SELECT
        if "SELECT" in sql_upper and "LIMIT" not in sql_upper:
            return {
                "permission_decision": "deny",
                "feedback": "SELECT queries must include LIMIT clause"
            }

    return {"permission_decision": "allow"}

# Post-tool hook for logging
async def log_tool_execution(context: HookContext) -> Dict:
    """Log all tool executions for audit"""
    logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "tool": context.tool_name,
        "input": context.tool_input,
        "output_preview": str(context.tool_output)[:100],
        "duration_ms": context.duration_ms,
        "success": context.success
    })

    return {}

# Register hooks
hooks = [
    PreToolUseHook(
        matcher=HookMatcher(tool_names=["query_database"]),
        callback=validate_sql
    ),
    PostToolUseHook(
        matcher=HookMatcher(all_tools=True),
        callback=log_tool_execution
    )
]

options = ClaudeAgentOptions(hooks=hooks)
```

### 5. Subagents

Specialized agents with isolated context windows for parallel work:

**Definition** (`.claude/agents/researcher.md`):
```markdown
---
name: researcher
description: Specialized research agent
system_prompt: |
  You are a research specialist. Your job is to thoroughly research topics
  and provide comprehensive summaries with citations.

  When researching:
  1. Use WebSearch to find authoritative sources
  2. Use WebFetch to read full articles
  3. Cross-reference multiple sources
  4. Cite all sources with URLs
  5. Provide balanced analysis
tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
max_turns: 30
---
```

**Usage**:
```python
# Subagent is invoked automatically when main agent delegates
# Main agent might say: "Let me have my research specialist investigate this"
# SDK automatically spawns subagent with isolated context

# Or programmatically:
from claude_agent_sdk import spawn_subagent

async def use_subagent(session: Session, task: str):
    """Delegate to specialized subagent"""

    result = await spawn_subagent(
        session=session,
        agent_name="researcher",
        prompt=task,
        return_to_parent=True
    )

    return result
```

### 6. Memory System

**CLAUDE.md Scratchpad**:

Persistent memory file that agents can use to remember important information across sessions:

```markdown
# .claude/CLAUDE.md

## Project Context
This is a Python web application using FastAPI and PostgreSQL.

## Important Conventions
- Use async/await for all I/O operations
- Tests go in tests/ directory
- Follow PEP 8 style guide
- All database queries use SQLAlchemy ORM

## Key Files
- main.py: Application entry point
- models.py: Database models
- routes/: API endpoints
- services/: Business logic

## Recent Decisions
- 2025-01-15: Switched from REST to GraphQL for new features
- 2025-01-10: Added Redis caching for user sessions
```

Agents automatically read this file at startup and can update it.

## Configuration Options

### ClaudeAgentOptions

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Model selection
    model="claude-sonnet-4-5-20250929",  # Latest Sonnet 4.5

    # System prompt
    system_prompt="You are a helpful coding assistant",

    # Context management
    max_turns=50,  # Maximum conversation turns
    max_tokens=200000,  # Context window size

    # Tool control
    allowed_tools=[
        "Read", "Write", "Edit",  # File operations
        "Bash",  # Command execution
        "WebSearch", "WebFetch"  # Web access
    ],

    # Permission model
    permission_mode="auto",  # "auto", "ask", "deny"

    # Working directory
    working_directory="/workspace",

    # Custom tools
    mcp_servers=[custom_tool_server],

    # Hooks
    hooks=[validation_hook, logging_hook],

    # Temperature (creativity)
    temperature=1.0,  # 0.0 to 1.0

    # Timeouts
    tool_timeout=120000,  # 2 minutes

    # Cost control
    max_tokens_per_turn=4000
)
```

## Performance Optimizations

### 1. Context Compaction Strategy

```python
class SmartCompaction:
    """Intelligent context compaction"""

    def compact(self, messages: List[Message]) -> List[Message]:
        """Compact while preserving important information"""

        # Always keep
        keep = []

        # System message (first)
        keep.append(messages[0])

        # Recent messages (last 20% of context)
        recent_count = len(messages) // 5
        recent = messages[-recent_count:]

        # Important messages (errors, user messages, key decisions)
        middle = messages[1:-recent_count]
        important = [
            msg for msg in middle
            if self._is_important(msg)
        ]

        # Summarize the rest
        unimportant = [
            msg for msg in middle
            if not self._is_important(msg)
        ]
        summary = self._generate_summary(unimportant)

        # Combine
        return keep + [summary] + important + recent

    def _is_important(self, msg: Message) -> bool:
        """Determine if message should be preserved"""
        if msg.role == "user":
            return True
        if "error" in str(msg.content).lower():
            return True
        if msg.get("tool_use"):
            # Keep successful tool uses
            return True
        return False
```

### 2. Parallel Tool Execution

```python
async def execute_tools_parallel(
    tool_calls: List[ToolCall],
    session: Session
) -> List[ToolResult]:
    """Execute multiple independent tools in parallel"""

    tasks = [
        execute_tool(session, tool_call)
        for tool_call in tool_calls
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results
```

### 3. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_file_content(file_path: str, mtime: float) -> str:
    """Cache file contents based on modification time"""
    with open(file_path) as f:
        return f.read()

# Use with mtime to invalidate on changes
mtime = os.path.getmtime(file_path)
content = get_file_content(file_path, mtime)
```

## Security Model

### Sandboxing

```python
# Run in Docker container
docker run -it \
  -v /workspace:/workspace:ro \  # Read-only workspace
  -v /output:/output \            # Write-only output
  --network none \                # No network access
  --memory 2g \                   # Memory limit
  --cpus 1.0 \                   # CPU limit
  agent-sdk python agent.py
```

### Principle of Least Privilege

```python
# Minimal permissions
options = ClaudeAgentOptions(
    allowed_tools=["Read"],  # Read-only
    working_directory="/workspace/docs",  # Limited scope
    permission_mode="ask"  # Require confirmation
)
```

This architecture enables building sophisticated, production-ready AI agents with full control over behavior, security, and capabilities.
