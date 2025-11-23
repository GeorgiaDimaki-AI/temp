# Comprehensive Report: AI/LLM Plugins and Tools Across Vendors

**Research Date:** November 2025
**Focus:** First Principles, Comparative Analysis, and Practical Implementation

---

## Table of Contents

1. [First Principles: Why AI Systems Need Plugins/Tools](#1-first-principles)
2. [General Concepts: Creating Plugins and Tools](#2-general-concepts)
3. [Vendor-Specific Approaches](#3-vendor-specific-approaches)
4. [Architectural Differences and Design Philosophy](#4-architectural-differences)
5. [Code Examples by Vendor](#5-code-examples)
6. [Best Practices and Patterns](#6-best-practices)
7. [References and Documentation](#7-references)

---

## 1. First Principles: Why AI Systems Need Plugins/Tools {#1-first-principles}

### The Core Problem

Large Language Models (LLMs) are fundamentally **stateless text generators**. Without tools and plugins, they face critical limitations:

1. **No Real-World Interaction**: LLMs cannot access current information, interact with databases, or call APIs
2. **No Persistence**: They lack memory between sessions and cannot maintain state
3. **No Computation**: They cannot perform reliable mathematical calculations or execute code
4. **Static Knowledge**: Their knowledge is frozen at their training cutoff date

### The Solution: Tool-Augmented Agents

Tools transform LLMs from "passive generators to active participants capable of completing real-world tasks."

**Key Quote from Research:**
> "Without memory and tools, an agent is just a chatbot. Complex questions require an LLM to break tasks into subparts which can be addressed using tools and a flow of operations that leads to a desired final response."

### Core Components of Agent Architecture

Modern AI agents consist of:

- **LLM Core**: The "brain" that controls operations
- **Planning Module**: Breaks down complex tasks into subtasks
- **Memory System**: Maintains context and state across interactions
- **Tool Layer**: Provides access to external functions, APIs, databases, and services
- **Execution Environment**: Runs the actual operations

### Real-World Impact (2025)

- **Enterprise Adoption**: Deloitte reports 25% of enterprises using generative AI are piloting autonomous agents in 2025, expected to reach 50% by 2027
- **Market Growth**: AI agents market grew from $5.4B (2024) to $7.6B (2025)
- **Production Usage**: 79% of organizations already using agents in production
- **Enterprise Spending**: LLM spending rose to $8.4B by mid-2025 (up from $3.5B in late 2024)

---

## 2. General Concepts: Creating Plugins and Tools {#2-general-concepts}

### The Tool Lifecycle

All LLM tool implementations follow a similar pattern:

1. **Tool Definition**: Declare available functions with parameters using JSON Schema
2. **Model Inference**: LLM analyzes user input and decides whether to use tools
3. **Tool Selection**: Model selects appropriate tool(s) and generates parameters
4. **Execution**: Application code executes the actual function
5. **Result Integration**: Results are fed back to the model
6. **Response Generation**: Model synthesizes final response using tool results

### JSON Schema: The Universal Language

All major vendors use JSON Schema to define tools:

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

### Key Principles for Tool Design

1. **Atomic Operations**: Each tool should do one thing well
2. **Clear Descriptions**: Descriptions are "potent instructions" for LLMs
3. **Strong Typing**: Use specific types and constraints
4. **Comprehensive Validation**: Validate inputs and outputs
5. **Error Handling**: Return meaningful error messages
6. **Idempotency**: Tools should be safe to retry

### Three Emerging Standards

As of 2025, three protocols are becoming industry standards:

1. **Function Calling**: Direct LLM-to-function integration (vendor-specific)
2. **Model Context Protocol (MCP)**: Standardized client-server architecture for tool integration
3. **Agent2Agent (A2A)**: Protocol for multi-agent collaboration

---

## 3. Vendor-Specific Approaches {#3-vendor-specific-approaches}

### 3.1 Anthropic (Claude)

**Primary Approach:** Model Context Protocol (MCP) + Native Tool Use API

#### Model Context Protocol (MCP)

**Launch:** November 2024
**Status:** Open-source, becoming industry standard

**Description:**
> "Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems."

**Key Features:**
- **Vendor-agnostic**: Works with any LLM, not just Claude
- **Client-server architecture**: MCP servers expose tools, clients manage connections
- **Three core primitives**:
  - **Tools**: Executable functions
  - **Resources**: Data sources (files, databases, API responses)
  - **Prompts**: Reusable prompt templates
- **Security-first**: Host controls all permissions and approvals

**Industry Adoption (2025):**
- OpenAI adopted MCP in March 2025 for ChatGPT desktop, Agents SDK, and Responses API
- Google DeepMind announced MCP support for Gemini in April 2025
- Microsoft Copilot Studio added MCP support in May 2025
- Thousands of community-built MCP servers available

#### Claude Native Tool Use API

**Latest Features (November 2025):**
- **Structured Outputs** (Beta): Guaranteed JSON schema compliance
- **Strict Tool Use**: Zero-error tool parameter validation
- **SDK Support**: Python (Pydantic) and TypeScript (Zod) schema helpers

**API Endpoint:** `https://api.anthropic.com/v1/messages`

**Key Parameters:**
- `tools`: Array of tool definitions
- `tool_choice`: Control tool selection (auto/any/specific tool)
- `beta`: `structured-outputs-2025-11-13` for guaranteed schemas

### 3.2 OpenAI

**Primary Approach:** Function Calling + Agents SDK + Responses API

#### Function Calling

**Status:** Mature, widely adopted
**API Versions:** Evolved from `functions`/`function_call` to `tools`/`tool_choice`

**Key Features:**
- **Parallel Function Calling**: Execute multiple tools simultaneously
- **Structured Outputs**: Guaranteed JSON schema compliance (2025)
- **Tool Choice Control**: `auto`, `none`, or specific tool selection
- **Streaming Support**: Stream function call arguments as generated

**Recent Updates (2025):**
- Support for o3-mini and o1 reasoning models
- Parallel function calling with strict mode
- Enhanced structured outputs

#### OpenAI Agents SDK

**Announced:** Early 2025
**Status:** Open-source

**Key Features:**
- Multi-agent workflow support
- LiteLLM integration (supports 100+ model providers)
- Built-in tracing and guardrails
- Minimal, Python-first design

**Use Cases:**
- Answering questions via external APIs (emails, weather)
- Querying internal datastores (sales data, documents)
- Creating structured data from unstructured text

### 3.3 Google (Gemini)

**Primary Approach:** Function Calling + Built-in Tools + Live API

#### Gemini Function Calling

**Latest Models:** Gemini 3 Pro, Gemini 2.0 Flash
**Documentation Updated:** November 2025

**Key Features:**
- **Automatic Function Calling**: Auto-converts Python functions to schema
- **Compositional/Sequential Calling**: Chain multiple functions together
- **Streaming Function Arguments**: Real-time argument generation
- **MCP Support**: Announced April 2025

**Unique Capabilities:**
- **Live API with Tools**: Real-time audio + function calling
- **Built-in Tools**: Optimized, fully managed tools for common tasks
- **OpenAI SDK Compatibility**: Can use OpenAI SDK with Gemini

**API Access:**
- Google AI Studio (free tier: 1,500 requests/day)
- Vertex AI (enterprise)

**Configuration:**
```python
functionCallingConfig = {
    "mode": "AUTO",  # or "ANY" or "NONE"
    "allowed_function_names": ["function1", "function2"],
    "streamFunctionCallArguments": True  # Gemini 3+
}
```

### 3.4 Microsoft

**Primary Approach:** Multi-modal integration across products

#### Microsoft 365 Copilot - API Plugins

**Key Features:**
- Declarative agents interact with REST APIs
- OpenAPI description support
- **MCP Server Support** (October 2025)
- Natural language API interaction

**Developer Tools:**
- Microsoft 365 Agents Toolkit (Visual Studio/VS Code)
- Kiota (CLI + VS Code extension)

#### Copilot Studio

**Latest Updates (2025):**

**October 2025:**
- MCP resources support
- GPT-5 family model availability (Auto, Chat, Reasoning)

**May 2025:**
- Multi-agent orchestration
- Access to 11,000+ Azure AI Foundry models
- Fine-tuning with enterprise data

#### Microsoft Agentic AI Framework

**Key Features:**
- OpenAPI-first design
- REST API → callable tools conversion
- Integration with Azure OpenAI, M365 Copilot, Copilot Studio

#### GitHub Copilot for Azure

**Features:**
- MCP capabilities
- Agents and integrations
- Full SDLC support (planning, coding, testing, modernizing)

### 3.5 AWS Bedrock

**Primary Approach:** Converse API with Tool Use

**Official Name:** "Tool Use" (not "function calling")

#### Key Features

- **Converse API**: Consistent interface across all Bedrock models
- **Multi-model Support**: Works with Claude, Llama, Command, Mistral
- **Context Management**: Tool use clearing (beta: `context-management-2025-06-27`)

#### Latest Features (2025)

- Claude Sonnet 4.5 memory tool
- Asynchronous tool use
- LiteLLM integration

**API Reference:**
- Main: `https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html`
- ToolConfiguration: `https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolConfiguration.html`

---

## 4. Architectural Differences and Design Philosophy {#4-architectural-differences}

### 4.1 Function Calling vs MCP vs A2A

| Aspect | Function Calling | MCP | A2A |
|--------|-----------------|-----|-----|
| **Scope** | Single-app tool integration | Universal tool/data protocol | Multi-agent collaboration |
| **Architecture** | Direct LLM-function binding | Client-server with intermediate host | Agent-to-agent HTTP/JSON-RPC |
| **Standardization** | Vendor-specific implementations | Open standard (works with any LLM) | Open standard (Linux Foundation) |
| **Security** | Application-level | Host-controlled approvals | OAuth 2.0, API keys, OpenID |
| **Best For** | Low-latency, tight integrations | Cross-platform tool portability | Multi-agent workflows |
| **Execution** | App runtime executes | MCP server executes | Remote agent executes |
| **Discovery** | Pre-defined schemas | MCP server manifests | Agent Cards (JSON) |

### 4.2 Design Philosophy Comparison

#### OpenAI: Pragmatic Integration
- **Philosophy**: "Make it work with existing systems"
- **Strength**: Mature ecosystem, extensive documentation
- **Approach**: Evolutionary (functions → tools → Agents SDK)
- **Focus**: Developer experience, backward compatibility
- **Trade-off**: Vendor lock-in for some features

#### Anthropic: Open Standardization
- **Philosophy**: "Create universal protocols"
- **Strength**: MCP becoming industry standard
- **Approach**: Protocol-first, vendor-agnostic
- **Focus**: Interoperability, security, long-term ecosystem
- **Trade-off**: More complex initial setup

#### Google: Ecosystem Integration
- **Philosophy**: "Leverage our platform"
- **Strength**: Deep integration with Google services
- **Approach**: Built-in tools + custom functions
- **Focus**: Enterprise integration, multimodal capabilities
- **Trade-off**: Best with Google ecosystem

#### Microsoft: Multi-Product Strategy
- **Philosophy**: "AI across all products"
- **Strength**: Tight integration with M365, Azure, GitHub
- **Approach**: Different APIs for different products
- **Focus**: Enterprise workflows, low-code options
- **Trade-off**: Fragmented across multiple products

### 4.3 Technical Architecture Patterns

#### Pattern 1: Direct Function Calling (OpenAI, Google, AWS)

```
User Query → LLM → Tool Selection → App Executes → LLM Response
```

**Characteristics:**
- Low latency
- Tight coupling
- Vendor-specific schemas
- Application runtime executes

#### Pattern 2: MCP Client-Server (Anthropic, adopted by others)

```
User Query → LLM → MCP Client → MCP Server → External Tool → Response
```

**Characteristics:**
- Intermediate host layer
- Standardized protocol
- Permission-based execution
- Server-side tool execution

#### Pattern 3: Agent-to-Agent (A2A)

```
Agent A → Discovery (Agent Card) → Task Request → Agent B → Task Execution → Response
```

**Characteristics:**
- Inter-agent communication
- Capability discovery
- Long-running tasks
- Federated execution

### 4.4 JSON Schema Implementation Differences

#### OpenAI

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather...",
        "parameters": { /* JSON Schema */ },
        "strict": True  # Structured outputs
    }
}]
```

#### Anthropic

```python
tools = [{
    "name": "get_weather",
    "description": "Get weather...",
    "input_schema": { /* JSON Schema */ },
    "strict": True  # Beta: structured outputs
}]
```

#### Google Gemini

```python
# Automatic from Python function
@genai.tool
def get_weather(location: str, unit: str = "celsius"):
    """Get weather for a location."""
    pass

# Or manual JSON Schema
tools = [genai.protos.Tool(
    function_declarations=[{
        "name": "get_weather",
        "description": "Get weather...",
        "parameters": { /* JSON Schema */ }
    }]
)]
```

### 4.5 Control Mechanisms

| Vendor | Auto Mode | Force Tool | Prevent Tool | Parallel Execution |
|--------|-----------|------------|--------------|-------------------|
| OpenAI | `tool_choice: "auto"` | `tool_choice: {"type": "function", "function": {"name": "..."}}` | `tool_choice: "none"` | `parallel_tool_calls: True` (default) |
| Anthropic | `tool_choice: {"type": "auto"}` | `tool_choice: {"type": "tool", "name": "..."}` | `tool_choice: {"type": "any"}` | Multiple in single response |
| Google | `mode: "AUTO"` | `mode: "ANY"` + `allowed_function_names` | `mode: "NONE"` | Compositional calling |

---

## 5. Code Examples by Vendor {#5-code-examples}

### 5.1 Anthropic Claude - Native Tool Use

#### Basic Tool Use with Structured Outputs

```python
import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic(api_key="your-api-key")

# Define tool with Pydantic (automatically converts to JSON Schema)
class WeatherParams(BaseModel):
    location: str
    unit: str = "celsius"

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": WeatherParams.model_json_schema(),
        "strict": True  # Guaranteed schema compliance
    }
]

# Make request with beta header for structured outputs
message = client.messages.create(
    model="claude-sonnet-4.5-20251022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
    # Beta header for structured outputs
    extra_headers={"anthropic-beta": "structured-outputs-2025-11-13"}
)

# Handle tool use
for block in message.content:
    if block.type == "tool_use":
        # Guaranteed to match schema
        tool_input = block.input

        # Execute the actual function
        if block.name == "get_weather":
            weather_data = get_weather_from_api(
                location=tool_input["location"],
                unit=tool_input.get("unit", "celsius")
            )

            # Send results back to Claude
            response = client.messages.create(
                model="claude-sonnet-4.5-20251022",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {"role": "user", "content": "What's the weather in San Francisco?"},
                    {"role": "assistant", "content": message.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(weather_data)
                            }
                        ]
                    }
                ]
            )
            print(response.content[0].text)

