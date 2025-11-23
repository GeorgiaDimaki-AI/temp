# Plugin and Tool Code Examples

Complete code examples for creating tools across different AI vendors.

## Anthropic Claude Examples

### Example 1: Basic Tool Use

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location. Use this when users ask about weather conditions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state or city and country (e.g., 'San Francisco, CA' or 'London, UK')"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit",
                    "default": "fahrenheit"
                }
            },
            "required": ["location"]
        }
    }
]

# Call Claude
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What's the weather like in NYC?"}
    ],
    tools=tools
)

# Process tool use
if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")

    # Execute tool
    if tool_use.name == "get_weather":
        location = tool_use.input["location"]
        weather_data = fetch_weather(location)  # Your implementation

        # Send result back
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "What's the weather like in NYC?"},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": weather_data
                        }
                    ]
                }
            ],
            tools=tools
        )

print(response.content[0].text)
```

### Example 2: Structured Outputs (Nov 2025)

```python
import anthropic
from pydantic import BaseModel

class WeatherResponse(BaseModel):
    temperature: float
    conditions: str
    humidity: int
    wind_speed: float

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Weather in Paris"}],
    # Guaranteed to match schema
    response_format=WeatherResponse
)

# Zero parsing errors - guaranteed valid
weather = WeatherResponse.model_validate_json(response.content[0].text)
print(f"Temp: {weather.temperature}°F")
```

## OpenAI Examples

### Example 3: Function Calling

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state or country"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            },
            "strict": True  # Structured outputs mode
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ],
    tools=functions
)

# Process function call
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_weather":
            args = json.loads(tool_call.function.arguments)
            weather = get_weather(args["location"], args.get("unit", "fahrenheit"))

            # Send result back
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": "What's the weather in Tokyo?"},
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": weather
                    }
                ],
                tools=functions
            )

print(response.choices[0].message.content)
```

### Example 4: Parallel Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the weather in NYC and Tokyo?"}
    ],
    tools=functions,
    parallel_tool_calls=True  # Enable parallel execution
)

# Process multiple tool calls
message = response.choices[0].message
if message.tool_calls:
    tool_results = []

    # Execute all tools (can be done in parallel)
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(args["location"])

        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    # Send all results back at once
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "What's the weather in NYC and Tokyo?"},
            message,
            *tool_results
        ],
        tools=functions
    )

print(final_response.choices[0].message.content)
```

## Google Gemini Examples

### Example 5: Auto Function Conversion

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# Define Python function - automatically converted!
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """
    Get current weather for a location.

    Args:
        location: The city and state or country
        unit: Temperature unit (celsius or fahrenheit)

    Returns:
        Weather description
    """
    # Your implementation
    return f"Weather in {location}: Sunny, 72°{unit[0].upper()}"

# Create model with function
model = genai.GenerativeModel(
    "gemini-3-flash",
    tools=[get_weather]  # Automatic conversion from Python function!
)

# Call model
response = model.generate_content("What's the weather in Paris?")
print(response.text)
```

### Example 6: Manual Function Definition

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")

# Manual definition
weather_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_weather",
            description="Get current weather for a location",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "location": genai.protos.Schema(type=genai.protos.Type.STRING),
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

model = genai.GenerativeModel("gemini-3-flash", tools=[weather_tool])

# Configure function calling mode
response = model.generate_content(
    "Weather in London?",
    tool_config={
        "function_calling_config": {
            "mode": "AUTO"  # AUTO, ANY, or NONE
        }
    }
)

# Handle function call
for part in response.parts:
    if fn := part.function_call:
        # Execute function
        result = get_weather(fn.args["location"])

        # Send result back
        response = model.generate_content([
            response.candidates[0].content,
            genai.protos.Content(
                parts=[genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=fn.name,
                        response={"result": result}
                    )
                )]
            )
        ])

print(response.text)
```

## AWS Bedrock Examples

### Example 7: Converse API

```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Define tool
tools = [
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
                            "description": "City and state or country"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    }
]

# Call model
response = bedrock.converse(
    modelId="anthropic.claude-sonnet-4-5-v1",
    messages=[
        {
            "role": "user",
            "content": [{"text": "What's the weather in Seattle?"}]
        }
    ],
    toolConfig={"tools": tools}
)

# Process tool use
output_message = response["output"]["message"]

if output_message["stopReason"] == "tool_use":
    for content_block in output_message["content"]:
        if "toolUse" in content_block:
            tool_use = content_block["toolUse"]

            # Execute tool
            weather = get_weather(tool_use["input"]["location"])

            # Send result back
            response = bedrock.converse(
                modelId="anthropic.claude-sonnet-4-5-v1",
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": "What's the weather in Seattle?"}]
                    },
                    output_message,
                    {
                        "role": "user",
                        "content": [
                            {
                                "toolResult": {
                                    "toolUseId": tool_use["toolUseId"],
                                    "content": [{"text": weather}]
                                }
                            }
                        ]
                    }
                ],
                toolConfig={"tools": tools}
            )

print(response["output"]["message"]["content"][0]["text"])
```

## Production Pattern: Reusable Tool Executor

```python
from typing import Callable, Dict, List, Any
import json

class ToolExecutor:
    """Reusable tool execution framework"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        """Register a tool function"""
        self.tools[name] = func

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name"""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            result = self.tools[tool_name](**arguments)
            return json.dumps({"success": True, "result": result})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    def get_schemas(self, format: str = "anthropic") -> List[Dict]:
        """Get tool schemas for different vendors"""
        schemas = []

        for name, func in self.tools.items():
            if format == "anthropic":
                schemas.append(self._anthropic_schema(name, func))
            elif format == "openai":
                schemas.append(self._openai_schema(name, func))

        return schemas

    def _anthropic_schema(self, name: str, func: Callable) -> Dict:
        """Generate Anthropic tool schema"""
        return {
            "name": name,
            "description": func.__doc__ or f"Execute {name}",
            "input_schema": self._extract_schema(func)
        }

    def _openai_schema(self, name: str, func: Callable) -> Dict:
        """Generate OpenAI function schema"""
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": func.__doc__ or f"Execute {name}",
                "parameters": self._extract_schema(func)
            }
        }

# Usage
executor = ToolExecutor()

def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get weather for a location"""
    return f"Sunny, 72°{unit[0].upper()}"

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between coordinates"""
    # Haversine formula implementation
    return 100.5  # km

executor.register("get_weather", get_weather)
executor.register("calculate_distance", calculate_distance)

# Get schemas for Anthropic
anthropic_tools = executor.get_schemas("anthropic")

# Get schemas for OpenAI
openai_tools = executor.get_schemas("openai")

# Execute tools
result = executor.execute("get_weather", {"location": "NYC"})
print(result)
```

This shows the core patterns for creating tools across all major AI vendors. The key is understanding each vendor's schema format and execution flow.
