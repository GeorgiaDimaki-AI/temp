# AI/LLM Tools & Plugins - Quick Reference Guide

## Vendor Comparison at a Glance

| Feature | OpenAI | Anthropic (Claude) | Google (Gemini) | Microsoft | AWS Bedrock |
|---------|--------|-------------------|-----------------|-----------|-------------|
| **Primary Approach** | Function Calling | MCP + Tool Use | Function Calling | Multi-product APIs | Converse API |
| **Parallel Execution** | ✅ Yes | ✅ Yes | ✅ Compositional | ✅ Yes | ✅ Yes |
| **Structured Outputs** | ✅ Strict mode | ✅ Beta (Nov 2025) | ✅ Yes | ✅ Yes | Via Claude models |
| **MCP Support** | ✅ Adopted (Mar 2025) | ✅ Creator | ✅ Announced (Apr 2025) | ✅ Oct 2025 | Via integrations |
| **Auto Function Execution** | ❌ Manual | ❌ Manual | ✅ Automatic mode | Varies | ❌ Manual |
| **SDK Languages** | Python, Node.js, .NET, Go | Python, TypeScript | Python, Node.js, Go | .NET, Python, TypeScript | Python, Java, .NET |
| **Free Tier** | ❌ No | ❌ No | ✅ 1,500 req/day | Limited | ❌ No |

## Protocol Comparison

| Aspect | Function Calling | MCP | A2A |
|--------|-----------------|-----|-----|
| **Purpose** | Tool integration | Universal tool protocol | Agent collaboration |
| **Scope** | Single app | Cross-platform | Multi-agent |
| **Standard** | Vendor-specific | Open (Anthropic) | Open (Linux Foundation) |
| **Transport** | LLM API | JSON-RPC over stdio/HTTP | HTTP/SSE + JSON-RPC |
| **Discovery** | Pre-defined | Server manifest | Agent Cards |
| **Security** | App-level | Host approval | OAuth 2.0, API keys |
| **Best For** | Low latency, tight integration | Reusable tools, vendor-agnostic | Agent networks |

## Tool Choice Parameters

### OpenAI
```python
tool_choice = "auto"  # Let model decide
tool_choice = "none"  # Prevent tool use
tool_choice = {"type": "function", "function": {"name": "tool_name"}}  # Force tool
parallel_tool_calls = True  # Enable parallel (default)
```

### Anthropic
```python
tool_choice = {"type": "auto"}  # Let model decide
tool_choice = {"type": "any"}  # Force any tool
tool_choice = {"type": "tool", "name": "tool_name"}  # Force specific
# Parallel supported by default
```

### Google Gemini
```python
mode = "AUTO"  # Let model decide
mode = "NONE"  # Prevent tools
mode = "ANY"  # Force tool use
allowed_function_names = ["tool1", "tool2"]  # Limit choices
```

## JSON Schema Template

```json
{
  "name": "function_name",
  "description": "Clear description of what this does and WHEN to use it",
  "parameters": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Detailed description with examples",
        "minLength": 1,
        "maxLength": 100
      },
      "param2": {
        "type": "integer",
        "description": "Integer parameter",
        "minimum": 1,
        "maximum": 100,
        "default": 10
      },
      "param3": {
        "type": "string",
        "enum": ["option1", "option2", "option3"],
        "description": "Choice parameter"
      },
      "param4": {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 1,
        "maxItems": 10,
        "uniqueItems": true
      }
    },
    "required": ["param1"],
    "additionalProperties": false
  }
}
```

## Common JSON Schema Types

| Type | Example | Constraints |
|------|---------|-------------|
| `string` | `"hello"` | minLength, maxLength, pattern, format, enum |
| `integer` | `42` | minimum, maximum, multipleOf |
| `number` | `3.14` | minimum, maximum, multipleOf |
| `boolean` | `true` | - |
| `array` | `[1,2,3]` | items, minItems, maxItems, uniqueItems |
| `object` | `{"a":1}` | properties, required, additionalProperties |
| `null` | `null` | - |

### Useful Formats
- `date-time`: ISO 8601 timestamp
- `date`: YYYY-MM-DD
- `time`: HH:MM:SS
- `email`: Email address
- `uri`: URI/URL
- `uuid`: UUID string

## Quick Start Examples

### OpenAI (Minimal)
```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}
        }
    }]
)
```

### Anthropic (Minimal)
```python
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4.5-20251022",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}}
    }],
    messages=[{"role": "user", "content": "What's the weather?"}]
)
```

### Google Gemini (Minimal - Auto)
```python
import google.generativeai as genai

def get_weather(location: str):
    """Get weather for location"""
    return {"temp": 72, "conditions": "sunny"}

model = genai.GenerativeModel("gemini-3-pro", tools=[get_weather])
response = model.generate_content("What's the weather?")
```

