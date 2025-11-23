# A2A Code Examples

## Python Examples

### Example 1: Simple Agent Client

```python
import httpx
import asyncio
from typing import Dict, Any

class A2AClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.client = httpx.AsyncClient()
    
    async def send_message(self, message: str, session_id: str = None) -> Dict:
        """Send a message to the agent"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "session_id": session_id,
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "content": message}]
                }
            }
        }
        
        response = await self.client.post(
            f"{self.base_url}/a2a",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    async def get_task(self, task_id: str) -> Dict:
        """Get task status"""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "task/get",
            "params": {"task_id": task_id}
        }
        
        response = await self.client.post(
            f"{self.base_url}/a2a",
            json=payload,
            headers=self.headers
        )
        return response.json()

# Usage
async def main():
    client = A2AClient(
        "https://api.example.com",
        "your-api-key"
    )
    
    # Send message
    result = await client.send_message(
        "Track shipment #12345",
        session_id="session-xyz"
    )
    print(result)

asyncio.run(main())
```

### Example 2: Multi-Agent Orchestration

```python
import httpx
import asyncio
from typing import List, Dict

class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.client = httpx.AsyncClient()
    
    def register_agent(self, name: str, url: str, api_key: str):
        """Register an agent"""
        self.agents[name] = {
            "url": url,
            "headers": {"Authorization": f"Bearer {api_key}"}
        }
    
    async def delegate_task(
        self,
        agent_name: str,
        description: str,
        context: Dict = None
    ) -> str:
        """Delegate a task to a specific agent"""
        agent = self.agents[agent_name]
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "task/create",
            "params": {
                "description": description,
                "context": context or {}
            }
        }
        
        response = await self.client.post(
            f"{agent['url']}/a2a",
            json=payload,
            headers=agent["headers"]
        )
        
        return response.json()["result"]["task_id"]
    
    async def wait_for_completion(
        self,
        agent_name: str,
        task_id: str,
        timeout: int = 60
    ) -> Dict:
        """Wait for task completion"""
        agent = self.agents[agent_name]
        start_time = asyncio.get_event_loop().time()
        
        while True:
            # Check if timeout
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Task {task_id} timeout")
            
            # Get task status
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "task/get",
                "params": {"task_id": task_id}
            }
            
            response = await self.client.post(
                f"{agent['url']}/a2a",
                json=payload,
                headers=agent["headers"]
            )
            
            task = response.json()["result"]
            
            if task["status"] == "completed":
                return task
            elif task["status"] == "failed":
                raise Exception(f"Task failed: {task.get('error')}")
            
            # Wait before polling again
            await asyncio.sleep(2)
    
    async def orchestrate_workflow(self, user_query: str) -> str:
        """Orchestrate multi-agent workflow"""
        
        # Step 1: Research agent gathers information
        research_task_id = await self.delegate_task(
            "research",
            f"Research: {user_query}"
        )
        research_result = await self.wait_for_completion(
            "research",
            research_task_id
        )
        
        # Step 2: Analysis agent processes research
        analysis_task_id = await self.delegate_task(
            "analysis",
            "Analyze research findings",
            context={"research": research_result["artifacts"]}
        )
        analysis_result = await self.wait_for_completion(
            "analysis",
            analysis_task_id
        )
        
        # Step 3: Writing agent creates final report
        writing_task_id = await self.delegate_task(
            "writing",
            "Create final report",
            context={"analysis": analysis_result["artifacts"]}
        )
        final_result = await self.wait_for_completion(
            "writing",
            writing_task_id
        )
        
        return final_result["artifacts"][0]["content"]

# Usage
async def main():
    orchestrator = AgentOrchestrator()
    
    # Register agents
    orchestrator.register_agent(
        "research",
        "https://research-agent.example.com",
        "research-api-key"
    )
    orchestrator.register_agent(
        "analysis",
        "https://analysis-agent.example.com",
        "analysis-api-key"
    )
    orchestrator.register_agent(
        "writing",
        "https://writing-agent.example.com",
        "writing-api-key"
    )
    
    # Run workflow
    result = await orchestrator.orchestrate_workflow(
        "Impact of AI on healthcare"
    )
    print(result)

asyncio.run(main())
```

