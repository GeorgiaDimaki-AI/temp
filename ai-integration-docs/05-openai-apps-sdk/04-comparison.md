# Apps SDK Comparison

## Apps SDK vs Other Frameworks

### Apps SDK vs Agents SDK (OpenAI)

| Aspect | Apps SDK | Agents SDK |
|--------|----------|------------|
| **Purpose** | UI apps in ChatGPT | Multi-agent backends |
| **Where it runs** | ChatGPT interface | Your server |
| **UI** | Rich widgets (HTML/JS) | No UI (backend only) |
| **User access** | 800M+ ChatGPT users | Your application users |
| **Discovery** | Organic (ChatGPT suggests) | Manual integration |
| **Best for** | Consumer-facing features | Business logic orchestration |

**Use Apps SDK when:**
- You want distribution to ChatGPT users
- Need interactive UI (maps, forms, charts)
- Building transactional services

**Use Agents SDK when:**
- Building backend agent orchestration
- Need complex multi-agent workflows
- Don't need UI in ChatGPT

**Can combine both:**
```
ChatGPT App (Apps SDK)
    ↓ calls backend
Your Server (Agents SDK)
    ↓ orchestrates
Multiple specialized agents
```

### Apps SDK vs MCP

| Aspect | Apps SDK | MCP |
|--------|----------|-----|
| **Layer** | Application + UI | Protocol only |
| **Scope** | ChatGPT-specific | Universal standard |
| **UI** | Rich widgets | No UI concept |
| **Foundation** | Built on MCP | Protocol specification |
| **Portability** | ChatGPT only | Works everywhere |

**Relationship:**

Apps SDK **uses** MCP as its foundation:
- MCP provides tool protocol
- Apps SDK adds UI layer on top
- Apps SDK is "MCP + widgets + ChatGPT integration"

**Migration path:**
```python
# Pure MCP server works with Apps SDK
@mcp.tool()
def my_tool():
    return {
        "content": "text for model",
        "structuredContent": {...},  # For widget
        "_meta": {
            "openai/outputTemplate": "ui://widget/my-widget.html"
        }
    }
```

### Apps SDK vs A2A

| Aspect | Apps SDK | A2A |
|--------|----------|-----|
| **Purpose** | UI apps for users | Agent-to-agent communication |
| **Users** | Humans (ChatGPT) | Other AI agents |
| **UI** | Rich widgets | No UI |
| **Communication** | User ↔ ChatGPT ↔ Backend | Agent ↔ Agent |
| **Discovery** | ChatGPT suggests | Agent Cards |

**Different use cases:**
- **Apps SDK**: Human-facing applications
- **A2A**: Agent collaboration

**Can be combined:**
```
User → ChatGPT (Apps SDK app)
           ↓
    Your Agent (A2A client)
           ↓ delegates via A2A
    Specialist Agent (external)
```

### Apps SDK vs Claude Agent SDK

| Aspect | Apps SDK | Claude Agent SDK |
|--------|----------|------------------|
| **Vendor** | OpenAI | Anthropic |
| **Where** | Inside ChatGPT | Your server |
| **UI** | Rich widgets | No built-in UI |
| **Distribution** | ChatGPT's 800M users | Your deployment |
| **Context** | Conversation-based | Long-running (hours) |
| **Tools** | MCP-based | Built-in + MCP |

**Different niches:**
- **Apps SDK**: Consumer apps in ChatGPT
- **Agent SDK**: Sophisticated autonomous agents

**Complementary:**
Your ChatGPT app (Apps SDK) can call backend powered by Agent SDK.

## Decision Matrix

### Choose Apps SDK When:

✅ You want distribution to ChatGPT users (800M+)
✅ Need rich, interactive UI (maps, charts, forms)
✅ Building transactional services (booking, ordering)
✅ Want organic discovery (ChatGPT suggests your app)
✅ Need minimal infrastructure (MCP server only)

