# A2A Code Examples: Practical Implementations

This document provides comprehensive code examples demonstrating A2A protocol implementation in Python, from simple agents to complex multi-agent systems.

## Installation

```bash
# Python SDK
pip install python-a2a

# Optional dependencies
pip install openai  # For LLM-powered agents
pip install requests # For HTTP clients
```

## Example 1: Simple Weather Agent

### Server Implementation

```python
from python_a2a import A2AServer, skill, agent, run_server
from python_a2a import TaskStatus, TaskState

@agent(
    name="Weather Agent",
    description="Provides weather information for cities worldwide",
    version="1.0.0"
)
class WeatherAgent(A2AServer):

    @skill(
        name="Get Weather",
        description="Get current weather for a location",
        tags=["weather", "forecast"]
    )
    def get_weather(self, location: str) -> str:
        """Get weather for a location."""
        # In production, this would call a real weather API
        weather_data = {
            "Paris": "sunny and 75°F",
            "London": "cloudy and 60°F",
            "Tokyo": "rainy and 68°F",
            "New York": "partly cloudy and 70°F"
        }
        return weather_data.get(location, f"Weather data not available for {location}")

    def handle_task(self, task):
        """Process incoming tasks."""
        # Extract message content
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""

        # Parse request
        if "weather" in text.lower() and "in" in text.lower():
            # Extract location from natural language
            location = text.split("in", 1)[1].strip().rstrip("?.")
            weather_text = self.get_weather(location)

            # Create response artifact
            task.artifacts = [{
                "parts": [{"type": "text", "text": weather_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            # Request more information
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={
                    "role": "agent",
                    "content": {
                        "type": "text",
                        "text": "Please ask about weather in a specific location."
                    }
                }
            )

        return task

if __name__ == "__main__":
    agent = WeatherAgent()
    run_server(agent, host="0.0.0.0", port=5000)
```

### Client Usage

```python
from python_a2a import A2AClient

# Connect to agent
client = A2AClient("http://localhost:5000")

# Discover agent capabilities
print(f"Connected to: {client.agent_card.name}")
print(f"Description: {client.agent_card.description}")
print(f"Skills: {[skill.name for skill in client.agent_card.skills]}")

# Send a query
response = client.ask("What's the weather in Paris?")
print(f"Response: {response}")
# Output: "sunny and 75°F"
```

## Example 2: LLM-Powered Agent

```python
import os
from python_a2a import OpenAIA2AServer, run_server

# Create agent backed by OpenAI GPT-4
agent = OpenAIA2AServer(
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4",
    system_prompt="""You are a helpful AI assistant specialized in
    explaining complex technical topics in simple terms. Always provide
    clear, concise answers with practical examples.""",
    name="Technical Explainer",
    description="Explains complex topics simply"
)

if __name__ == "__main__":
    run_server(agent, host="0.0.0.0", port=5001)
```

**Client Usage**:
```python
client = A2AClient("http://localhost:5001")
response = client.ask("Explain quantum computing in simple terms")
print(response)
```

## Example 3: Calculator Agent with Multiple Skills

```python
from python_a2a import agent, skill, A2AServer, run_server
from python_a2a import TaskStatus, TaskState

@agent(
    name="Calculator",
    description="Performs mathematical calculations",
    version="1.0.0"
)
class CalculatorAgent(A2AServer):

    @skill(
        name="Add",
        description="Add two numbers",
        tags=["math", "addition"]
    )
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return float(a) + float(b)

    @skill(
        name="Multiply",
        description="Multiply two numbers",
        tags=["math", "multiplication"]
    )
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return float(a) * float(b)

    @skill(
        name="Divide",
        description="Divide two numbers",
        tags=["math", "division"]
    )
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return float(a) / float(b)

    def handle_task(self, task):
        """Process mathematical operations."""
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "")

        try:
            # Simple parsing logic
            if "+" in text:
                parts = text.split("+")
                result = self.add(float(parts[0].strip()), float(parts[1].strip()))
            elif "*" in text:
                parts = text.split("*")
                result = self.multiply(float(parts[0].strip()), float(parts[1].strip()))
            elif "/" in text:
                parts = text.split("/")
                result = self.divide(float(parts[0].strip()), float(parts[1].strip()))
            else:
                raise ValueError("Unsupported operation. Use +, *, or /")

            task.artifacts = [{
                "parts": [{"type": "text", "text": f"Result: {result}"}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={
                    "role": "agent",
                    "content": {"type": "text", "text": f"Error: {str(e)}"}
                }
            )

        return task

if __name__ == "__main__":
    calculator = CalculatorAgent()
    run_server(calculator, port=5002)
```