### Example 3: Agent Server Implementation

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
from datetime import datetime

app = FastAPI()

# In-memory task storage
tasks: Dict[str, Dict] = {}

class Message(BaseModel):
    role: str
    parts: List[Dict]

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int
    method: str
    params: Dict

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Serve Agent Card"""
    return {
        "id": "shipping-agent-001",
        "name": "Shipping Tracker",
        "description": "Track shipments across multiple carriers",
        "version": "1.0.0",
        "endpoint": "https://api.example.com/a2a",
        "capabilities": [
            "track_shipment",
            "estimate_delivery",
            "update_address"
        ],
        "authentication": {
            "type": "bearer",
            "description": "API key authentication"
        }
    }

@app.post("/a2a")
async def handle_rpc(request: JsonRpcRequest):
    """Handle JSON-RPC requests"""
    
    method = request.method
    params = request.params
    
    if method == "message/send":
        return handle_message_send(request.id, params)
    elif method == "task/get":
        return handle_task_get(request.id, params)
    elif method == "task/cancel":
        return handle_task_cancel(request.id, params)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown method: {method}"
        )

def handle_message_send(rpc_id: int, params: Dict):
    """Handle message/send"""
    message = params["message"]
    user_message = message["parts"][0]["content"]
    
    # Create task
    task_id = f"task-{uuid.uuid4()}"
    tasks[task_id] = {
        "task_id": task_id,
        "status": "working",
        "created_at": datetime.utcnow().isoformat(),
        "messages": [message]
    }
    
    # Process message (simplified)
    response_text = process_shipment_query(user_message)
    
    # Update task
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["artifacts"] = [{
        "type": "text",
        "content": response_text
    }]
    
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": {
            "message": {
                "role": "agent",
                "parts": [{
                    "type": "text",
                    "content": response_text
                }]
            },
            "task_id": task_id
        }
    }

def handle_task_get(rpc_id: int, params: Dict):
    """Handle task/get"""
    task_id = params["task_id"]
    
    if task_id not in tasks:
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {
                "code": -32001,
                "message": "Task not found"
            }
        }
    
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": tasks[task_id]
    }

def handle_task_cancel(rpc_id: int, params: Dict):
    """Handle task/cancel"""
    task_id = params["task_id"]
    
    if task_id not in tasks:
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {
                "code": -32001,
                "message": "Task not found"
            }
        }
    
    tasks[task_id]["status"] = "canceled"
    
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": {"success": True}
    }

def process_shipment_query(query: str) -> str:
    """Process shipment tracking query"""
    # Simplified implementation
    if "track" in query.lower():
        return "Shipment is in transit. ETA: January 17, 2025"
    elif "estimate" in query.lower():
        return "Estimated delivery: 2-3 business days"
    else:
        return "How can I help with your shipment?"

# Run with: uvicorn server:app --host 0.0.0.0 --port 8000
```

## Comparison: A2A vs MCP

### When to Use Each

```python
# Use MCP for tool access
from mcp.client import Client

mcp_client = Client(connection)
await mcp_client.call_tool(
    "query_database",
    {"sql": "SELECT * FROM users"}
)

# Use A2A for agent collaboration
a2a_client = A2AClient(url, api_key)
await a2a_client.send_message(
    "Please analyze the user data and provide insights"
)
```

### Combined Usage

```python
class HybridAgent:
    """Agent that uses both MCP (for tools) and A2A (for collaboration)"""
    
    def __init__(self):
        # MCP for data access
        self.mcp_client = Client(mcp_connection)
        
        # A2A for agent delegation
        self.a2a_client = A2AClient(url, api_key)
    
    async def process_customer_query(self, query: str):
        # Use MCP to get customer data
        customer_data = await self.mcp_client.call_tool(
            "get_customer",
            {"query": query}
        )
        
        # Use A2A to delegate to specialist
        if "shipping" in query:
            return await self.a2a_client.send_message(
                f"Handle shipping query for {customer_data}"
            )
        elif "billing" in query:
            return await self.a2a_client.send_message(
                f"Handle billing query for {customer_data}"
            )
```