❌ Avoid Apps SDK when:
- Need fine-grained control over UI
- Want multi-page workflows
- Building internal tools (no need for ChatGPT distribution)
- Need sensitive data display
- Require complex authentication flows

### Alternative Choices

**For internal tools:** Claude Agent SDK or custom agent
**For agent orchestration:** OpenAI Agents SDK or LangGraph
**For universal tools:** Pure MCP servers
**For agent networks:** A2A protocol

## Combined Architecture Example

### Multi-Layer System

```
┌─────────────────────────────────────────┐
│  User facing: ChatGPT App (Apps SDK)    │
│  - Rich UI for users                    │
│  - 800M user distribution               │
└─────────────────┬───────────────────────┘
                  │ MCP calls
┌─────────────────▼───────────────────────┐
│  Backend: Agent Orchestrator            │
│  (OpenAI Agents SDK or Agent SDK)       │
│  - Business logic                       │
│  - Multi-agent coordination             │
└─────────────────┬───────────────────────┘
                  │ Uses MCP for tools
          ┌───────┼───────┐
          ▼       ▼       ▼
    ┌─────────┬──────┬─────────┐
    │Database │Email │ API     │ (MCP Servers)
    └─────────┴──────┴─────────┘
                  │ Uses A2A for collaboration
                  ▼
    ┌─────────────────────────┐
    │ External Partner Agents │ (A2A)
    └─────────────────────────┘
```

**Benefits:**
- **User layer**: ChatGPT distribution + rich UI
- **Orchestration**: Sophisticated agent logic
- **Tools**: Reusable MCP integrations
- **Collaboration**: Partner agent integration

## Real-World Examples

### E-commerce Platform

```
ChatGPT App (Apps SDK)
├─ Product search with visual grid
├─ Interactive cart management
├─ Booking and checkout
└─ Order tracking with live updates

Backend (Agents SDK)
├─ Inventory management
├─ Payment processing
├─ Order fulfillment
└─ Shipping coordination (via A2A to carrier agents)

Tools (MCP)
├─ Product database
├─ Payment gateway
├─ Email notifications
└─ CRM integration
```

### Customer Support

```
ChatGPT App (Apps SDK)
├─ Interactive FAQ widget
├─ Ticket submission form
├─ Live status tracking
└─ Knowledge base search

Backend (Agent SDK)
├─ Triage and classification
├─ Knowledge retrieval
├─ Escalation handling
└─ Specialist delegation (via A2A)

Tools (MCP)
├─ Ticketing system
├─ Knowledge base
├─ Customer database
└─ Email/Slack integration
```

## Migration Strategies

### From Pure MCP to Apps SDK

**Step 1:** Build MCP server (works everywhere)
```python
@mcp.tool()
def my_tool(args):
    return {"content": "result"}
```

**Step 2:** Add structured content
```python
@mcp.tool()
def my_tool(args):
    return {
        "content": "result",
        "structuredContent": {...}  # Data for widget
    }
```

**Step 3:** Add widget
```python
@mcp.tool()
def my_tool(args):
    return {
        "content": "result",
        "structuredContent": {...},
        "_meta": {
            "openai/outputTemplate": "ui://widget/my-widget.html"
        }
    }
```

**Benefit:** MCP server still works with other clients!

### From Agents SDK to Apps SDK

Keep agents backend, add ChatGPT frontend:

```
Before:
User App → Agents SDK Backend

After:
ChatGPT (Apps SDK) → MCP Adapter → Agents SDK Backend
```

## Summary

**Apps SDK fills a specific niche:**
- **What**: Rich UI apps in ChatGPT
- **Who**: Consumer-facing features
- **Why**: 800M user distribution + organic discovery
- **How**: MCP backend + HTML widgets

**Best used with:**
- MCP for tool integration
- Agents SDK for backend orchestration
- A2A for agent collaboration

**Not a replacement for:**
- Backend agent frameworks
- Custom UIs with full control
- Internal enterprise tools

The power comes from combining technologies at appropriate layers!
