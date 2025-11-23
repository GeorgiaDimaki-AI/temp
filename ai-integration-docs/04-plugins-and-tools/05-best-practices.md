# AI Tool Design Best Practices

## JSON Schema Mastery

### Descriptions are "Potent Instructions"

Research shows **90%+ error reduction** with well-written descriptions.

**Bad:**
```python
{
    "name": "get_weather",
    "description": "Get weather"  # Too vague!
}
```

**Good:**
```python
{
    "name": "get_weather",
    "description": """Get current weather conditions for a specified location.
    Returns temperature, humidity, wind speed, and conditions.
    Use this when users ask about CURRENT weather, not forecasts.""",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state or city and country (e.g., 'San Francisco, CA' or 'London, UK'). Be specific to avoid ambiguity.",
                "minLength": 1,
                "maxLength": 100
            }
        }
    }
}
```

### Schema Best Practices

**1. Use Constraints**
```python
{
    "temperature": {
        "type": "number",
        "minimum": -100,
        "maximum": 150,
        "description": "Temperature in Fahrenheit"
    },
    "email": {
        "type": "string",
        "format": "email",
        "pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
    },
    "count": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100
    }
}
```

**2. Use Enums for Fixed Options**
```python
{
    "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "description": "Task priority level. Use 'urgent' only for time-critical issues."
    }
}
```

**3. Provide Examples**
```python
{
    "date": {
        "type": "string",
        "description": "Date in YYYY-MM-DD format",
        "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
        "examples": ["2025-01-15", "2024-12-31"]
    }
}
```

**4. Use additionalProperties: false**
```python
{
    "type": "object",
    "properties": {...},
    "required": ["field1"],
    "additionalProperties": false  # Prevents extra fields
}
```

## Design Patterns

### 1. ReAct Pattern (Reason-Act-Observe)

Most common agentic pattern:

```
User Query
    ↓
Think (Reasoning)
    ↓
Act (Tool Use)
    ↓
Observe (Tool Result)
    ↓
Think (Process Result)
    ↓
Repeat or Respond
```

**Implementation:**
```python
def react_loop(user_query, max_iterations=10):
    context = [{"role": "user", "content": user_query}]

    for i in range(max_iterations):
        # Think: Model reasons about next action
        response = call_model(context, tools=available_tools)

        # Act: Execute tools if requested
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call)

                # Observe: Add result to context
                context.append({
                    "role": "tool",
                    "content": result
                })

        # Check if done
        if response.stop_reason == "end_turn":
            return response.content

    return "Max iterations reached"
```

### 2. Sequential Orchestration

For multi-step workflows:

```python
async def sequential_workflow(data):
    # Step 1: Validate
    validation_result = await call_tool("validate_data", data)

    if not validation_result["valid"]:
        return {"error": "Invalid data"}

    # Step 2: Process
    processed = await call_tool("process_data", validation_result["data"])

    # Step 3: Store
    stored = await call_tool("store_result", processed["result"])

    # Step 4: Notify
    await call_tool("send_notification", {
        "result_id": stored["id"]
    })

    return {"success": True, "id": stored["id"]}
```

### 3. Parallel Execution

For independent operations:

```python
import asyncio

async def parallel_research(topic):
    # Execute multiple research tools in parallel
    results = await asyncio.gather(
        call_tool("web_search", {"query": topic}),
        call_tool("academic_search", {"query": topic}),
        call_tool("news_search", {"query": topic})
    )

    # Synthesize results
    synthesis = await call_model(
        f"Synthesize these research results: {results}"
    )

    return synthesis
```

### 4. Error Recovery

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def resilient_tool_call(tool_name, args):
    """Tool call with automatic retries"""
    try:
        result = await execute_tool(tool_name, args)
        return result
    except TransientError as e:
        # Retry on transient errors
        logger.warning(f"Transient error: {e}, retrying...")
        raise
    except PermanentError as e:
        # Don't retry permanent errors
        logger.error(f"Permanent error: {e}")
        raise
