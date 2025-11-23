# Agent-to-Agent (A2A) Protocol

## Overview

The Agent-to-Agent (A2A) Protocol is an open communication standard created by Google (now under the Linux Foundation) that enables AI agents from different vendors and frameworks to discover, communicate, and collaborate with each other.

## Quick Start

### What is A2A?

A2A is a protocol for horizontal agent-to-agent communication that treats agents as "opaque" - preserving privacy and intellectual property while enabling interoperability.

### Core Capabilities

- **Agent Discovery**: Find capable agents via Agent Cards
- **Task Management**: Create, track, and manage long-running tasks
- **Message Exchange**: Structured communication between agents
- **Artifact Sharing**: Exchange documents, images, data
- **Authentication**: OAuth 2.0, API keys, OpenID Connect

### Simple Example

```python
import httpx

client = httpx.AsyncClient()

# Create task on remote agent
response = await client.post(
    "https://agent.example.com/tasks",
    json={"description": "Track shipment #12345"}
)

task_id = response.json()["task_id"]

# Send message
await client.post(
    f"https://agent.example.com/tasks/{task_id}/messages",
    json={
        "role": "user",
        "parts": [{"type": "text", "content": "Provide ETA"}]
    }
)
```

## Contents

1. [First Principles](./01-first-principles.md)
2. [Architecture](./02-architecture.md)
3. [Code Examples](./03-examples.md)
4. [Comparison with MCP](./04-comparison-with-mcp.md)
5. [References](./05-references.md)

## Key Differences from MCP

- **A2A**: Agent↔Agent (horizontal, peer-to-peer)
- **MCP**: Agent↔Tool (vertical, client-server)

They're complementary, not competing!

## Official Resources

- [A2A Protocol Website](https://a2a-protocol.org/latest/)
- [A2A Specification](https://a2a-protocol.org/latest/specification/)
- [Google Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