### MCP Server (Minimal)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get weather for location"""
    return f"Weather in {location}: 72°F, sunny"

mcp.run()
```

## Design Pattern Quick Reference

### 1. ReAct (Reason-Act)
```
User Query → Think → Action (Tool) → Observe → Think → Response
```
**Use for:** Complex multi-step problems

### 2. Sequential Chain
```
Tool 1 → Tool 2 → Tool 3 → Final Answer
```
**Use for:** Ordered workflows (research → analyze → report)

### 3. Parallel Execution
```
                → Tool 1 →
User Query →   → Tool 2 → → Synthesize → Response
                → Tool 3 →
```
**Use for:** Independent data gathering

### 4. Dynamic Routing
```
User Query → Router Agent → Specialized Agent → Response
```
**Use for:** Multi-agent systems with specialized agents

## Error Handling Checklist

- [ ] Validate input against schema before execution
- [ ] Implement retry logic with exponential backoff
- [ ] Return structured error responses
- [ ] Log all tool executions
- [ ] Handle timeouts gracefully
- [ ] Implement rate limiting
- [ ] Provide clear error messages to users
- [ ] Include recovery suggestions

## Security Checklist

- [ ] Validate all inputs
- [ ] Require approval for dangerous operations
- [ ] Implement rate limiting
- [ ] Audit log all tool calls
- [ ] Use least-privilege access
- [ ] Sanitize outputs
- [ ] Never expose API keys in schemas
- [ ] Implement timeout limits

## Performance Optimization

1. **Caching**: Cache identical tool calls
2. **Deduplication**: Remove duplicate requests
3. **Parallel Execution**: Run independent tools simultaneously
4. **Right-size Models**: Use smaller models for simple tasks
5. **Streaming**: Stream responses for better UX
6. **Batch Processing**: Batch similar requests

## Common Pitfalls to Avoid

❌ **Weak descriptions** → LLM doesn't know when to use tool
❌ **Missing constraints** → Invalid parameters
❌ **Over-complex schemas** → API errors (400)
❌ **No validation** → Runtime errors
❌ **No error handling** → Poor UX
❌ **Synchronous blocking** → Slow performance
❌ **No testing** → Production failures
❌ **Missing rate limits** → API abuse

## Testing Strategy

1. **Unit Tests**: Individual tool functions
2. **Integration Tests**: Tool + LLM interaction
3. **Schema Validation**: All parameter combinations
4. **Error Cases**: Invalid inputs, timeouts, failures
5. **Performance Tests**: Latency, throughput
6. **Security Tests**: Input sanitization, permissions
7. **User Acceptance**: Real-world scenarios

## Monitoring Metrics

- **Success Rate**: % of successful tool calls
- **Latency**: P50, P95, P99 response times
- **Error Rate**: % of failed calls
- **Token Usage**: Cost tracking
- **Tool Usage**: Which tools are used most
- **User Satisfaction**: Feedback scores

## Decision Tree: Which Approach to Use?

```
Need multi-agent collaboration?
├─ Yes → Use A2A Protocol
└─ No → Need vendor portability?
    ├─ Yes → Use MCP
    └─ No → Committed to one vendor?
        ├─ OpenAI → Function Calling
        ├─ Anthropic → Tool Use API (or MCP)
        ├─ Google → Function Calling (auto mode)
        ├─ Microsoft → Product-specific APIs
        └─ AWS → Converse API
```

## 2025 Best Practices Summary

1. ✅ Use structured outputs for guaranteed schema compliance
2. ✅ Write detailed descriptions (they're instructions!)
3. ✅ Start with simple schemas, expand gradually
4. ✅ Version everything (tools, schemas, prompts)
5. ✅ Test extensively with real scenarios
6. ✅ Monitor performance and errors
7. ✅ Implement proper error handling
8. ✅ Use appropriate models (right-size)
9. ✅ Cache and optimize for performance
10. ✅ Prioritize security and safety

## Useful Commands

### Install SDKs
```bash
# OpenAI
pip install openai

# Anthropic
pip install anthropic

# Google Gemini
pip install google-generativeai

# MCP (Python)
pip install mcp

# MCP (TypeScript)
npm install @modelcontextprotocol/sdk
```

### Test Tool Schema
```python
from jsonschema import validate

schema = {...}  # Your schema
test_data = {...}  # Test input

try:
    validate(instance=test_data, schema=schema)
    print("✅ Valid")
except Exception as e:
    print(f"❌ Invalid: {e}")
```

## Further Reading Priority

**Start Here:**
1. OpenAI Function Calling Guide
2. Anthropic MCP Documentation
3. Your vendor's official docs

**Dive Deeper:**
4. JSON Schema specification
5. Design pattern guides
6. Best practices articles

**Advanced:**
7. Multi-agent orchestration
8. A2A protocol specification
9. Performance optimization

---

**Last Updated:** November 2025
**Quick Reference Version:** 1.0