```

## Production Best Practices

### 1. Validation

**Always validate tool inputs:**
```python
def execute_tool(tool_name: str, args: Dict) -> str:
    # 1. Validate tool exists
    if tool_name not in registered_tools:
        raise ValueError(f"Unknown tool: {tool_name}")

    # 2. Validate required arguments
    required = get_required_args(tool_name)
    missing = required - args.keys()
    if missing:
        raise ValueError(f"Missing required args: {missing}")

    # 3. Validate data types and ranges
    schema = get_tool_schema(tool_name)
    validate_against_schema(args, schema)

    # 4. Sanitize inputs (prevent injection)
    sanitized_args = sanitize_inputs(args)

    # 5. Execute
    return registered_tools[tool_name](**sanitized_args)
```

### 2. Security

**SQL Injection Prevention:**
```python
# Bad
def query_database(sql: str):
    return db.execute(sql)  # SQL injection risk!

# Good
def query_database(table: str, filters: Dict):
    # Only allow specific tables
    allowed_tables = ["users", "orders", "products"]
    if table not in allowed_tables:
        raise ValueError(f"Table {table} not allowed")

    # Use parameterized queries
    query = f"SELECT * FROM {table} WHERE "
    conditions = []
    params = []

    for field, value in filters.items():
        conditions.append(f"{field} = ?")
        params.append(value)

    query += " AND ".join(conditions)
    return db.execute(query, params)
```

**Command Injection Prevention:**
```python
import shlex

# Bad
def run_command(command: str):
    os.system(command)  # Command injection risk!

