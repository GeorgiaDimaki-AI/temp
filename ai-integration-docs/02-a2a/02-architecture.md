# A2A Architecture & Technical Design

## Protocol Design

A2A uses **JSON-RPC 2.0 over HTTPS** for communication.

### Why JSON-RPC 2.0 over HTTP?

1. **Standardized**: Well-understood protocol
2. **Interoperable**: Works with any HTTP client
3. **Firewall-friendly**: Uses standard HTTP/HTTPS ports
4. **Scalable**: Leverages HTTP infrastructure
5. **Secure**: TLS encryption, standard auth

## Core Components

```
┌──────────────────┐         ┌──────────────────┐
│   Client Agent   │         │   Remote Agent   │
│                  │         │                  │
│  ┌────────────┐  │         │  ┌────────────┐  │
│  │  A2A Client│  │         │  │ A2A Server │  │
│  └──────┬─────┘  │         │  └──────┬─────┘  │
└─────────┼────────┘         └─────────┼────────┘
          │                            │
          │   HTTP/HTTPS (JSON-RPC)    │
          └────────────────────────────┘
```

### Agent Card

**JSON metadata describing agent capabilities**:

```json
{
  "id": "agent-123",
  "name": "Shipping Tracker",
  "description": "Track shipments across multiple carriers",
  "capabilities": ["track_shipment", "estimate_delivery", "update_address"],
  "version": "1.0.0",
  "endpoint": "https://api.example.com/a2a",
  "authentication": {
    "type": "oauth2",
    "authorization_endpoint": "https://auth.example.com/authorize",
    "token_endpoint": "https://auth.example.com/token"
  },
  "metadata": {
    "supported_carriers": ["UPS", "FedEx", "USPS"],
    "rate_limit": "100/hour"
  }
}
```

## Task Lifecycle

### Task States

```
submitted → working → completed
    │          │
    ↓          ↓
input_required ← ─ → paused
    │          │
    ↓          ↓
  failed    canceled
```

**States**:
- `submitted`: Task created, not started
- `working`: Agent actively processing
- `input_required`: Needs human/external input
- `paused`: Temporarily suspended
- `completed`: Successfully finished
- `failed`: Error occurred
- `canceled`: Explicitly canceled

### Task Structure

```json
{
  "task_id": "task-abc-123",
  "status": "working",
  "description": "Track shipment #12345",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:05:00Z",
  "context": {
    "user_id": "user-789",
    "priority": "high"
  },
  "artifacts": [],
  "messages": []
}
```

## Core Methods

### 1. `message/send`

Send a message to an agent (creates task if needed):

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "session_id": "session-xyz",
    "message": {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "content": "Track shipment #12345"
        }
      ]
    }
  }
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "message": {
      "role": "agent",
      "parts": [
        {
          "type": "text",
          "content": "Shipment is in transit, ETA: Jan 17"
        }
      ]
    }
  }
}
```

### 2. `task/get`

Retrieve task status:

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "task/get",
  "params": {
    "task_id": "task-abc-123"
  }
}
```

### 3. `task/cancel`

Cancel a running task:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "task/cancel",
  "params": {
    "task_id": "task-abc-123"
  }
}
```

### 4. `task/subscribe`

Subscribe to task updates (push notifications):

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "task/subscribe",
  "params": {
    "task_id": "task-abc-123",
    "webhook_url": "https://client.com/webhook"
  }
}
```

## Communication Patterns

### Synchronous

Simple request-response:

```
Client → Server: message/send
Client ← Server: immediate response
```

### Streaming (SSE)

Server-sent events for real-time updates:

```
Client → Server: message/send (with stream=true)
Client ← Server: SSE stream with updates
           data: {"status": "working"}
           data: {"status": "completed", "result": "..."}
```

### Asynchronous (Webhooks)

Long-running tasks with push notifications:

```
Client → Server: task/subscribe
Client ← Server: acknowledgment

... later ...

Client ← Server: webhook notification
         {"task_id": "...", "status": "completed"}
```

## Authentication & Authorization

### Supported Methods

1. **API Keys**
   ```
   Authorization: Bearer <api_key>
   ```

2. **OAuth 2.0**
   ```
   Authorization: Bearer <access_token>
   ```

3. **OpenID Connect**
   - Identity verification
   - User context

4. **Mutual TLS**
   - Certificate-based auth
   - High security scenarios

### OAuth Flow

```
1. Client discovers auth endpoints from Agent Card
2. Client initiates OAuth flow
3. User authorizes access
4. Client receives access token
5. Client includes token in API requests
6. Server validates token
7. Access granted/denied
```

## Message Structure

### Parts

Messages consist of "parts" for multimodal content:

```json
{
  "role": "user",
  "parts": [
    {
      "type": "text",
      "content": "Analyze this image"
    },
    {
      "type": "image",
      "url": "https://example.com/image.jpg",
      "mimeType": "image/jpeg"
    }
  ]
}
```

### Artifacts

Outputs generated by agents:

```json
{
  "id": "artifact-001",
  "type": "document",
  "name": "Report.pdf",
  "mimeType": "application/pdf",
  "url": "https://storage.example.com/report.pdf",
  "size": 1024000
}
```

## Design Patterns

### Triage → Specialist

```
Customer Query
    ↓
Triage Agent (determines intent)
    ├─→ Billing Agent
    ├─→ Technical Support Agent
    ├─→ Shipping Agent
    └─→ Returns Agent
```

### Sequential Orchestration

```
Research Agent
    ↓ (passes findings)
Analysis Agent
    ↓ (passes analysis)
Writing Agent
    ↓ (produces final output)
Final Report
```

### Parallel Execution

```
User Query
    ├─→ Agent A (data source 1)
    ├─→ Agent B (data source 2)
    └─→ Agent C (data source 3)
         ↓ (all results combined)
    Synthesis Agent
```

## Error Handling

### Standard Error Codes

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "Task not found",
    "data": {
      "task_id": "task-invalid"
    }
  }
}
```

**Error codes**:
- `-32000`: Agent error
- `-32001`: Task not found
- `-32002`: Authentication failed
- `-32003`: Rate limit exceeded
- `-32004`: Invalid input

## Performance Considerations

### Connection Reuse

```python
# Maintain persistent HTTP session
session = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(max_connections=100)
)
```

### Batch Operations

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "batch",
  "params": {
    "operations": [
      {"method": "task/get", "params": {"task_id": "task-1"}},
      {"method": "task/get", "params": {"task_id": "task-2"}},
      {"method": "task/get", "params": {"task_id": "task-3"}}
    ]
  }
}
```

### Caching Agent Cards

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_agent_card(agent_url: str):
    # Cache for 1 hour
    return fetch_agent_card(agent_url)
```