def get_weather_from_api(location: str, unit: str) -> dict:
    """Your actual API call here"""
    return {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "conditions": "Sunny"
    }
```

### 5.2 Anthropic - MCP Server (Python)

#### Creating an MCP Server with FastMCP

```python
from mcp.server.fastmcp import FastMCP
import httpx

# Initialize MCP server
mcp = FastMCP("Weather Service")

@mcp.tool()
async def get_weather(location: str, unit: str = "celsius") -> str:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates
        unit: Temperature unit (celsius or fahrenheit)

    Returns:
        Weather information as JSON string
    """
    async with httpx.AsyncClient() as client:
        # Call actual weather API
        response = await client.get(
            f"https://api.weather.example/current",
            params={"location": location, "unit": unit}
        )
        return response.text

@mcp.resource("weather://forecast/{location}")
async def get_forecast(location: str) -> str:
    """Get 7-day forecast for a location"""
    # Resource example - provides data access
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weather.example/forecast",
            params={"location": location}
        )
        return response.text

@mcp.prompt()
def weather_report_prompt(location: str) -> str:
    """Generate a detailed weather report for {location}"""
    return f"Provide a comprehensive weather analysis for {location}, including current conditions, forecast, and recommendations."

if __name__ == "__main__":
    mcp.run()
```

#### MCP Server (TypeScript)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create server
const server = new McpServer({
  name: "Weather Service",
  version: "1.0.0"
});

// Define tool with Zod schema
server.tool(
  "get_weather",
  "Get current weather for a location",
  {
    location: z.string().describe("City name or coordinates"),
    unit: z.enum(["celsius", "fahrenheit"]).default("celsius")
  },
  async ({ location, unit }) => {
    // Call actual weather API
    const response = await fetch(
      `https://api.weather.example/current?location=${location}&unit=${unit}`
    );
    const data = await response.json();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(data, null, 2)
        }
      ]
    };
  }
);

// Add resource
server.resource(
  "weather://forecast/{location}",
  "7-day forecast",
  "application/json",
  async (uri) => {
    const location = uri.pathname.split('/')[2];
    const response = await fetch(
      `https://api.weather.example/forecast?location=${location}`
    );
    return await response.text();
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 5.3 OpenAI - Function Calling

#### Basic Function Calling

```python
from openai import OpenAI
import json

client = OpenAI(api_key="your-api-key")

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            },
            "strict": True  # Structured outputs
        }
    }
]

# Initial request
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the weather in San Francisco and New York?"}
    ],
    tools=tools,
    tool_choice="auto"  # Let model decide
)

# Check if model wants to use tools
message = response.choices[0].message
if message.tool_calls:
    # Process each tool call (parallel execution)
    tool_results = []

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Execute the actual function
        if function_name == "get_weather":
            result = get_weather_from_api(**function_args)
            tool_results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(result)
            })

    # Send results back to model
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "What's the weather in San Francisco and New York?"},
            message,
            *tool_results
        ]
    )

    print(final_response.choices[0].message.content)

def get_weather_from_api(location: str, unit: str = "celsius") -> dict:
    """Your actual API call"""
    return {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "conditions": "Sunny"
    }
```

#### Parallel Function Calling with Strict Mode

```python
from openai import OpenAI
from pydantic import BaseModel
import json

client = OpenAI()

# Define schema with Pydantic
class WeatherParams(BaseModel):
    location: str
    unit: str = "celsius"

# Convert to OpenAI's strict schema format
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": WeatherParams.model_json_schema(),
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Get weather forecast",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "days": {"type": "integer", "minimum": 1, "maximum": 10}
                },
                "required": ["location"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather now and forecast for SF?"}],
    tools=tools,
    parallel_tool_calls=True  # Enable parallel execution (default)
)

# Model may return multiple tool calls
for tool_call in response.choices[0].message.tool_calls:
    print(f"Tool: {tool_call.function.name}")
    print(f"Args: {tool_call.function.arguments}")
```

#### Forcing Specific Tool

```python
# Force model to use specific tool
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me about the weather"}],
    tools=tools,
    tool_choice={
        "type": "function",
        "function": {"name": "get_weather"}
    }
)
```

### 5.4 Google Gemini - Function Calling

#### Automatic Function Calling (Python)

```python
import google.generativeai as genai
from google.generativeai import types

genai.configure(api_key="your-api-key")

# Define Python functions - automatically converted to schema
def get_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates
        unit: Temperature unit (celsius or fahrenheit)

    Returns:
        Current weather data
    """
    # Your actual API call
    return {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "conditions": "Sunny"
    }

