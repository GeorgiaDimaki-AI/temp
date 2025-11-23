# Agent SDK Code Examples

Comprehensive code examples demonstrating the Claude Agent SDK in Python and TypeScript.

## Table of Contents

1. [Basic Python Examples](#basic-python-examples)
2. [Advanced Python Patterns](#advanced-python-patterns)
3. [TypeScript Examples](#typescript-examples)
4. [Production Patterns](#production-patterns)
5. [Real-World Applications](#real-world-applications)

## Basic Python Examples

### Example 1: Hello World Agent

```python
import anyio
from claude_agent_sdk import query

async def main():
    """Simplest possible agent"""
    async for message in query(prompt="What is 2 + 2?"):
        if message.type == "text":
            print(message.content)

anyio.run(main())
```

Output:
```
2 + 2 = 4
```

### Example 2: Basic Agent with Options

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def main():
    # Initialize client
    client = ClaudeSDKClient(api_key="your-api-key")

    # Configure agent
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        max_turns=10,
        allowed_tools=["Read", "Write", "Bash"],
        working_directory="/workspace"
    )

    # Send message
    async for message in client.send_message(
        prompt="List all Python files in the current directory",
        options=options
    ):
        if message.type == "text":
            print(f"Agent: {message.content}")
        elif message.type == "tool_use":
            print(f"Using tool: {message.tool_name}")

anyio.run(main())
```

### Example 3: File Analysis Agent

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def analyze_codebase():
    """Agent that analyzes a codebase"""
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="""You are a code analysis expert.
        Analyze codebases for quality, bugs, and improvements.""",
        max_turns=30,
        allowed_tools=["Read", "Glob", "Grep"],  # Read-only
        working_directory="/workspace/project"
    )

    prompt = """
    Please analyze this codebase:
    1. Find all Python files
    2. Check for common code smells
    3. Identify potential bugs
    4. Suggest improvements
    """

    async for message in client.send_message(prompt, options):
        if message.type == "text":
            print(message.content)

anyio.run(analyze_codebase())
```

## Advanced Python Patterns

### Example 4: Agent with Custom Tools

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    create_sdk_mcp_server
)
import anyio
import aiohttp

# Define custom tools
async def fetch_weather(city: str) -> str:
    """
    Fetch current weather for a city.

    Args:
        city: City name (e.g., "San Francisco, CA")

    Returns:
        Weather description
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weather.com/v1/current?city={city}"
        async with session.get(url) as response:
            data = await response.json()
            return f"Weather in {city}: {data['conditions']}, {data['temp']}°F"

def calculate_roi(
    investment: float,
    return_amount: float,
    years: float
) -> Dict[str, float]:
    """
    Calculate return on investment.

    Args:
        investment: Initial investment amount
        return_amount: Final return amount
        years: Investment period in years

    Returns:
        ROI metrics including percentage and annual rate
    """
    total_return = return_amount - investment
    roi_percentage = (total_return / investment) * 100
    annual_rate = ((return_amount / investment) ** (1/years) - 1) * 100

    return {
        "total_return": total_return,
        "roi_percentage": round(roi_percentage, 2),
        "annual_rate": round(annual_rate, 2)
    }

# Create MCP server with custom tools
custom_tools = create_sdk_mcp_server(
    name="custom-tools",
    tools=[fetch_weather, calculate_roi]
)

async def main():
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant with access to weather and financial tools.",
        mcp_servers=[custom_tools],
        max_turns=20
    )

    async for message in client.send_message(
        prompt="What's the weather in NYC and what's the ROI on a $10k investment returning $15k over 5 years?",
        options=options
    ):
        print(message)

anyio.run(main())
```

### Example 5: Agent with Security Hooks

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    PreToolUseHook,
    PostToolUseHook,
    HookMatcher
)
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security validation hook
async def validate_bash_command(context):
    """Block dangerous bash commands"""
    command = context.tool_input.get("command", "")

    # Dangerous patterns
    dangerous = [
        r"rm\s+-rf\s+/",  # rm -rf /
        r"dd\s+if=",  # dd commands
        r"mkfs",  # filesystem formatting
        r":\(\)\{.*\|\:&\}\;",  # fork bombs
        r">\s*/dev/sd",  # writing to devices
        r"curl.*\|\s*bash",  # pipe to bash
    ]

    for pattern in dangerous:
        if re.search(pattern, command, re.IGNORECASE):
            logger.warning(f"Blocked dangerous command: {command}")
            return {
                "permission_decision": "deny",
                "feedback": f"Command blocked for safety: contains '{pattern}'"
            }

    # Log all allowed commands
    logger.info(f"Allowing command: {command}")
    return {"permission_decision": "allow"}

# Audit logging hook
async def audit_log(context):
    """Log all tool executions for compliance"""
    logger.info({
        "event": "tool_execution",
        "tool": context.tool_name,
        "input": context.tool_input,
        "success": context.success,
        "duration_ms": context.duration_ms,
        "timestamp": context.timestamp
    })
    return {}

async def main():
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="You are a system administrator assistant.",
        allowed_tools=["Bash", "Read", "Write"],
        hooks=[
            PreToolUseHook(
                matcher=HookMatcher(tool_names=["Bash"]),
                callback=validate_bash_command
            ),
            PostToolUseHook(
                matcher=HookMatcher(all_tools=True),
                callback=audit_log
            )
        ],
        working_directory="/workspace"
    )

    async for message in client.send_message(
        prompt="Set up a Python development environment",
        options=options
    ):
        print(message)

anyio.run(main())
```

### Example 6: Multi-Step Data Analysis

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def analyze_sales_data():
    """Agent that performs multi-step data analysis"""
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="""You are a data analyst expert.
        You can read CSV files, analyze data, and create visualizations.""",
        max_turns=50,
        allowed_tools=["Read", "Write", "Bash"],
        working_directory="/workspace/data"
    )

    prompt = """
    Analyze the sales data in sales_2024.csv:

    1. Read and understand the data structure
    2. Calculate key metrics:
       - Total revenue
       - Average order value
       - Top 5 products by revenue
       - Monthly revenue trend
    3. Create a Python visualization script using matplotlib
    4. Generate a summary report in markdown format

    Save the visualization as sales_analysis.png and the report as analysis_report.md
    """

    results = []
    async for message in client.send_message(prompt, options):
        if message.type == "text":
            print(f"\nAgent: {message.content}")
            results.append(message.content)
        elif message.type == "tool_use":
            print(f"\nExecuting: {message.tool_name}")

    return results

anyio.run(analyze_sales_data())
```

### Example 7: Iterative Code Generation

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def build_feature():
    """Agent that builds and tests a feature iteratively"""
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="""You are an expert Python developer.
        Write high-quality, tested code following best practices.""",
        max_turns=40,
        allowed_tools=["Read", "Write", "Edit", "Bash", "Grep"],
        working_directory="/workspace/project"
    )

    prompt = """
    Implement a user authentication system:

    1. Create a User model with email and password fields
    2. Implement password hashing using bcrypt
    3. Create login and registration functions
    4. Write comprehensive unit tests
    5. Run the tests and fix any failures
    6. Document the API with docstrings

    Iterate until all tests pass.
    """

    async for message in client.send_message(prompt, options):
        if message.type == "text":
            print(message.content)
        elif message.type == "tool_use":
            print(f"[{message.tool_name}] {message.input.get('file_path', '')}")

anyio.run(build_feature())
```

## TypeScript Examples

### Example 8: Basic TypeScript Agent

```typescript
import { ClaudeSDKClient, ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  const client = new ClaudeSDKClient({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  const options: ClaudeAgentOptions = {
    systemPrompt: "You are a helpful coding assistant",
    maxTurns: 20,
    allowedTools: ["Read", "Write", "Bash"],
    workingDirectory: "/workspace",
  };

  const stream = client.sendMessage(
    "Analyze the package.json and suggest dependency updates",
    options
  );

  for await (const message of stream) {
    if (message.type === "text") {
      console.log(`Agent: ${message.content}`);
    } else if (message.type === "tool_use") {
      console.log(`Using: ${message.toolName}`);
    }
  }
}

main().catch(console.error);
```

### Example 9: TypeScript with Custom Tools

```typescript
import {
  ClaudeSDKClient,
  ClaudeAgentOptions,
  createSdkMcpServer,
} from "@anthropic-ai/claude-agent-sdk";

// Define custom tools
async function queryDatabase(sql: string): Promise<any[]> {
  /**
   * Execute SQL query against the database
   *
   * @param sql - SQL query string
   * @returns Query results
   */
  // Your database logic here
  const results = await db.query(sql);
  return results;
}

async function sendEmail(
  to: string,
  subject: string,
  body: string
): Promise<string> {
  /**
   * Send an email
   *
   * @param to - Recipient email address
   * @param subject - Email subject
   * @param body - Email body
   * @returns Confirmation message
   */
  // Your email logic here
  await emailService.send({ to, subject, body });
  return `Email sent to ${to}`;
}

// Create MCP server
const customTools = createSdkMcpServer({
  name: "business-tools",
  tools: [queryDatabase, sendEmail],
});

async function main() {
  const client = new ClaudeSDKClient({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  const options: ClaudeAgentOptions = {
    systemPrompt: "You are a business automation assistant",
    mcpServers: [customTools],
    maxTurns: 30,
  };

  const stream = client.sendMessage(
    "Find customers with overdue invoices and send them reminder emails",
    options
  );

  for await (const message of stream) {
    console.log(message);
  }
}

main();
```

## Production Patterns

### Example 10: Error Handling and Retries

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from tenacity import retry, stop_after_attempt, wait_exponential
import anyio
import logging

logger = logging.getLogger(__name__)

class RobustAgent:
    """Production-ready agent with error handling"""

    def __init__(self, api_key: str):
        self.client = ClaudeSDKClient(api_key=api_key)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def execute_task(
        self,
        prompt: str,
        options: ClaudeAgentOptions
    ) -> List[str]:
        """Execute task with automatic retries"""
        results = []

        try:
            async for message in self.client.send_message(prompt, options):
                if message.type == "text":
                    results.append(message.content)
                elif message.type == "error":
                    logger.error(f"Agent error: {message.error}")
                    raise Exception(message.error)

            return results

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            raise

    async def execute_with_timeout(
        self,
        prompt: str,
        options: ClaudeAgentOptions,
        timeout_seconds: int = 300
    ):
        """Execute with timeout"""
        try:
            return await anyio.wait_for(
                self.execute_task(prompt, options),
                timeout=timeout_seconds
            )
        except TimeoutError:
            logger.error(f"Task timeout after {timeout_seconds}s")
            raise

# Usage
async def main():
    agent = RobustAgent(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        max_turns=20
    )

    try:
        results = await agent.execute_with_timeout(
            "Analyze the codebase",
            options,
            timeout_seconds=300
        )
        print(results)
    except Exception as e:
        logger.error(f"Failed after retries: {e}")

anyio.run(main())
```

### Example 11: Cost Monitoring

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio
from dataclasses import dataclass
from typing import List

@dataclass
class UsageMetrics:
    """Track agent resource usage"""
    total_turns: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    tool_executions: int = 0
    total_cost: float = 0.0

    def calculate_cost(self):
        """Calculate cost based on Claude Sonnet 4.5 pricing"""
        # $3 per million input tokens
        # $15 per million output tokens
        input_cost = (self.total_input_tokens / 1_000_000) * 3
        output_cost = (self.total_output_tokens / 1_000_000) * 15
        self.total_cost = input_cost + output_cost
        return self.total_cost

class MonitoredAgent:
    """Agent with cost and usage monitoring"""

    def __init__(self, api_key: str):
        self.client = ClaudeSDKClient(api_key=api_key)
        self.metrics = UsageMetrics()

    async def execute(self, prompt: str, options: ClaudeAgentOptions):
        """Execute and track metrics"""
        turn = 0

        async for message in self.client.send_message(prompt, options):
            if message.type == "text":
                # Track token usage
                self.metrics.total_input_tokens += message.input_tokens
                self.metrics.total_output_tokens += message.output_tokens
                self.metrics.total_turns += 1

                print(message.content)

            elif message.type == "tool_use":
                self.metrics.tool_executions += 1
                print(f"Tool: {message.tool_name}")

            turn += 1

        # Calculate final cost
        cost = self.metrics.calculate_cost()
        print(f"\n--- Usage Metrics ---")
        print(f"Turns: {self.metrics.total_turns}")
        print(f"Input tokens: {self.metrics.total_input_tokens:,}")
        print(f"Output tokens: {self.metrics.total_output_tokens:,}")
        print(f"Tool executions: {self.metrics.tool_executions}")
        print(f"Estimated cost: ${cost:.4f}")

# Usage
async def main():
    agent = MonitoredAgent(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        max_turns=20,
        max_tokens_per_turn=4000  # Control output size
    )

    await agent.execute("Analyze this codebase", options)

anyio.run(main())
```

## Real-World Applications

### Example 12: Customer Support Agent

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    create_sdk_mcp_server
)
import anyio

# Customer database tool
async def get_customer_info(customer_id: str) -> Dict:
    """Fetch customer information from CRM"""
    # Database query
    customer = await crm_db.query(
        "SELECT * FROM customers WHERE id = ?",
        customer_id
    )
    return customer

async def get_order_history(customer_id: str) -> List[Dict]:
    """Get customer's order history"""
    orders = await orders_db.query(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY date DESC",
        customer_id
    )
    return orders

async def create_support_ticket(
    customer_id: str,
    issue: str,
    priority: str = "medium"
) -> str:
    """Create support ticket"""
    ticket_id = await support_system.create_ticket({
        "customer_id": customer_id,
        "issue": issue,
        "priority": priority
    })
    return f"Ticket created: {ticket_id}"

# Create tools
support_tools = create_sdk_mcp_server(
    name="support-tools",
    tools=[get_customer_info, get_order_history, create_support_ticket]
)

async def handle_customer_query(query: str, customer_id: str):
    """Handle customer support query"""
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt=f"""You are a helpful customer support agent.
        Current customer ID: {customer_id}

        Guidelines:
        - Be friendly and professional
        - Look up customer information when needed
        - Create support tickets for issues you can't resolve
        - Always summarize what you did to help
        """,
        mcp_servers=[support_tools],
        max_turns=25
    )

    response = []
    async for message in client.send_message(query, options):
        if message.type == "text":
            response.append(message.content)

    return "\n".join(response)

# Usage
async def main():
    response = await handle_customer_query(
        "I haven't received my order from last week",
        customer_id="CUST-12345"
    )
    print(response)

anyio.run(main())
```

### Example 13: DevOps Automation Agent

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def deploy_application():
    """Autonomous DevOps agent"""
    client = ClaudeSDKClient(api_key="your-api-key")

    options = ClaudeAgentOptions(
        system_prompt="""You are a DevOps automation expert.
        You can deploy applications, manage infrastructure, and troubleshoot issues.

        Deployment checklist:
        1. Run tests
        2. Build Docker image
        3. Push to registry
        4. Update Kubernetes manifests
        5. Apply manifests
        6. Verify deployment
        7. Run smoke tests
        """,
        allowed_tools=["Read", "Write", "Bash"],
        working_directory="/workspace/app",
        max_turns=50
    )

    prompt = """
    Deploy the application to production:

    1. Run the test suite (pytest)
    2. If tests pass, build Docker image
    3. Tag image with version from package.json
    4. Push to Docker Hub
    5. Update k8s/deployment.yaml with new image tag
    6. Apply Kubernetes manifests
    7. Wait for rollout to complete
    8. Run smoke tests against production
    9. If smoke tests fail, rollback
    10. Report deployment status

    Handle errors appropriately and provide detailed logging.
    """

    async for message in client.send_message(prompt, options):
        if message.type == "text":
            print(f"\n{message.content}")
        elif message.type == "tool_use":
            print(f"\n[EXECUTING] {message.tool_name}")
            if message.tool_name == "Bash":
                print(f"  Command: {message.input['command']}")

anyio.run(deploy_application())
```

These examples demonstrate the full spectrum of Agent SDK capabilities, from basic usage to production-ready patterns. The SDK handles the complexity of agent orchestration while giving you complete control over behavior, security, and functionality.