# Good
def run_command(program: str, args: List[str]):
    # Whitelist allowed programs
    allowed_programs = ["ls", "cat", "grep"]
    if program not in allowed_programs:
        raise ValueError(f"Program {program} not allowed")

    # Use subprocess with list (no shell)
    import subprocess
    result = subprocess.run(
        [program] + args,
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout
```

### 3. Rate Limiting

```python
from functools import wraps
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = defaultdict(list)

    def check(self, user_id: str) -> bool:
        now = time.time()

        # Remove old calls (older than 1 minute)
        self.calls[user_id] = [
            t for t in self.calls[user_id]
            if now - t < 60
        ]

        # Check limit
        if len(self.calls[user_id]) >= self.calls_per_minute:
            return False

        # Record call
        self.calls[user_id].append(now)
        return True

rate_limiter = RateLimiter(calls_per_minute=100)

def rate_limited(func):
    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        if not rate_limiter.check(user_id):
            raise Exception("Rate limit exceeded")
        return func(user_id, *args, **kwargs)
    return wrapper

@rate_limited
def execute_tool(user_id, tool_name, args):
    # Tool execution
    pass
```

### 4. Monitoring and Observability

```python
import logging
import time
from dataclasses import dataclass

@dataclass
class ToolMetrics:
    tool_name: str
    duration_ms: float
    success: bool
    error: str = None

class ToolMonitor:
    def __init__(self):
        self.metrics = []

    def record_execution(
        self,
        tool_name: str,
        duration_ms: float,
        success: bool,
        error: str = None
    ):
        metric = ToolMetrics(
            tool_name=tool_name,
            duration_ms=duration_ms,
            success=success,
            error=error
        )
        self.metrics.append(metric)

        # Log
        if success:
            logging.info(f"Tool {tool_name} succeeded in {duration_ms}ms")
        else:
            logging.error(f"Tool {tool_name} failed: {error}")

    def get_stats(self, tool_name: str = None):
        """Get aggregated statistics"""
        filtered = self.metrics
        if tool_name:
            filtered = [m for m in filtered if m.tool_name == tool_name]

        if not filtered:
            return None

        return {
            "total_calls": len(filtered),
            "success_rate": sum(1 for m in filtered if m.success) / len(filtered),
            "avg_duration_ms": sum(m.duration_ms for m in filtered) / len(filtered),
            "errors": [m.error for m in filtered if not m.success]
        }

monitor = ToolMonitor()

def execute_tool_monitored(tool_name, args):
    start = time.time()
    try:
        result = execute_tool(tool_name, args)
        duration_ms = (time.time() - start) * 1000
        monitor.record_execution(tool_name, duration_ms, True)
        return result
    except Exception as e:
        duration_ms = (time.time() - start) * 1000
        monitor.record_execution(tool_name, duration_ms, False, str(e))
        raise
```

### 5. Versioning

```python
# Tool versioning for backward compatibility
TOOLS_V1 = {
    "get_weather": get_weather_v1
}

TOOLS_V2 = {
    "get_weather": get_weather_v2,  # New version with more features
    "get_weather_v1": get_weather_v1  # Keep old version
}

def execute_tool(tool_name: str, args: Dict, api_version: str = "v2"):
    if api_version == "v1":
        tools = TOOLS_V1
    elif api_version == "v2":
        tools = TOOLS_V2
    else:
        raise ValueError(f"Unknown API version: {api_version}")

    return tools[tool_name](**args)
```

### 6. Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_weather_tool_success():
    """Test successful weather lookup"""
    result = get_weather("New York, NY")

    assert "temperature" in result
    assert "conditions" in result
    assert isinstance(result["temperature"], (int, float))

def test_weather_tool_invalid_location():
    """Test error handling for invalid location"""
    with pytest.raises(ValueError):
        get_weather("InvalidCity123")

def test_weather_tool_api_failure():
    """Test handling of API failures"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("API unavailable")

        result = get_weather("NYC")
        assert "error" in result

@pytest.mark.parametrize("location,expected", [
    ("NYC", "New York"),
    ("LA", "Los Angeles"),
    ("SF", "San Francisco")
])
def test_location_normalization(location, expected):
    """Test location name normalization"""
    result = get_weather(location)
    assert expected in result["location"]
```

## Performance Optimization

### 1. Caching

```python
from functools import lru_cache
import hashlib
import json

class ToolCache:
    def __init__(self, ttl_seconds=300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds

    def _make_key(self, tool_name: str, args: Dict) -> str:
        """Create cache key from tool name and args"""
        args_str = json.dumps(args, sort_keys=True)
        return f"{tool_name}:{hashlib.md5(args_str.encode()).hexdigest()}"

    def get(self, tool_name: str, args: Dict):
        """Get cached result if valid"""
        key = self._make_key(tool_name, args)
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return result
        return None

    def set(self, tool_name: str, args: Dict, result):
        """Cache result"""
        key = self._make_key(tool_name, args)
        self.cache[key] = (result, time.time())

cache = ToolCache(ttl_seconds=300)

def execute_tool_cached(tool_name, args):
    # Check cache
    cached = cache.get(tool_name, args)
    if cached is not None:
        return cached

    # Execute and cache
    result = execute_tool(tool_name, args)
    cache.set(tool_name, args, result)
    return result
```

### 2. Batching

```python
async def batch_tool_calls(tool_calls: List[ToolCall]):
    """Batch multiple tool calls for efficiency"""

    # Group by tool name
    batches = defaultdict(list)
    for call in tool_calls:
        batches[call.tool_name].append(call)

    results = []

    # Execute batches
    for tool_name, calls in batches.items():
        if supports_batch(tool_name):
            # Batch execution
            batch_args = [call.args for call in calls]
            batch_results = await execute_tool_batch(tool_name, batch_args)
            results.extend(batch_results)
        else:
            # Individual execution
            for call in calls:
                result = await execute_tool(tool_name, call.args)
                results.append(result)

    return results
```

## Summary

**Top 5 Best Practices:**

1. **Write Clear Descriptions** - 90% error reduction
2. **Validate Everything** - Security and reliability
3. **Monitor Execution** - Observability for debugging
4. **Use Structured Outputs** - Zero parsing errors
5. **Test Thoroughly** - Catch issues before production

Following these practices ensures production-ready AI tools that are reliable, secure, and maintainable.