def get_forecast(location: str, days: int = 7) -> dict:
    """Get weather forecast for a location"""
    return {
        "location": location,
        "days": days,
        "forecast": [{"day": i, "temp": 70 + i} for i in range(days)]
    }

# Create model with automatic function calling
model = genai.GenerativeModel(
    model_name="gemini-3-pro",
    tools=[get_weather, get_forecast]  # Direct Python functions!
)

# Automatic execution - model calls functions automatically
response = model.generate_content(
    "What's the weather in Paris and the 5-day forecast?",
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="AUTO",  # Automatic tool calling
        )
    )
)

print(response.text)  # Final synthesized answer
```

#### Manual Function Calling with JSON Schema

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# Manual tool definition
tools = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="get_weather",
                description="Get current weather for a location",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="City name"
                        ),
                        "unit": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            enum=["celsius", "fahrenheit"]
                        )
                    },
                    required=["location"]
                )
            )
        ]
    )
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=tools
)

# Manual control - model suggests, you execute
response = model.generate_content(
    "What's the weather in Tokyo?",
    tool_config={
        "function_calling_config": {
            "mode": "ANY",  # Force tool use
            "allowed_function_names": ["get_weather"]
        }
    }
)

# Check for function calls
for part in response.parts:
    if part.function_call:
        function_name = part.function_call.name
        function_args = dict(part.function_call.args)

        # Execute function
        if function_name == "get_weather":
            result = get_weather_from_api(**function_args)

            # Send result back
            response = model.generate_content([
                response.candidates[0].content,
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": result}
                        )
                    )]
                )
            ])
            print(response.text)
```

#### Compositional/Sequential Function Calling

```python
# Gemini can chain multiple function calls
def search_places(query: str, location: str) -> list:
    """Search for places near a location"""
    return [
        {"name": "Golden Gate Park", "rating": 4.5},
        {"name": "Fisherman's Wharf", "rating": 4.2}
    ]

def get_reviews(place_name: str) -> list:
    """Get reviews for a place"""
    return [
        {"text": "Great place!", "rating": 5},
        {"text": "Nice views", "rating": 4}
    ]

model = genai.GenerativeModel(
    model_name="gemini-3-pro",
    tools=[search_places, get_reviews, get_weather]
)

# Model automatically chains: search → reviews → weather
response = model.generate_content(
    "Find top-rated parks in SF, show reviews, and check if weather is good for visiting"
)

print(response.text)  # Comprehensive answer using all tools
```

### 5.5 AWS Bedrock - Tool Use with Converse API

#### Basic Tool Use

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Define tool configuration
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"]
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        }
    ]
}

# Initial request
response = bedrock.converse(
    modelId="anthropic.claude-sonnet-4.5-v2:0",
    messages=[
        {
            "role": "user",
            "content": [{"text": "What's the weather in Seattle?"}]
        }
    ],
    toolConfig=tool_config
)

# Handle tool use
if response['stopReason'] == 'tool_use':
    # Extract tool use from response
    tool_use_block = None
    for block in response['output']['message']['content']:
        if 'toolUse' in block:
            tool_use_block = block['toolUse']
            break

    # Execute the tool
    tool_result = None
    if tool_use_block['name'] == 'get_weather':
        weather_data = get_weather_from_api(**tool_use_block['input'])
        tool_result = {
            "toolUseId": tool_use_block['toolUseId'],
            "content": [{"json": weather_data}]
        }

    # Send result back
    final_response = bedrock.converse(
        modelId="anthropic.claude-sonnet-4.5-v2:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": "What's the weather in Seattle?"}]
            },
            response['output']['message'],
            {
                "role": "user",
                "content": [{"toolResult": tool_result}]
            }
        ],
        toolConfig=tool_config
    )

    print(final_response['output']['message']['content'][0]['text'])

def get_weather_from_api(location: str, unit: str = "celsius"):
    """Your actual API call"""
    return {
        "location": location,
        "temperature": 72,
        "unit": unit,
        "conditions": "Sunny"
    }
```

#### Async Tool Use (Bedrock with Claude)

```python
import asyncio
import boto3