## Example 4: Multi-Agent Collaboration

### Travel Planning Orchestrator

```python
from python_a2a import A2AClient

class TravelOrchestratorAgent:
    def __init__(self):
        # Connect to specialized agents
        self.weather_agent = A2AClient("http://weather-agent.example.com")
        self.activity_agent = A2AClient("http://activity-agent.example.com")
        self.booking_agent = A2AClient("http://booking-agent.example.com")

    def plan_trip(self, destination: str, duration: int):
        """Orchestrate trip planning across multiple agents."""

        # Step 1: Get weather forecast
        weather_response = self.weather_agent.ask(
            f"What's the weather in {destination} for the next {duration} days?"
        )
        print(f"Weather: {weather_response}")

        # Step 2: Get activity recommendations
        activity_response = self.activity_agent.ask(
            f"Recommend activities in {destination} for {duration} days. "
            f"Weather forecast: {weather_response}"
        )
        print(f"Activities: {activity_response}")

        # Step 3: Find hotels
        booking_response = self.booking_agent.ask(
            f"Find hotels in {destination} near these activities: {activity_response}"
        )
        print(f"Booking: {booking_response}")

        # Step 4: Synthesize final itinerary
        final_plan = {
            "destination": destination,
            "duration": duration,
            "weather": weather_response,
            "activities": activity_response,
            "hotels": booking_response
        }

        return final_plan

# Usage
orchestrator = TravelOrchestratorAgent()
itinerary = orchestrator.plan_trip("Tokyo", 5)
print(f"\nFinal Itinerary: {itinerary}")
```

## Example 5: Long-Running Task with Async Processing

### Server with Background Processing

```python
from python_a2a import A2AServer, agent, run_server
from python_a2a import TaskStatus, TaskState
import time
import threading

@agent(
    name="Data Processing Agent",
    description="Processes large datasets asynchronously",
    version="1.0.0"
)
class DataProcessingAgent(A2AServer):
    def __init__(self):
        super().__init__()
        self.tasks = {}  # In-memory task storage

    def handle_task(self, task):
        """Start long-running processing."""
        # Store task
        self.tasks[task.id] = task

        # Immediately return with 'working' status
        task.status = TaskStatus(
            state=TaskState.WORKING,
            message={
                "role": "agent",
                "content": {
                    "type": "text",
                    "text": "Processing started. This may take a while..."
                }
            }
        )

        # Start background processing
        thread = threading.Thread(
            target=self._process_in_background,
            args=(task.id,)
        )
        thread.daemon = True
        thread.start()

        return task

    def _process_in_background(self, task_id):
        """Simulate long-running processing."""
        time.sleep(30)  # Simulate 30 seconds of processing

        # Update task when complete
        task = self.tasks[task_id]
        task.artifacts = [{
            "parts": [{
                "type": "text",
                "text": "Processing complete! 10,000 records analyzed."
            }]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        # If webhook configured, send notification
        if hasattr(task, 'webhook_url'):
            self.notify_webhook(task)

if __name__ == "__main__":
    agent = DataProcessingAgent()
    run_server(agent, port=5003)
```

### Client with Polling

```python
import time
from python_a2a import A2AClient

client = A2AClient("http://localhost:5003")

# Start long-running task
task = client.send_message("Process dataset.csv")
print(f"Task started: {task.id}")
print(f"Initial status: {task.status.state}")

# Poll for completion
while task.status.state == "WORKING":
    time.sleep(5)  # Wait 5 seconds
    task = client.get_task(task.id)
    print(f"Status: {task.status.state}")

# Task completed
if task.status.state == "COMPLETED":
    print(f"Result: {task.artifacts[0]['parts'][0]['text']}")
```

## Example 6: Agent with Push Notifications (Webhooks)

### Client with Webhook Receiver

