# Vendor Tool Approach Comparison

## High-Level Comparison Table

| Aspect | Anthropic | OpenAI | Google | Microsoft | AWS |
|--------|-----------|--------|--------|-----------|-----|
| **Approach** | Tool Use + MCP | Function Calling | Auto-conversion | Multiple APIs | Converse API |
| **Latest Feature** | Structured Outputs | Strict mode | Gemini 3 auto | MCP support | Multi-provider |
| **Maturity** | Mature | Very mature | Evolving | Enterprise-ready | Stable |
| **Unique** | MCP standard | Parallel calls | Python auto-convert | M365 integration | Model-agnostic |
| **Best For** | Safety, structure | Ecosystem | Python-first | Enterprise | Multi-cloud |

## Detailed Comparisons

### Schema Definition Style

**Anthropic - Clean Separation:**
```python
{
    "name": "get_weather",
    "description": "...",
    "input_schema": {
        # JSON Schema here
    }
}
```
✅ Clear structure
✅ Easy to read
✅ Consistent naming

**OpenAI - Nested Structure:**
```python
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "...",
        "parameters": {
            # JSON Schema here
        }
    }
}
```
✅ Follows OpenAPI conventions
✅ Explicit type field
⚠️ More nesting

**Google - Auto or Manual:**
```python
# Option 1: Auto (Python function)
def get_weather(location: str) -> str:
    """Get weather"""
    pass

# Option 2: Manual (like others)
genai.protos.FunctionDeclaration(...)
```
✅ Python-first convenience
✅ Flexibility
⚠️ Two ways to do same thing

### Execution Model

**Anthropic:**
- Sequential by default
- Can request multiple tools
- Model decides order

**OpenAI:**
- Parallel execution supported
- `parallel_tool_calls=True`
- Significant performance gain

**Google:**
- Automatic execution optional
- `mode: AUTO` - model decides
- `mode: ANY` - must use tool
- `mode: NONE` - no tools

**AWS Bedrock:**
- Provider-dependent
- Unified interface
- Works across models

### Error Handling

**Anthropic:**
```python
# Tool results can indicate errors
{
    "type": "tool_result",
    "tool_use_id": "...",
    "content": "Error: Invalid location",
    "is_error": True
}
```

**OpenAI:**
```python
# Return error as string content
{
    "role": "tool",
    "tool_call_id": "...",
    "content": json.dumps({"error": "Invalid location"})
}
```

**Google:**
```python
# Exception in function bubbles up
genai.protos.FunctionResponse(
    name="...",
    response={"error": "Invalid location"}
)
```

### Structured Outputs

**Anthropic - Native (Nov 2025):**
```python
response = client.messages.create(
    response_format=WeatherSchema  # Pydantic model
)
# Guaranteed to match schema, zero parsing errors
```

**OpenAI - Strict Mode:**
```python
{
    "type": "function",
    "function": {
        "strict": True,  # Enable structured outputs
        "parameters": {...}
    }
}
# Guaranteed schema compliance
```

**Google - Not Yet:**
- No structured outputs guarantee
- Standard JSON parsing needed

## Performance Comparison

### Latency

**Local (Single Tool Call):**
- Anthropic: ~1-2s
- OpenAI: ~1-2s
- Google: ~1-2s
- Similar across vendors

**Parallel Execution:**
- OpenAI: Best (native parallel support)
- Anthropic: Good (can request multiple)
- Google: Manual orchestration

### Cost Efficiency

**Token Usage:**
- Tool definitions add to input tokens
- Large schemas impact cost
- MCP can reduce this (dynamic discovery)

**Optimization Strategies:**
1. Use concise descriptions
2. Minimal schema (only required fields)
3. Dynamic tool loading (MCP)
4. Batch operations when possible

## Developer Experience

### Documentation Quality

**Best:** OpenAI
- Comprehensive guides
- Many examples
- Active community

**Good:** Anthropic, Google
- Clear documentation
- Growing examples
- Responsive support

**Enterprise:** Microsoft
- Product-specific docs
- Enterprise focus
- Integration guides

### Ecosystem Maturity

**Most Mature:** OpenAI
- LangChain integration
- LlamaIndex support
- Huge community
- Many third-party tools

**Growing Fast:** Anthropic
- MCP adoption accelerating
- Claude Code integration
- Enterprise partnerships

**Established:** Google
- Google Cloud integration
- Vertex AI platform
- Firebase extensions

## Vendor Lock-In Considerations

### Portability

**Most Portable:** MCP (Anthropic's standard)
- Open protocol
- Vendor-agnostic
- Growing adoption (OpenAI, Google)

**Least Portable:** Vendor-specific function calling
- Different schemas per vendor
- Custom code required
- Migration effort

### Mitigation Strategy

**Use abstraction layer:**
```python
class UniversalToolExecutor:
    def to_anthropic_schema(self, tool): ...
    def to_openai_schema(self, tool): ...
    def to_google_schema(self, tool): ...

    def execute(self, vendor, tool, args): ...
```

**Or use MCP:**
- Build tools once
- Works everywhere
- Future-proof

## Recommendations by Use Case

### Startup / Rapid Development
**Choose:** OpenAI
- Fastest to production
- Best documentation
- Largest ecosystem

### Enterprise / Compliance
**Choose:** Anthropic or Microsoft
- Strong safety features
- Structured outputs
- Enterprise support
- Microsoft for M365 integration

### Python-First Teams
**Choose:** Google Gemini
- Auto-function conversion
- Pythonic API
- Great for data science

### Multi-Cloud / Flexibility
**Choose:** AWS Bedrock + MCP
- Provider agnostic
- AWS infrastructure
- Model flexibility

### Long-Term Investment
**Choose:** MCP-based approach
- Open standard
- Cross-vendor support
- Future-proof

## Migration Paths

### From OpenAI to Anthropic:
```python
# OpenAI
tools = [{"type": "function", "function": {...}}]

# Anthropic equivalent
tools = [{...}]  # Remove "type" and "function" wrapper
```

### From Anthropic to MCP:
```python
# Anthropic Tool Use
tools = [{"name": "...", "input_schema": {...}}]

# MCP Server
@server.tool()
def my_tool(...): ...
```

### From Any Vendor to MCP:
Build MCP server → Works with all vendors

## Summary

**For most projects:** Start with your primary LLM provider's native approach

**For portability:** Use MCP from the beginning

**For maximum reach:** Build MCP servers that work everywhere

**For existing code:** Abstract vendor differences behind a common interface

The industry is converging on standards (MCP, A2A), making vendor choice less critical over time.