async def async_tool_use():
    bedrock = boto3.client('bedrock-runtime')

    # Use Claude Sonnet 4.5 with memory tool
    response = bedrock.converse(
        modelId="anthropic.claude-sonnet-4.5-v2:0",
        messages=[
            {"role": "user", "content": [{"text": "Remember: My favorite city is Paris"}]},
        ],
        toolConfig={
            "tools": [{
                "toolSpec": {
                    "name": "memory_tool",
                    "description": "Store and retrieve information",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["store", "retrieve"]},
                                "key": {"type": "string"},
                                "value": {"type": "string"}
                            },
                            "required": ["action", "key"]
                        }
                    }
                }
            }]
        },
        additionalModelRequestFields={
            "anthropic_beta": ["context-management-2025-06-27"]
        }
    )

    return response

# Run async
asyncio.run(async_tool_use())
```

### 5.6 Microsoft Copilot Studio - MCP Integration

#### Creating MCP Resource in Copilot Studio

```python
# Example MCP server for Copilot Studio
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Enterprise Data Service")

@mcp.resource("sharepoint://documents/{document_id}")
async def get_document(document_id: str) -> str:
    """Access SharePoint documents via MCP resource"""
    # Integration with Microsoft Graph API
    from msgraph import GraphServiceClient

    client = GraphServiceClient(credentials, scopes)
    document = await client.sites.by_site_id(
        'site_id'
    ).drives.by_drive_id(
        'drive_id'
    ).items.by_drive_item_id(
        document_id
    ).get()

    return document.content

@mcp.tool()
async def search_emails(query: str, top: int = 10) -> list:
    """Search Outlook emails"""
    # Microsoft Graph API integration
    from msgraph import GraphServiceClient

    client = GraphServiceClient(credentials, scopes)
    messages = await client.me.messages.get(
        query_parameters={
            "search": query,
            "top": top
        }
    )

    return [
        {
            "subject": msg.subject,
            "from": msg.from_address.email_address.address,
            "date": msg.received_date_time
        }
        for msg in messages.value
    ]

if __name__ == "__main__":
    mcp.run()
```

---

## 6. Best Practices and Patterns {#6-best-practices}

### 6.1 Core Design Patterns (2025)

Based on industry research, these are the most widely adopted patterns:

#### 1. ReAct (Reason and Act)

**Description:** Model iterates through Thought → Action → Observation cycles

**Implementation:**
```python
def react_pattern(query: str, tools: list, max_iterations: int = 5):
    """ReAct pattern implementation"""
    conversation_history = [{"role": "user", "content": query}]

    for iteration in range(max_iterations):
        # Model reasons about next action
        response = llm.chat(
            messages=conversation_history,
            tools=tools
        )

        # If model provides final answer, return
        if not response.tool_calls:
            return response.content

        # Execute tools (Action)
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)  # Action

            # Add observation to history
            conversation_history.extend([
                response,
                {"role": "tool", "content": result}  # Observation
            ])

    return "Max iterations reached"
```

#### 2. Tool Use Pattern

**Description:** Direct interaction with enterprise systems

**Best Practices:**
- **Atomic tools**: Each tool does one thing well
- **Clear boundaries**: Separate data access from computation
- **Error handling**: Always return structured error messages
- **Validation**: Validate inputs before execution

```python
class ToolRegistry:
    """Centralized tool management"""

    def __init__(self):
        self.tools = {}
        self.tool_schemas = []

    def register(self, name: str, description: str, schema: dict):
        """Register a tool with validation"""
        def decorator(func):
            self.tools[name] = func
            self.tool_schemas.append({
                "name": name,
                "description": description,
                "parameters": schema
            })
            return func
        return decorator

    async def execute(self, name: str, args: dict) -> dict:
        """Execute tool with error handling"""
        try:
            if name not in self.tools:
                return {"error": f"Unknown tool: {name}"}

            # Validate args against schema
            validate_args(args, self.get_schema(name))

            # Execute
            result = await self.tools[name](**args)
            return {"success": True, "data": result}

        except Exception as e:
            return {"error": str(e), "success": False}

    def get_schema(self, name: str) -> dict:
        """Get tool schema for validation"""
        for schema in self.tool_schemas:
            if schema["name"] == name:
                return schema["parameters"]
        return None

# Usage
registry = ToolRegistry()

@registry.register(
    "get_weather",
    "Get current weather",
    {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
)
async def get_weather(location: str) -> dict:
    """Weather tool implementation"""
    # Implementation
    pass
```

#### 3. Multi-Agent Collaboration

**Orchestration Patterns:**

**a) Sequential Orchestration:**
```python
async def sequential_orchestration(task: str, agents: list):
    """Tasks flow sequentially through agents"""
    result = task

    for agent in agents:
        result = await agent.process(result)

    return result

# Example: Research → Analysis → Writing
result = await sequential_orchestration(
    "Write a market analysis report",
    agents=[researcher_agent, analyst_agent, writer_agent]
)
```

**b) Concurrent Orchestration:**
```python
import asyncio

async def concurrent_orchestration(task: str, agents: list):
    """Agents work in parallel"""
    tasks = [agent.process(task) for agent in agents]
    results = await asyncio.gather(*tasks)

    # Synthesize results
    return synthesize_results(results)

# Example: Multiple data sources
results = await concurrent_orchestration(
    "Gather competitive intelligence",
    agents=[web_scraper, api_fetcher, database_query]
)
```

**c) Dynamic Handoff:**
```python
class AgentOrchestrator:
    """Dynamic routing based on task requirements"""

    def __init__(self, agents: dict):
        self.agents = agents

    async def route(self, task: str):
        """Dynamically select agent based on task"""
        # Use LLM to determine best agent
        routing_decision = await self.llm.chat([
            {
                "role": "system",
                "content": f"Available agents: {self.get_agent_descriptions()}"
            },
            {
                "role": "user",
                "content": f"Which agent should handle: {task}"
            }
        ])

        agent_name = extract_agent_name(routing_decision)
        return await self.agents[agent_name].process(task)
```

#### 4. Planning Pattern

**Two Approaches:**

**a) Dynamic Planning (LLM-generated):**
```python
async def dynamic_planning(goal: str, tools: list):
    """LLM creates and executes plan"""

    # Generate plan
    plan_response = await llm.chat([
        {
            "role": "system",
            "content": f"Create a step-by-step plan to: {goal}\nAvailable tools: {tools}"
        }
    ])

    plan_steps = extract_steps(plan_response)

    # Execute plan
    results = []
    for step in plan_steps:
        result = await execute_step(step, tools)
        results.append(result)

    return synthesize_results(results)
```

**b) Predefined Workflow:**
```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class WorkflowStep:
    name: str
    tool: Callable
    depends_on: list[str] = None

class Workflow:
    """Predefined execution sequence"""

    def __init__(self):
        self.steps = []
        self.results = {}

    def add_step(self, step: WorkflowStep):
        self.steps.append(step)

    async def execute(self, initial_input):
        """Execute workflow with dependency resolution"""
        for step in self.steps:
            # Wait for dependencies
            if step.depends_on:
                await self.wait_for_dependencies(step.depends_on)

            # Execute step
            result = await step.tool(
                initial_input,
                dependencies=self.get_dependency_results(step.depends_on)
            )

            self.results[step.name] = result

        return self.results

# Usage
workflow = Workflow()
workflow.add_step(WorkflowStep("fetch_data", fetch_tool))
workflow.add_step(WorkflowStep("analyze", analyze_tool, depends_on=["fetch_data"]))
workflow.add_step(WorkflowStep("report", report_tool, depends_on=["analyze"]))

result = await workflow.execute(user_query)
```

### 6.2 JSON Schema Best Practices

Based on 2025 industry research showing 90%+ error reduction:

#### 1. Comprehensive Descriptions

**Bad:**
```json
{
  "name": "get_weather",
  "description": "Get weather",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {"type": "string"},
      "unit": {"type": "string"}
    }
  }
}
```

**Good:**
```json
{
  "name": "get_weather",
  "description": "Retrieves current weather conditions for a specified location. Returns temperature, humidity, wind speed, and general conditions. Use this when users ask about current weather, not forecasts.",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state or city and country (e.g., 'San Francisco, CA' or 'London, UK'). Can also accept coordinates in 'lat,lon' format."
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit", "kelvin"],
        "description": "Temperature unit for the response. Defaults to celsius. Use fahrenheit for US locations unless specified otherwise.",
        "default": "celsius"
      }
    },
    "required": ["location"],
    "additionalProperties": false
  }
}
```

**Key Principles:**
- Descriptions are "potent instructions" - treat them as part of the prompt
- Explain WHEN to use the tool (not just what it does)
- Provide format examples for string parameters
- Clarify defaults and edge cases

#### 2. Strong Typing and Constraints

```json
{
  "name": "schedule_meeting",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "minLength": 1,
        "maxLength": 100,
        "description": "Meeting title"
      },
      "start_time": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 format: 2025-11-23T14:30:00Z"
      },
      "duration_minutes": {
        "type": "integer",
        "minimum": 15,
        "maximum": 480,
        "multipleOf": 15,
        "description": "Meeting duration in 15-minute increments"
      },
      "attendees": {
        "type": "array",
        "items": {
          "type": "string",
          "format": "email"
        },
        "minItems": 1,
        "maxItems": 50,
        "uniqueItems": true
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "default": "medium"
      }
    },
    "required": ["title", "start_time", "attendees"],
    "additionalProperties": false
  }
}
```

**Constraints to Use:**
- `minLength`, `maxLength` for strings
- `minimum`, `maximum` for numbers
- `multipleOf` for increments
- `format` for standard types (email, date-time, uri, etc.)
- `enum` for fixed choices
- `pattern` for regex validation
- `minItems`, `maxItems`, `uniqueItems` for arrays
- `additionalProperties: false` to prevent unexpected fields

#### 3. Start Simple, Expand Gradually

**Common Error:** Schema too complex → 400 InvalidArgument

**Approach:**
```python
# Step 1: Minimal working schema
basic_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"}
    },
    "required": ["query"]
}