```python
from flask import Flask, request, jsonify
from python_a2a import A2AClient
import threading

# Setup webhook receiver
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_notification():
    """Handle incoming webhook notifications."""
    notification = request.json

    # Verify authorization
    auth = request.headers.get('Authorization')
    if auth != 'Bearer my-secret-token':
        return jsonify({'error': 'Unauthorized'}), 401

    # Process notification
    if notification['type'] == 'taskStatusUpdate':
        print(f"Task {notification['taskId']} status: {notification['status']['state']}")

        if notification['status']['state'] == 'COMPLETED':
            print(f"Artifacts: {notification.get('artifacts', [])}")

    return jsonify({'status': 'received'}), 200

# Start webhook server in background
def start_webhook_server():
    app.run(port=8080, debug=False)

webhook_thread = threading.Thread(target=start_webhook_server)
webhook_thread.daemon = True
webhook_thread.start()

# Connect to agent with webhook configuration
client = A2AClient("http://localhost:5003")
task = client.send_message(
    message="Process large dataset",
    push_notification_config={
        "url": "http://localhost:8080/webhook",
        "headers": {"Authorization": "Bearer my-secret-token"},
        "events": ["taskStatusUpdate"]
    }
)

print(f"Task submitted: {task.id}")
print("Waiting for webhook notifications...")

# Keep script running
import time
while True:
    time.sleep(1)
```

## Example 7: Agent Discovery

```python
import requests
import json

def discover_agent(agent_url):
    """Discover agent capabilities via Agent Card."""
    # Standard well-known URI
    well_known_url = f"{agent_url}/.well-known/agent.json"

    try:
        response = requests.get(well_known_url)
        response.raise_for_status()
        agent_card = response.json()

        print(f"\nAgent: {agent_card['name']}")
        print(f"Description: {agent_card['description']}")
        print(f"Protocol Version: {agent_card['protocolVersion']}")

        print(f"\nCapabilities:")
        caps = agent_card['capabilities']
        print(f"  Streaming: {caps.get('streaming', False)}")
        print(f"  Push Notifications: {caps.get('pushNotifications', False)}")

        print(f"\nSkills:")
        for skill in agent_card['skills']:
            print(f"  - {skill['name']}: {skill['description']}")
            print(f"    Input: {', '.join(skill['inputModes'])}")
            print(f"    Output: {', '.join(skill['outputModes'])}")

        return agent_card

    except requests.RequestException as e:
        print(f"Failed to discover agent: {e}")
        return None

# Discover multiple agents
agents = [
    "http://weather-agent.example.com",
    "http://calculator-agent.example.com",
    "http://translator-agent.example.com"
]

for agent_url in agents:
    print(f"\n{'='*60}")
    discover_agent(agent_url)
```

## Example 8: Multi-Modal Agent

```python
from python_a2a import A2AServer, agent, skill, run_server
from python_a2a import TaskStatus, TaskState
import base64

@agent(
    name="Image Analysis Agent",
    description="Analyzes images and provides descriptions",
    version="1.0.0"
)
class ImageAnalysisAgent(A2AServer):

    @skill(
        name="Analyze Image",
        description="Provides detailed analysis of images",
        tags=["vision", "analysis"]
    )
    def analyze_image(self, image_url: str) -> dict:
        """Analyze an image."""
        # In production, use actual computer vision API
        return {
            "description": "A sunny landscape with mountains",
            "objects": ["mountain", "sky", "trees"],
            "dominant_colors": ["blue", "green", "white"]
        }

    def handle_task(self, task):
        """Process image analysis tasks."""
        message_data = task.message or {}
        content = message_data.get("content", {})

        if content.get("type") == "image":
            # Extract image URL
            image_url = content.get("imageUrl")
            analysis = self.analyze_image(image_url)

            # Return multi-part artifact
            task.artifacts = [{
                "parts": [
                    {
                        "type": "text",
                        "text": f"Image Analysis: {analysis['description']}"
                    },
                    {
                        "type": "structured_data",
                        "data": analysis
                    }
                ]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={
                    "role": "agent",
                    "content": {
                        "type": "text",
                        "text": "Please provide an image for analysis"
                    }
                }
            )

        return task

if __name__ == "__main__":
    agent = ImageAnalysisAgent()
    run_server(agent, port=5004)
```

**Client Usage**:
```python
client = A2AClient("http://localhost:5004")

# Send image for analysis
task = client.send_message({
    "role": "user",
    "content": {
        "type": "image",
        "imageUrl": "https://example.com/landscape.jpg"
    }
})

# Get structured analysis
analysis = task.artifacts[0]['parts'][1]['data']
print(f"Objects detected: {analysis['objects']}")
print(f"Colors: {analysis['dominant_colors']}")
```

