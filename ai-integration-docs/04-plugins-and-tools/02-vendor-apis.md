# Vendor APIs for AI Tools

## Overview of Approaches

### Anthropic (Claude)

**Two Approaches:**

1. **Native Tool Use API** (Vendor-specific)
2. **Model Context Protocol (MCP)** (Universal standard)

**Tool Use API:**
```python
import anthropic

client = anthropic.Anthropic(api_key="...")

tools = [{
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "What's the weather in NYC?"}],
    tools=tools,
    max_tokens=1024
)
```

**Latest Feature: Structured Outputs (Nov 2025)**
- Guaranteed schema compliance
- Zero parsing errors
- Production-ready reliability

### OpenAI

**Function Calling API:**

```python
from openai import OpenAI

client = OpenAI(api_key="...")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        },
        "strict": True  # Structured outputs mode
    }
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Weather in NYC?"}],
    tools=tools,
    parallel_tool_calls=True  # Execute multiple tools in parallel
)
```

**Key Features:**
- Parallel function calling
- Strict mode (structured outputs)
- Forced tool use

### Google (Gemini)

**Unique Feature: Auto-converts Python functions**

```python
import google.generativeai as genai

def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"Weather in {location}: Sunny, 72°F"

model = genai.GenerativeModel(
    "gemini-3-flash",
    tools=[get_weather]  # Automatically converted!
)

response = model.generate_content(
    "What's the weather in NYC?",
    tool_config={"function_calling_config": {"mode": "AUTO"}}
)
```

**Modes:**
- `AUTO`: Model decides when to use tools
- `ANY`: Must use at least one tool
- `NONE`: Disable tools for this request

### Microsoft

**Different APIs per product:**

**Azure OpenAI:**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://your-resource.openai.azure.com",
    api_key="...",
    api_version="2024-10-01-preview"
)

# Same as OpenAI function calling
```

**M365 Copilot:**
- Declarative agent manifests
- Plugin system with OpenAPI specs

**GitHub Copilot:**
- Extension API for tools
- Custom agent builders

### AWS Bedrock

**Converse API (Unified):**

```python
import boto3

bedrock = boto3.client("bedrock-runtime")

response = bedrock.converse(
    modelId="anthropic.claude-sonnet-4-5-v1",
    messages=[{"role": "user", "content": [{"text": "Weather in NYC?"}]}],
    toolConfig={
        "tools": [{
            "toolSpec": {
                "name": "get_weather",
                "description": "Get current weather",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"}
                        }
                    }
                }
            }
        }]
    }
)
```

**Advantages:**
- Works with multiple model providers
- Unified API across Claude, Llama, etc.
- AWS infrastructure integration

## Key Architectural Differences

### Schema Definition

**Anthropic:**
- JSON Schema directly in tool definition
- Clear separation of name, description, input_schema

**OpenAI:**
- JSON Schema in `parameters` field
- `strict: true` for guaranteed compliance

**Google:**
- Automatic from Python type hints
- Or manual JSON Schema

**AWS Bedrock:**
- Nested structure with `toolSpec`
- `inputSchema.json` for schema definition

### Execution Flow

**All vendors follow similar pattern:**
1. User query → Model
2. Model returns tool calls
3. Execute tools
4. Send results back to model
5. Model generates final response

**Differences:**
- **Parallel execution**: OpenAI, Anthropic (multi-tool)
- **Auto execution**: Google Gemini (optional)
- **Streaming**: Different implementations

## When to Use Each

**Anthropic:** Best for safety-critical, structured outputs, long context

**OpenAI:** Best for mature ecosystem, extensive docs, parallel tools

**Google:** Best for Python-first development, auto-conversion

**Microsoft:** Best for enterprise integration, M365 ecosystem

**AWS:** Best for multi-provider, cloud infrastructure