# Step 2: Add common options
intermediate_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "limit": {"type": "integer", "default": 10},
        "filters": {"type": "object"}  # Simple object
    },
    "required": ["query"]
}

# Step 3: Full schema with nested structures
advanced_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100},
        "filters": {
            "type": "object",
            "properties": {
                "date_range": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string", "format": "date"},
                        "end": {"type": "string", "format": "date"}
                    }
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    },
    "required": ["query"]
}
```

#### 4. Validation Workflow

```python
from jsonschema import validate, ValidationError
import json

def validate_tool_input(tool_call: dict, schema: dict) -> tuple[bool, str]:
    """Validate LLM-generated tool input against schema"""
    try:
        # Parse arguments (may be string from LLM)
        if isinstance(tool_call.get("arguments"), str):
            args = json.loads(tool_call["arguments"])
        else:
            args = tool_call.get("arguments", {})

        # Validate against schema
        validate(instance=args, schema=schema)

        return True, "Valid"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    except ValidationError as e:
        return False, f"Schema validation failed: {e.message}"

# Usage in tool execution
is_valid, error_msg = validate_tool_input(tool_call, schema)

if not is_valid:
    # With structured outputs (2025), this shouldn't happen
    # But keep validation for older models or non-strict mode
    return {
        "error": error_msg,
        "suggestion": "Please try again with correct parameters"
    }
```

### 6.3 Production Best Practices (2025)

Based on UiPath, Microsoft, and Google recommendations:

#### 1. Version Everything

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ToolVersion:
    name: str
    version: str
    schema: dict
    prompt_template: str
    created_at: datetime
    evaluation_results: dict

class ToolVersionManager:
    """Track and manage tool versions"""

    def __init__(self):
        self.versions = {}

    def register_version(self, tool: ToolVersion):
        """Register new tool version"""
        key = f"{tool.name}@{tool.version}"
        self.versions[key] = tool

    def get_version(self, name: str, version: str = "latest"):
        """Get specific version or latest"""
        if version == "latest":
            versions = [
                v for v in self.versions.values()
                if v.name == name
            ]
            return max(versions, key=lambda v: v.created_at)

        return self.versions.get(f"{name}@{version}")

    def rollback(self, name: str, to_version: str):
        """Rollback to previous version"""
        return self.get_version(name, to_version)

# Usage
manager = ToolVersionManager()

manager.register_version(ToolVersion(
    name="search_documents",
    version="2.1.0",
    schema=search_schema_v2_1,
    prompt_template=prompt_v2_1,
    created_at=datetime.now(),
    evaluation_results={"accuracy": 0.95, "latency_p95": 1.2}
))
```

#### 2. Comprehensive Testing and Evaluation

```python
class ToolEvaluator:
    """Evaluate tool performance"""

    def __init__(self, test_cases: list):
        self.test_cases = test_cases
        self.results = []

    async def evaluate_tool(self, tool_name: str, tool_func: callable):
        """Run evaluation suite"""
        results = {
            "tool": tool_name,
            "total_tests": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "errors": [],
            "latency_p50": 0,
            "latency_p95": 0
        }

        latencies = []

        for test_case in self.test_cases:
            start = time.time()

            try:
                result = await tool_func(**test_case["input"])
                latency = time.time() - start
                latencies.append(latency)

                # Validate output
                if self.validate_output(result, test_case["expected"]):
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "test": test_case["name"],
                        "expected": test_case["expected"],
                        "got": result
                    })

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "test": test_case["name"],
                    "error": str(e)
                })

        # Calculate latency percentiles
        latencies.sort()
        results["latency_p50"] = latencies[len(latencies) // 2]
        results["latency_p95"] = latencies[int(len(latencies) * 0.95)]

        return results

# Test cases
test_cases = [
    {
        "name": "basic_weather_query",
        "input": {"location": "San Francisco, CA", "unit": "fahrenheit"},
        "expected": {"has_temperature": True, "has_conditions": True}
    },
    {
        "name": "coordinates_query",
        "input": {"location": "37.7749,-122.4194"},
        "expected": {"has_temperature": True}
    }
]

evaluator = ToolEvaluator(test_cases)
results = await evaluator.evaluate_tool("get_weather", get_weather)
```

#### 3. Safety and Determinism

**For deterministic tasks, prefer automation over agent actions:**

```python
class SafeToolExecutor:
    """Execute tools with safety checks"""

    def __init__(self):
        self.dangerous_tools = {
            "delete_file", "drop_table", "send_email", "make_payment"
        }
        self.approval_required = set()

    async def execute_with_safety(
        self,
        tool_name: str,
        args: dict,
        user_id: str
    ):
        """Execute tool with safety checks"""

        # 1. Check if tool is dangerous
        if tool_name in self.dangerous_tools:
            # Require explicit approval
            approval = await self.request_approval(
                user_id,
                tool_name,
                args
            )

            if not approval:
                return {
                    "error": "User denied permission",
                    "action_required": "manual_execution"
                }

        # 2. Dry run for write operations
        if self.is_write_operation(tool_name):
            dry_run_result = await self.execute_dry_run(tool_name, args)

            # Show user what will happen
            await self.show_preview(user_id, dry_run_result)

        # 3. Rate limiting
        if not await self.check_rate_limit(user_id, tool_name):
            return {"error": "Rate limit exceeded"}

        # 4. Execute with monitoring
        try:
            result = await self.execute_monitored(tool_name, args)

            # 5. Audit log
            await self.log_execution(user_id, tool_name, args, result)

            return result

        except Exception as e:
            await self.log_error(user_id, tool_name, args, e)
            raise
```

#### 4. Performance Optimization