## Example 9: Human-in-the-Loop Workflow

```python
from python_a2a import A2AServer, agent, run_server
from python_a2a import TaskStatus, TaskState

@agent(
    name="Approval Agent",
    description="Handles approval workflows with human oversight",
    version="1.0.0"
)
class ApprovalAgent(A2AServer):

    def handle_task(self, task):
        """Process approval requests."""
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "")

        # Parse approval request
        if "approve" in text.lower() and "budget" in text.lower():
            # Extract amount
            import re
            match = re.search(r'\$?([\d,]+)', text)
            if match:
                amount = int(match.group(1).replace(',', ''))

                if amount > 10000:
                    # Requires human approval
                    task.status = TaskStatus(
                        state=TaskState.INPUT_REQUIRED,
                        message={
                            "role": "agent",
                            "content": {
                                "type": "text",
                                "text": f"Budget of ${amount} requires manager approval. "
                                       "Please confirm (yes/no):"
                            }
                        }
                    )
                else:
                    # Auto-approve
                    task.artifacts = [{
                        "parts": [{
                            "type": "text",
                            "text": f"Budget of ${amount} automatically approved"
                        }]
                    }]
                    task.status = TaskStatus(state=TaskState.COMPLETED)
            else:
                task.status = TaskStatus(
                    state=TaskState.FAILED,
                    message={
                        "role": "agent",
                        "content": {"type": "text", "text": "Could not parse amount"}
                    }
                )
        elif text.lower() in ['yes', 'approved', 'confirm']:
            # Human provided approval
            task.artifacts = [{
                "parts": [{"type": "text", "text": "Request approved by manager"}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            task.status = TaskStatus(
                state=TaskState.REJECTED,
                message={
                    "role": "agent",
                    "content": {"type": "text", "text": "Request denied"}
                }
            )

        return task

if __name__ == "__main__":
    agent = ApprovalAgent()
    run_server(agent, port=5005)
```

**Client Workflow**:
```python
client = A2AClient("http://localhost:5005")

# Request budget approval
task = client.ask("Approve budget of $15,000 for marketing campaign")

if task.status.state == "INPUT_REQUIRED":
    # Agent needs human approval
    print(task.status.message['content']['text'])

    # Manager provides approval
    task = client.send_message(
        "yes",
        context_id=task.context_id
    )

    print(task.artifacts[0]['parts'][0]['text'])
    # Output: "Request approved by manager"
```

## Example 10: Error Handling and Retry Logic

```python
import time
from python_a2a import A2AClient

class ResilientA2AClient:
    def __init__(self, agent_url, max_retries=3):
        self.client = A2AClient(agent_url)
        self.max_retries = max_retries

    def send_with_retry(self, message):
        """Send message with exponential backoff retry."""
        for attempt in range(self.max_retries):
            try:
                return self.client.ask(message)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed after {self.max_retries} attempts: {e}")

                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)

# Usage
resilient_client = ResilientA2AClient("http://unreliable-agent.example.com")
response = resilient_client.send_with_retry("Process this request")
print(response)
```

## Best Practices Demonstrated

1. **Clear Skill Definitions**: Use descriptive names and detailed descriptions
2. **Robust Error Handling**: Catch exceptions and return meaningful error states
3. **State Management**: Properly manage task states (WORKING, COMPLETED, FAILED, etc.)
4. **Multi-Modal Support**: Handle different content types (text, images, structured data)
5. **Human-in-the-Loop**: Use INPUT_REQUIRED for human oversight
6. **Async Processing**: Use background threads for long-running tasks
7. **Webhook Integration**: Implement push notifications for async updates
8. **Discovery**: Properly advertise capabilities via Agent Cards
9. **Retry Logic**: Implement exponential backoff for resilience
10. **Orchestration**: Coordinate multiple agents for complex workflows

## Next Steps

- Review [A2A vs MCP comparison](./04-comparison-with-mcp.md) to understand when to use each protocol
- Explore [references](./05-references.md) for official documentation and additional resources
- Build your own custom agents using these examples as templates
- Join the A2A community to share your implementations

## Additional Resources

- **Python SDK Documentation**: [https://python-a2a.readthedocs.io/](https://python-a2a.readthedocs.io/)
- **Google Codelabs**: Interactive A2A tutorials
- **Community Examples**: [https://github.com/a2aproject/a2a-samples](https://github.com/a2aproject/a2a-samples)