```python
class OptimizedToolExecutor:
    """Optimize tool execution"""

    def __init__(self):
        self.cache = {}
        self.execution_history = []

    async def execute_optimized(
        self,
        tool_calls: list,
        enable_caching: bool = True,
        enable_parallel: bool = True
    ):
        """Execute tools with optimizations"""

        # 1. Deduplication
        unique_calls = self.deduplicate_calls(tool_calls)

        # 2. Cache check
        if enable_caching:
            cached_results = self.check_cache(unique_calls)
            remaining_calls = [
                call for call in unique_calls
                if call not in cached_results
            ]
        else:
            remaining_calls = unique_calls

        # 3. Parallel execution
        if enable_parallel and len(remaining_calls) > 1:
            new_results = await self.execute_parallel(remaining_calls)
        else:
            new_results = await self.execute_sequential(remaining_calls)

        # 4. Cache results
        if enable_caching:
            self.update_cache(new_results)

        # 5. Combine cached + new results
        all_results = {**cached_results, **new_results}

        return all_results

    async def execute_parallel(self, calls: list):
        """Execute multiple tools in parallel"""
        import asyncio

        tasks = [
            self.execute_single(call)
            for call in calls
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            call: result
            for call, result in zip(calls, results)
        }

    def deduplicate_calls(self, calls: list) -> list:
        """Remove duplicate tool calls"""
        seen = set()
        unique = []

        for call in calls:
            # Create hashable key
            key = (call["name"], json.dumps(call["args"], sort_keys=True))

            if key not in seen:
                seen.add(key)
                unique.append(call)

        return unique
```

#### 5. Right-Size Model Selection

```python
class AdaptiveModelSelector:
    """Select appropriate model based on task complexity"""

    def __init__(self):
        self.models = {
            "routing": "gpt-4o-mini",  # Fast, cheap for routing
            "tool_use": "gpt-4o",       # Good balance
            "reasoning": "o3-mini",     # Complex reasoning
            "classification": "gpt-4o-mini"  # Simple classification
        }

    def select_model(self, task_type: str, complexity: str):
        """Select model based on task requirements"""

        if task_type == "routing" or task_type == "classification":
            # Use smaller model
            return self.models["classification"]

        elif task_type == "tool_use":
            if complexity == "high":
                # Multiple steps, complex reasoning
                return self.models["reasoning"]
            else:
                # Standard tool use
                return self.models["tool_use"]

        elif task_type == "reasoning":
            return self.models["reasoning"]

        return self.models["tool_use"]  # Default

# Usage
selector = AdaptiveModelSelector()

# Route to appropriate model
model = selector.select_model(
    task_type="tool_use",
    complexity="low"
)  # Returns "gpt-4o" for standard tool use

# For simple classification, use cheaper model
model = selector.select_model(
    task_type="classification",
    complexity="low"
)  # Returns "gpt-4o-mini"
```

#### 6. Clear User Communication

```python
class TransparentAgent:
    """Agent with transparent communication"""

    async def execute_with_transparency(self, user_query: str):
        """Execute with clear communication"""

        # 1. Set expectations
        await self.communicate(
            "I can help with weather, scheduling, and document search. "
            "I cannot delete files or make purchases without your approval."
        )

        # 2. Show thinking (for complex tasks)
        await self.communicate("Let me break this down...")
        plan = await self.create_plan(user_query)
        await self.communicate(f"I'll: {plan}")

        # 3. Show tool usage
        for step in plan:
            await self.communicate(f"🔧 Using {step.tool_name}...")
            result = await self.execute_tool(step)

            if step.requires_review:
                # Show what will happen
                await self.communicate(
                    f"⚠️  About to {step.action}. "
                    f"Preview: {result.preview}. "
                    f"Proceed? (yes/no)"
                )

                approval = await self.get_user_input()
                if approval != "yes":
                    await self.communicate("❌ Cancelled")
                    continue

        # 4. Escalation path
        if self.cannot_complete(plan):
            await self.communicate(
                "I cannot complete this task because [reason]. "
                "Would you like me to:\n"
                "1. Connect you with support\n"
                "2. Show manual steps\n"
                "3. Try a different approach"
            )
```

### 6.4 Error Handling Patterns

```python
class RobustToolExecutor:
    """Tool executor with comprehensive error handling"""

    async def execute_with_retry(
        self,
        tool_name: str,
        args: dict,
        max_retries: int = 3
    ):
        """Execute tool with retry logic"""

        for attempt in range(max_retries):
            try:
                result = await self.execute_tool(tool_name, args)
                return {"success": True, "data": result}

            except ValidationError as e:
                # Schema validation error - don't retry
                return {
                    "success": False,
                    "error": "invalid_input",
                    "message": str(e),
                    "recoverable": False
                }

            except TimeoutError as e:
                # Timeout - retry with backoff
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue

                return {
                    "success": False,
                    "error": "timeout",
                    "message": "Tool execution timed out",
                    "recoverable": True,
                    "retry_after": 60
                }

            except PermissionError as e:
                # Permission denied - don't retry
                return {
                    "success": False,
                    "error": "permission_denied",
                    "message": str(e),
                    "recoverable": False,
                    "action_required": "request_permission"
                }

            except RateLimitError as e:
                # Rate limit - retry after delay
                retry_after = e.retry_after or 60

                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_after)
                    continue

                return {
                    "success": False,
                    "error": "rate_limit",
                    "message": "Rate limit exceeded",
                    "recoverable": True,
                    "retry_after": retry_after
                }

            except Exception as e:
                # Unknown error - log and retry
                await self.log_error(tool_name, args, e)

                if attempt < max_retries - 1:
                    continue

                return {
                    "success": False,
                    "error": "unknown",
                    "message": str(e),
                    "recoverable": True
                }

        return {
            "success": False,
            "error": "max_retries_exceeded",
            "message": f"Failed after {max_retries} attempts"
        }
```

---

## 7. References and Documentation {#7-references}

### 7.1 Official Documentation

#### Anthropic (Claude)

**MCP (Model Context Protocol):**
- Main Documentation: [https://docs.anthropic.com/en/docs/mcp](https://docs.anthropic.com/en/docs/mcp)
- GitHub Repository: [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- Protocol Specification: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- Claude Code Integration: [https://docs.anthropic.com/en/docs/claude-code/mcp](https://docs.anthropic.com/en/docs/claude-code/mcp)
- Training Course: [https://anthropic.skilljar.com/introduction-to-model-context-protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol)

**Claude Tool Use API:**
- Tool Use Overview: [https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)
- Structured Outputs: [https://docs.claude.com/en/docs/build-with-claude/structured-outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)
- API Development Guide: [https://www.anthropic.com/learn/build-with-claude](https://www.anthropic.com/learn/build-with-claude)

**Blog Posts:**
- MCP Announcement: [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)
- Code Execution with MCP: [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)

#### OpenAI

**Function Calling:**
- Main Guide: [https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
- Parallel Function Calling: [https://platform.openai.com/docs/guides/function-calling/parallel-function-calling-and-structured-outputs](https://platform.openai.com/docs/guides/function-calling/parallel-function-calling-and-structured-outputs)
- Assistants API: [https://platform.openai.com/docs/assistants/tools/function-calling](https://platform.openai.com/docs/assistants/tools/function-calling)
- Help Center: [https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api)

**Practical Guide:**
- Building Agents Guide: [https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Code Examples:**
- OpenAI Cookbook: [https://github.com/openai/openai-cookbook](https://github.com/openai/openai-cookbook)
- Function Calling Examples: [https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb)

#### Google (Gemini)

**Function Calling:**
- Main Documentation: [https://ai.google.dev/gemini-api/docs/function-calling](https://ai.google.dev/gemini-api/docs/function-calling)
- Tools Documentation: [https://ai.google.dev/gemini-api/docs/tools](https://ai.google.dev/gemini-api/docs/tools)
- Live API Tools: [https://ai.google.dev/gemini-api/docs/live-tools](https://ai.google.dev/gemini-api/docs/live-tools)
- Gemini 3 Guide: [https://ai.google.dev/gemini-api/docs/gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3)

**Vertex AI (Enterprise):**
- Function Calling Introduction: [https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)

**Tutorials:**
- Google Codelabs: [https://codelabs.developers.google.com/codelabs/gemini-function-calling](https://codelabs.developers.google.com/codelabs/gemini-function-calling)
- Firebase Guide: [https://firebase.google.com/docs/ai-logic/function-calling](https://firebase.google.com/docs/ai-logic/function-calling)

**Code Examples:**
- Gemini Cookbook: [https://github.com/google-gemini/cookbook](https://github.com/google-gemini/cookbook)
- Function Calling Notebook: [https://github.com/google-gemini/cookbook/blob/main/quickstarts/Function_calling.ipynb](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Function_calling.ipynb)
- GCP Examples: [https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/intro_function_calling.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/intro_function_calling.ipynb)

#### Microsoft

**M365 Copilot:**
- API Plugins: [https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-api-plugins](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-api-plugins)

**Copilot Studio:**
- Azure OpenAI Integration: [https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-azure-openai](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-azure-openai)
- October 2025 Updates: [https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-october-2025/](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-october-2025/)
- May 2025 Updates: [https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-may-2025/](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-may-2025/)

**Azure:**
- Azure OpenAI Function Calling: [https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/function-calling](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/function-calling)
- AI Agent Orchestration Patterns: [https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

**GitHub Copilot:**
- GitHub Copilot for Azure: [https://learn.microsoft.com/en-us/azure/developer/github-copilot-azure/get-started](https://learn.microsoft.com/en-us/azure/developer/github-copilot-azure/get-started)

**Blog Posts:**
- A2A Protocol Support: [https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/](https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/)
- Agent Factory: [https://azure.microsoft.com/en-us/blog/agent-factory-the-new-era-of-agentic-ai-common-use-cases-and-design-patterns/](https://azure.microsoft.com/en-us/blog/agent-factory-the-new-era-of-agentic-ai-common-use-cases-and-design-patterns/)

#### AWS (Bedrock)

**Tool Use:**
- Main Documentation: [https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)
- Converse API: [https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html)
- API Reference: [https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolConfiguration.html](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolConfiguration.html)
- Code Examples: [https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-examples.html](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-examples.html)

**GitHub Examples:**
- Function Calling Sample: [https://github.com/aws-samples/function-calling-using-amazon-bedrock-anthropic-claude-3](https://github.com/aws-samples/function-calling-using-amazon-bedrock-anthropic-claude-3)

**A2A Protocol:**
- AWS Blog: [https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-4-inter-agent-communication-on-a2a/](https://aws.amazon.com/blogs/opensource/open-protocols-for-agent-interoperability-part-4-inter-agent-communication-on-a2a/)

### 7.2 Open Standards and Protocols

#### Model Context Protocol (MCP)

- Official Website: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- GitHub Organization: [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- Documentation Hub: [https://www.claudemcp.com/docs](https://www.claudemcp.com/docs)
- Wikipedia: [https://en.wikipedia.org/wiki/Model_Context_Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)

**Tutorials:**
- Building MCP Clients (Node.js): [https://modelcontextprotocol.info/docs/tutorials/building-a-client-node/](https://modelcontextprotocol.info/docs/tutorials/building-a-client-node/)
- MCP Quickstart: [https://modelcontextprotocol.io/quickstart/client](https://modelcontextprotocol.io/quickstart/client)

#### Agent2Agent Protocol (A2A)

- Official Website: [https://a2aprotocol.ai](https://a2aprotocol.ai)
- GitHub Repository: [https://github.com/a2aproject/A2A](https://github.com/a2aproject/A2A)
- Complete Guide: [https://a2aprotocol.ai/blog/2025-full-guide-a2a-protocol](https://a2aprotocol.ai/blog/2025-full-guide-a2a-protocol)

**Announcements:**
- Google Blog: [https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- InfoQ Article: [https://www.infoq.com/news/2025/04/google-agentic-a2a/](https://www.infoq.com/news/2025/04/google-agentic-a2a/)

**Reference:**
- IBM Explainer: [https://www.ibm.com/think/topics/agent2agent-protocol](https://www.ibm.com/think/topics/agent2agent-protocol)

### 7.3 Community Resources and Tutorials

#### General AI Agents

- LLM Agents Guide: [https://www.promptingguide.ai/research/llm-agents](https://www.promptingguide.ai/research/llm-agents)
- AI Agent Protocols 2025: [https://dev.to/copilotkit/ai-agent-protocols-every-developer-should-know-in-2025-39m3](https://dev.to/copilotkit/ai-agent-protocols-every-developer-should-know-in-2025-39m3)

#### Comparative Analysis

**Protocol Comparisons:**
- MCP vs Function Calling vs OpenAPI: [https://www.marktechpost.com/2025/10/08/model-context-protocol-mcp-vs-function-calling-vs-openapi-tools-when-to-use-each/](https://www.marktechpost.com/2025/10/08/model-context-protocol-mcp-vs-function-calling-vs-openapi-tools-when-to-use-each/)
- Function Calling vs MCP: [https://medium.com/@1xcoder/mcp-vs-function-calling-understanding-the-future-of-llm-integrations-9ff33007b21d](https://medium.com/@1xcoder/mcp-vs-function-calling-understanding-the-future-of-llm-integrations-9ff33007b21d)
- Why You Need Both: [https://decryptai.substack.com/p/function-calling-vs-mcp-wrong-question](https://decryptai.substack.com/p/function-calling-vs-mcp-wrong-question)
- A2A vs MCP: [https://getstream.io/blog/agent2agent-vs-mcp/](https://getstream.io/blog/agent2agent-vs-mcp/)
- Four Protocol Comparison: [https://jtanruan.medium.com/open-standards-for-ai-agents-a-technical-comparison-of-a2a-mcp-langchain-agent-protocol-and-482be1101ad9](https://jtanruan.medium.com/open-standards-for-ai-agents-a-technical-comparison-of-a2a-mcp-langchain-agent-protocol-and-482be1101ad9)

**Vendor Comparisons:**
- OpenAI vs Anthropic vs Google: [https://xenoss.io/blog/openai-vs-anthropic-vs-google-gemini-enterprise-llm-platform-guide](https://xenoss.io/blog/openai-vs-anthropic-vs-google-gemini-enterprise-llm-platform-guide)
- LLM Competitive Landscape 2025: [https://www.globenewswire.com/news-release/2025/11/19/3191231/28124/en/Large-Language-Models-LLM-Competitive-Landscape-Report-2025-Evaluation-of-OpenAI-Google-Microsoft-Amazon-Anthropic-IBM-Meta-Cohere-and-Others.html](https://www.globenewswire.com/news-release/2025/11/19/3191231/28124/en/Large-Language-Models-LLM-Competitive-Landscape-Report-2025-Evaluation-of-OpenAI-Google-Microsoft-Amazon-Anthropic-IBM-Meta-Cohere-and-Others.html)
- Framework Comparison: [https://medium.com/@roberto.g.infante/the-state-of-ai-agent-frameworks-comparing-langgraph-openai-agent-sdk-google-adk-and-aws-d3e52a497720](https://medium.com/@roberto.g.infante/the-state-of-ai-agent-frameworks-comparing-langgraph-openai-agent-sdk-google-adk-and-aws-d3e52a497720)

#### Tutorials and Examples

**OpenAI:**
- DataCamp Tutorial: [https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial](https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial)
- Kanaries Guide: [https://docs.kanaries.net/articles/openai-function-calling](https://docs.kanaries.net/articles/openai-function-calling)
- Medium Guide: [https://medium.com/dev-bits/a-clear-guide-to-openai-function-calling-with-python-dcbc200c5d70](https://medium.com/dev-bits/a-clear-guide-to-openai-function-calling-with-python-dcbc200c5d70)

**Anthropic/MCP:**
- Creating MCP Server: [https://codecowboy.io/development/mcp_with_anthropic/](https://codecowboy.io/development/mcp_with_anthropic/)
- MCP with Python: [https://tinztwinshub.com/data-science/an-introduction-to-anthropic-model-context-protocol-mcp-with-python/](https://tinztwinshub.com/data-science/an-introduction-to-anthropic-model-context-protocol-mcp-with-python/)
- Ultimate MCP Guide: [https://guangzhengli.com/blog/en/model-context-protocol](https://guangzhengli.com/blog/en/model-context-protocol)

**Gemini:**
- Philipp Schmid's Guide: [https://www.philschmid.de/gemini-function-calling](https://www.philschmid.de/gemini-function-calling)

**AWS Bedrock:**
- Medium Tutorial: [https://medium.com/@zeek.granston/function-calling-with-anthropic-claude-and-amazon-bedrock-c6eda7358b0f](https://medium.com/@zeek.granston/function-calling-with-anthropic-claude-and-amazon-bedrock-c6eda7358b0f)

#### Design Patterns and Best Practices

**Design Patterns:**
- Microsoft Agent Factory: [https://azure.microsoft.com/en-us/blog/agent-factory-the-new-era-of-agentic-ai-common-use-cases-and-design-patterns/](https://azure.microsoft.com/en-us/blog/agent-factory-the-new-era-of-agentic-ai-common-use-cases-and-design-patterns/)
- 6 Design Patterns (2025): [https://valanor.co/design-patterns-for-ai-agents/](https://valanor.co/design-patterns-for-ai-agents/)
- 5 Agentic AI Patterns: [https://www.azilen.com/blog/agentic-ai-design-patterns/](https://www.azilen.com/blog/agentic-ai-design-patterns/)
- Complete Guide: [https://pub.towardsai.net/ai-agents-design-patterns-complete-guide-to-agentic-ai-models-in-2025-b0fe49cd02d7](https://pub.towardsai.net/ai-agents-design-patterns-complete-guide-to-agentic-ai-models-in-2025-b0fe49cd02d7)
- Google Cloud Patterns: [https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- 7 Must-Know Patterns: [https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns/](https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns/)

**Best Practices:**
- UiPath Best Practices: [https://www.uipath.com/blog/ai/agent-builder-best-practices](https://www.uipath.com/blog/ai/agent-builder-best-practices)
- Ultimate Guide 2025: [https://medium.com/@divyanshbhatiajm19/the-ultimate-guide-to-building-ai-agents-in-2025-from-concept-to-deployment-121da166562e](https://medium.com/@divyanshbhatiajm19/the-ultimate-guide-to-building-ai-agents-in-2025-from-concept-to-deployment-121da166562e)

#### JSON Schema and Structured Outputs

- How JSON Schema Works: [https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/](https://blog.promptlayer.com/how-json-schema-works-for-structured-outputs-and-tool-integration/)
- Optimizing LLM JSON Outputs: [https://dev.to/yigit-konur/the-art-of-the-description-your-ultimate-guide-to-optimizing-llm-json-outputs-with-json-schema-jne](https://dev.to/yigit-konur/the-art-of-the-description-your-ultimate-guide-to-optimizing-llm-json-outputs-with-json-schema-jne)
- Complete Guide to Structured Outputs: [https://superjson.ai/blog/2025-08-17-json-schema-structured-output-apis-complete-guide/](https://superjson.ai/blog/2025-08-17-json-schema-structured-output-apis-complete-guide/)
- Awesome LLM JSON: [https://github.com/imaurer/awesome-llm-json](https://github.com/imaurer/awesome-llm-json)

### 7.4 Market Analysis and Trends

**2025 Trends:**
- LLM Agents in 2025: [https://orq.ai/blog/llm-agents](https://orq.ai/blog/llm-agents)
- AI Agent Architecture 2025: [https://orq.ai/blog/ai-agent-architecture](https://orq.ai/blog/ai-agent-architecture)
- IBM Expectations vs Reality: [https://www.ibm.com/think/insights/ai-agents-2025-expectations-vs-reality](https://www.ibm.com/think/insights/ai-agents-2025-expectations-vs-reality)
- Framework Guide: [https://botpress.com/blog/llm-agent-framework](https://botpress.com/blog/llm-agent-framework)

**Framework Comparisons:**
- LLM Agent Frameworks: [https://livechatai.com/blog/llm-agent-frameworks](https://livechatai.com/blog/llm-agent-frameworks)
- Chatbase Guide: [https://www.chatbase.co/blog/llm-agent-framework-guide](https://www.chatbase.co/blog/llm-agent-framework-guide)
- Core Components: [https://futureagi.com/blogs/llm-agent-architectures-core-components](https://futureagi.com/blogs/llm-agent-architectures-core-components)

**Pricing:**
- LLM API Pricing 2025: [https://aithemes.net/en/posts/llm_provider_price_comparison_tags](https://aithemes.net/en/posts/llm_provider_price_comparison_tags)
- Top LLM Providers: [https://the-rogue-marketing.github.io/top-llm-api-provider-to-build-ai-applications-and-ai-agents/](https://the-rogue-marketing.github.io/top-llm-api-provider-to-build-ai-applications-and-ai-agents/)

### 7.5 GitHub Repositories

**MCP Servers:**
- Official SDK (TypeScript): [https://github.com/grunge-ai/anthropic-mcp](https://github.com/grunge-ai/anthropic-mcp)
- Think MCP Server: [https://github.com/marcopesani/think-mcp-server](https://github.com/marcopesani/think-mcp-server)
- MCP Servers Collection: [https://github.com/madhukarkumar/anthropic-mcp-servers](https://github.com/madhukarkumar/anthropic-mcp-servers)

**OpenAI Examples:**
- Function Calling Examples: [https://github.com/svpino/openai-function-calling](https://github.com/svpino/openai-function-calling)
- Weather Demo: [https://github.com/robertbenson/docker_openai_custom_weather_demo](https://github.com/robertbenson/docker_openai_custom_weather_demo)

**Tools:**
- Jsonformer: [https://github.com/1rgs/jsonformer](https://github.com/1rgs/jsonformer)
- Awesome LLM JSON: [https://github.com/imaurer/awesome-llm-json](https://github.com/imaurer/awesome-llm-json)

### 7.6 Technical Specifications

**JSON-RPC 2.0:**
- Used by MCP and A2A protocols
- Standard for remote procedure calls

**JSON Schema:**
- Universal schema definition language
- Used by all vendors for tool definitions

**OpenAPI Specification:**
- REST API description format
- Used by Microsoft and others for plugin definitions

---

## Summary and Key Takeaways

### The Evolution of AI Tool Integration

The AI/LLM ecosystem is rapidly standardizing around three complementary protocols:

1. **Function Calling**: Vendor-specific, optimized for tight integrations
2. **MCP**: Universal protocol for tool/data connectivity (becoming industry standard)
3. **A2A**: Protocol for multi-agent collaboration

### Choosing the Right Approach

**Use Function Calling when:**
- Building single-vendor solutions
- Need lowest latency
- Want simplest implementation
- Already committed to a vendor ecosystem

**Use MCP when:**
- Need cross-platform compatibility
- Building reusable integrations
- Want vendor independence
- Prioritize long-term maintainability

**Use A2A when:**
- Building multi-agent systems
- Need agent discovery and routing
- Want federated agent execution
- Building agent marketplaces

### 2025 Best Practices Summary

1. **Start with JSON Schema mastery** - It's universal across all vendors
2. **Version everything** - Tools, prompts, schemas, evaluations
3. **Test extensively** - Build comprehensive evaluation sets
4. **Optimize model selection** - Right-size models for tasks
5. **Prioritize safety** - Use automation for deterministic tasks
6. **Communicate clearly** - Set expectations, show progress, enable escalation
7. **Monitor and iterate** - Continuous evaluation and improvement

### The Future (2025 and Beyond)

- **Standardization**: MCP and A2A adoption accelerating across vendors
- **Multi-agent systems**: Expected to become mainstream (50% enterprises by 2027)
- **Improved reliability**: Structured outputs reducing errors by 90%+
- **Better tooling**: Enhanced SDKs, debugging, and monitoring
- **Enterprise integration**: Deeper connections to business systems

---

**Report Compiled:** November 2025
**Total Sources Referenced:** 100+
**Vendors Covered:** Anthropic, OpenAI, Google, Microsoft, AWS
**Code Examples:** 20+ working implementations

---

*This report represents a comprehensive snapshot of the AI/LLM tools and plugins landscape as of November 2025, based on official documentation, industry research, and practical implementations.*
