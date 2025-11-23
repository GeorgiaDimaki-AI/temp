# OpenAI Apps SDK: Comprehensive Research Report

## Executive Summary

This report provides an in-depth analysis of OpenAI's Apps SDK and related application development frameworks, exploring the evolution of OpenAI's approach to building AI-powered applications from first principles. The Apps SDK represents OpenAI's latest evolution in extensibility, moving from ChatGPT Plugins (2023) to Custom GPTs (2023-2024) to fully-featured apps with graphical interfaces integrated directly into ChatGPT conversations (2025).

---

## 1. What is the Apps SDK and Why Was It Created (First Principles)

### Definition

The **OpenAI Apps SDK** is a developer toolkit that enables building interactive applications that run directly inside ChatGPT conversations. It extends the Model Context Protocol (MCP) to allow developers to design both the backend logic and frontend interface of applications that integrate seamlessly with ChatGPT.

### Historical Evolution: The Path to Apps SDK

OpenAI's approach to application extensibility has evolved through three distinct phases:

#### **Phase 1: ChatGPT Plugins (March 2023 - April 2024)**
- Launched in March 2023 as the first extensibility mechanism
- Plugins were tools designed specifically for language models with safety as a core principle
- Helped ChatGPT access up-to-date information, run computations, or use third-party services
- **Limitation**: Required separate installation, limited UI customization, and created friction in user experience
- Deprecated March 19, 2024; existing conversations ended April 9, 2024

#### **Phase 2: GPTs and GPT Store (November 2023 - January 2024)**
- Announced at Developer Day 2023 as "GPTs" – chatbots customized for specific tasks or domains
- GPT Store debuted January 2024 with ~3 million custom GPTs created
- **Advancement**: Broader capabilities than plugins, easier to create, integrated marketplace
- **Limitation**: Still primarily conversational, limited interactive UI elements

#### **Phase 3: Apps SDK (October 2025 - Present)**
- Announced October 2025 in preview mode
- Represents a fundamental shift to full-featured apps with rich, interactive graphical interfaces
- Built on the open-source Model Context Protocol (MCP) standard
- **Key Innovation**: Native integration of web components rendered in iframes within ChatGPT

### First Principles: Why Apps SDK Exists

The Apps SDK was created to address fundamental limitations in how AI applications are built and distributed:

#### **1. The Distribution Problem**
**Traditional Model**: Users must discover, download, and install standalone apps, creating significant friction.

**Apps SDK Solution**: Users find apps organically when ChatGPT determines the app can solve their problem, eliminating downloads and installations. With over 800 million ChatGPT users, developers gain instant reach.

#### **2. The Integration Problem**
**Traditional Model**: Applications exist separately from conversational AI, requiring context switching and manual data transfer.

**Apps SDK Solution**: Apps are "conversation-native" – they fit naturally into dialogue, maintain context automatically, and blend conversational flows with interactive interfaces.

#### **3. The Platform Vision**
**Strategic Intent**: Transform ChatGPT from a chatbot into a "chat-driven operating system" where apps are native capabilities rather than external tools.

As described in the announcement: "This isn't just another API – it's OpenAI's play to become a chat-driven operating system. ChatGPT becomes a chat-driven operating system, and your app is one of its capabilities."

#### **4. The Standardization Problem**
**Technical Foundation**: Built on MCP (Model Context Protocol), an open standard ensuring apps can run anywhere that adopts this protocol, not just ChatGPT.

**Philosophy**: By making the SDK open-source and standards-based, OpenAI enables broader ecosystem adoption while maintaining interoperability.

---

## 2. The Core Problem It Solves

### Primary Problem: AI Application Extensibility with Native UX

The Apps SDK solves the fundamental challenge of **extending AI capabilities with custom logic and interactive interfaces while maintaining a seamless, conversation-native user experience**.

### Specific Problems Addressed:

#### **A. Context Persistence and Management**
**Problem**: In traditional web apps, developers must manually manage conversation state, handle context window limits, and maintain session history.

**Solution**: The Apps SDK, through its MCP foundation and integration with ChatGPT, automatically handles:
- Conversation history maintenance
- Context window management
- State persistence across interactions via `window.openai.setWidgetState`

#### **B. Discoverability**
**Problem**: Users don't know what tools are available or when to use them.

**Solution**: ChatGPT suggests apps contextually based on:
- Natural language understanding of user intent
- Tool metadata and descriptions
- Current conversation context
- Apps can also be invoked by name

#### **C. Interactive Data Presentation**
**Problem**: Pure conversational interfaces struggle with rich data visualization, complex forms, and interactive controls.

**Solution**: Apps can render custom web components (React, Vue, vanilla JS) as:
- **Inline cards**: Compact summaries with key information
- **Fullscreen views**: Complex interfaces for detailed interactions
- **Interactive widgets**: Maps, playlists, presentations, forms, etc.

#### **D. Tool Integration Standardization**
**Problem**: Every AI platform has different APIs for tool calling, authentication, and data exchange.

**Solution**: MCP provides a standardized protocol for:
- Tool discovery and registration
- JSON Schema-based input/output contracts
- OAuth 2.1 authentication flows
- Consistent behavior across platforms

#### **E. Real-time Bi-directional Communication**
**Problem**: Traditional plugins or extensions lack real-time, bidirectional communication between UI, backend, and AI model.

**Solution**: The Apps SDK architecture enables:
- Model invokes tools based on conversation
- UI receives structured data via `window.openai.toolOutput`
- UI can trigger backend tools via `window.openai.callTool`
- Persistent state flows throughout conversation

---

## 3. How It Works Technically

### Architecture Overview

The Apps SDK consists of **three interconnected layers** that work together:

```
┌─────────────────────────────────────────────────────────┐
│                    ChatGPT (Client)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Conversation Interface                    │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │   Sandboxed Widget (iframe)                │  │  │
│  │  │   - HTML/CSS/JS (React, Vue, etc.)         │  │  │
│  │  │   - window.openai globals                  │  │  │
│  │  │   - Renders interactive UI                 │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↕                              │
│              Model Context Protocol (MCP)              │
│                          ↕                              │
└─────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────┐
│              MCP Server (Your Backend)                  │
│  - Defines tools with JSON Schema                      │
│  - Handles authentication & authorization               │
│  - Returns structured data + metadata                   │
│  - References UI component templates                    │
└─────────────────────────────────────────────────────────┘
```

### Three Core Components

#### **1. Web Component (Frontend/UI Layer)**

A web component built with any framework (React, Vue, Svelte, vanilla JS) that renders in a sandboxed iframe within ChatGPT.

**Key Characteristics:**
- Built with standard web technologies (HTML, CSS, JavaScript)
- Runs in a sandboxed iframe for security
- Accesses data and APIs via `window.openai` globals
- Can be inline (compact cards) or fullscreen (complex interfaces)

**window.openai API Reference:**

| Property/Method | Type | Purpose |
|----------------|------|---------|
| `toolOutput` | Object | Latest tool response data (structuredContent) |
| `toolResponseMetadata` | Object | Metadata exclusively for widget (_meta) |
| `widgetState` | Object | Persisted UI state across conversation |
| `setWidgetState(state)` | Function | Synchronously store new UI state snapshots |
| `callTool(name, args)` | Function | Invoke backend tools from widget |
| `requestModal` | Function | Spawn ChatGPT-owned modal overlays |
| `displayMode` | String | Current display context (inline/fullscreen) |
| `theme` | String | UI theme (light/dark) |

**Example widget integration:**
```javascript
// Access tool response data
const data = window.openai.toolOutput;

// Persist widget state
window.openai.setWidgetState({ selectedTab: 'map', filters: {...} });

// Call backend tool from UI
await window.openai.callTool('refresh_data', { location: 'NYC' });
```

#### **2. MCP Server (Backend/Logic Layer)**

An HTTP server implementing the Model Context Protocol that:
- Exposes tools (functions/capabilities)
- Handles tool invocations
- Returns structured data and UI references
- Manages authentication and business logic

**MCP Server Capabilities:**

1. **List Tools** – Advertise available tools with JSON Schema contracts
2. **Execute Tools** – Process tool invocations and return results
3. **Register Resources** – Serve UI templates and components

**Tool Response Structure:**
```json
{
  "content": "User-facing narration for the model",
  "structuredContent": {
    // Data that both widget AND model can read
    "items": [...],
    "summary": "..."
  },
  "_meta": {
    "openai/outputTemplate": "ui://widget/component.html",
    "openai/widgetData": {
      // Large or sensitive data ONLY for widget
      // Never sent to the model
    }
  }
}
```

**Three-Part Response Pattern:**

| Component | Visibility | Purpose |
|-----------|-----------|---------|
| `content` | Model only | Natural language narration |
| `structuredContent` | Model + Widget | Core data used by both |
| `_meta` | Widget only | Large datasets, sensitive info |

#### **3. Model Layer (AI Orchestration)**

ChatGPT's model determines when to invoke tools based on:
- Natural language understanding of user intent
- Tool metadata and descriptions (`openai/toolInvocation/*` annotations)
- Conversation context
- Tool input/output schemas

**Tool Metadata Annotations:**
```json
{
  "name": "get_restaurants",
  "description": "Find restaurants near a location",
  "inputSchema": { /* JSON Schema */ },
  "_meta": {
    "openai/outputTemplate": "ui://widget/restaurant-card.html",
    "openai/toolInvocation/invoking": "Searching for restaurants...",
    "openai/toolInvocation/invoked": "Found {count} restaurants",
    "openai/widgetAccessible": true  // Enables window.openai.callTool
  }
}
```

### Technical Data Flow

**1. User makes a request in ChatGPT**
```
User: "Find Italian restaurants near me in Brooklyn"
```

**2. Model reasons about intent and selects tool**
```
Model determines: Use 'search_restaurants' tool
Parameters: { cuisine: "Italian", location: "Brooklyn" }
```

**3. ChatGPT invokes MCP server tool**
```
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_restaurants",
    "arguments": { "cuisine": "Italian", "location": "Brooklyn" }
  }
}
```

**4. MCP server processes request**
```python
@mcp.tool()
async def search_restaurants(cuisine: str, location: str):
    """Search for restaurants by cuisine and location"""
    results = await restaurant_api.search(cuisine, location)

    return {
        "content": f"Found {len(results)} {cuisine} restaurants in {location}",
        "structuredContent": {
            "restaurants": [r.summary() for r in results],
            "count": len(results)
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/restaurant-list.html",
            "openai/widgetData": {
                "detailed_results": [r.full_details() for r in results]
            }
        }
    }
```

**5. ChatGPT renders widget**
```
ChatGPT:
- Displays natural language response: "Found 12 Italian restaurants in Brooklyn"
- Loads widget iframe with restaurant-list.html
- Injects toolOutput and metadata into window.openai
- Widget renders interactive map + list
```

**6. User interacts with widget**
```javascript
// Widget code
document.getElementById('filter-btn').addEventListener('click', async () => {
    // Widget calls backend to refine results
    const refined = await window.openai.callTool('filter_restaurants', {
        priceRange: [2, 3],
        rating: 4.5
    });
});
```

### Transport and Protocol

**MCP Protocol Details:**
- Based on **JSON-RPC 2.0** specification
- Supports **Server-Sent Events (SSE)** and **Streamable HTTP** transports
- **Recommended**: Streamable HTTP for production deployments

**Authentication:**
- Built-in OAuth 2.1 flows
- Protected resource metadata
- Token-based authentication for user-specific data

---

## 4. Key Concepts and Architecture

### Core Architectural Principles

#### **1. Conversation-Native Design**
Apps are designed to feel like natural extensions of conversation, not separate applications:
- **Natural language is the primary interface**: Users describe intent, not specific commands
- **Contextual discovery**: ChatGPT suggests apps when relevant
- **Inline integration**: Apps render within chat history, maintaining conversational flow

#### **2. Sandboxed Widget Runtime**
Security and isolation through iframe sandboxing:
- **Content Security Policy (CSP)**: Restrict network access via `openai/widgetCSP`
- **No direct DOM access**: Widgets cannot access ChatGPT's DOM
- **Explicit API surface**: All communication through `window.openai`
- **State isolation**: Widget state is scoped per message/widget instance

#### **3. MCP as Connective Tissue**
Model Context Protocol standardizes all communication:
- **Self-describing**: Tools advertise capabilities and schemas
- **Wire format standardization**: Consistent JSON-RPC 2.0 protocol
- **Authentication standardization**: OAuth 2.1 built-in
- **Metadata extensibility**: Custom annotations for OpenAI-specific features

#### **4. Three-Layer Architecture**

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: PRESENTATION (What users see)             │
│  - Widget UI (HTML/CSS/JS in iframe)                │
│  - Inline cards vs fullscreen views                 │
│  - Interactive elements (maps, forms, charts)       │
└─────────────────────────────────────────────────────┘
                        ↕ window.openai
┌─────────────────────────────────────────────────────┐
│  LAYER 2: PROTOCOL (How they communicate)           │
│  - Model Context Protocol (MCP)                     │
│  - JSON-RPC 2.0 transport                           │
│  - Tool discovery & invocation                      │
└─────────────────────────────────────────────────────┘
                        ↕ HTTP/SSE
┌─────────────────────────────────────────────────────┐
│  LAYER 3: LOGIC (What they do)                      │
│  - MCP server (Node.js, Python, etc.)               │
│  - Business logic & data access                     │
│  - Authentication & authorization                   │
└─────────────────────────────────────────────────────┘
```

### Key Concepts

#### **Templates (UI Resources)**

Templates are MCP resources that define widget entry points:

```typescript
server.registerResource(
  "restaurant-widget",                    // Resource name
  "ui://widget/restaurant-list.html",     // URI
  {},                                      // Metadata
  async () => ({
    contents: [{
      uri: "ui://widget/restaurant-list.html",
      mimeType: "text/html+skybridge",    // Special MIME type for widgets
      text: `
        <!DOCTYPE html>
        <html>
          <head>
            <style>/* Inline styles */</style>
          </head>
          <body>
            <div id="app"></div>
            <script>
              // Access data from window.openai.toolOutput
              const restaurants = window.openai.toolOutput.restaurants;
              // Render UI
            </script>
          </body>
        </html>
      `
    }]
  })
);
```

**Template Requirements:**
- Must use `mimeType: "text/html+skybridge"` to signal ChatGPT
- Should inline all assets (CSS, JS, images) for self-contained deployment
- Can reference external resources if allowed by CSP
- Should handle both connected (ChatGPT) and disconnected (local dev) states

#### **Tools (Capabilities)**

Tools are functions exposed via MCP that the model can invoke:

```python
from fastmcp import FastMCP

mcp = FastMCP("restaurant-app")

@mcp.tool()
async def search_restaurants(
    cuisine: str,
    location: str,
    price_range: tuple[int, int] = (1, 4)
) -> dict:
    """
    Search for restaurants by cuisine, location, and price range.

    Args:
        cuisine: Type of cuisine (e.g., "Italian", "Mexican")
        location: City or neighborhood name
        price_range: Price level tuple (1-4, where 1=$, 4=$$$$)

    Returns:
        Restaurant search results with details and map
    """
    results = await db.query_restaurants(cuisine, location, price_range)

    return {
        "content": f"Found {len(results)} {cuisine} restaurants",
        "structuredContent": {
            "restaurants": [r.to_dict() for r in results]
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/restaurant-list.html",
            "openai/toolInvocation/invoking": "Searching restaurants...",
            "openai/toolInvocation/invoked": f"Found {len(results)} options",
            "openai/widgetAccessible": True
        }
    }
```

**Tool Design Best Practices:**
- **Idempotent**: Model may retry calls, design for safe re-execution
- **Descriptive metadata**: Help model understand when to use the tool
- **Focused scope**: One clear purpose per tool
- **Type hints**: Enable automatic JSON Schema generation (Python)

#### **Widget State Management**

State can be persisted across conversation turns:

```javascript
// Save state
window.openai.setWidgetState({
  selectedTab: 'map',
  filters: { priceRange: [2, 3], rating: 4.5 },
  sortBy: 'distance'
});

// State persists across conversation
// Later in conversation, state is restored
const previousState = window.openai.widgetState;
console.log(previousState.selectedTab); // 'map'
```

**State Management Guidelines:**
- Keep state under 4k tokens for performance
- State is sent to the model – avoid sensitive data
- State is scoped to specific widget instance (message_id/widgetId pair)
- Use for UI preferences, selections, temporary filters

#### **Display Modes**

Widgets can render in two modes:

| Mode | Use Case | Characteristics |
|------|----------|----------------|
| **Inline** | Quick actions, summaries | Compact cards, key info + CTA |
| **Fullscreen** | Complex interactions | Full interface, multi-step flows |

```javascript
// Detect current mode
const mode = window.openai.displayMode;

if (mode === 'fullscreen') {
  // Render detailed interface
  renderFullMapView();
} else {
  // Render compact card
  renderSummaryCard();
}
```

### Security Architecture

#### **Sandboxing**

Widgets run in a heavily restricted sandbox:

```typescript
// In tool metadata
"_meta": {
  "openai/widgetCSP": "default-src 'self'; connect-src https://api.example.com",
  "openai/widgetDomains": ["api.example.com"]
}
```

**Security Boundaries:**
- No direct access to ChatGPT DOM or data
- CSP enforces network restrictions
- Cross-origin isolation via iframe
- Explicit API surface through `window.openai`

#### **Authentication**

Built-in support for user authentication:

```python
# Server-side authentication check
async def get_user_data(context):
    user_id = context.user_id  # From OAuth flow
    if not user_id:
        raise AuthenticationError("User must be logged in")

    return await db.get_user_profile(user_id)
```

**Security Best Practices:**
- Never embed API keys or secrets in `structuredContent`, `content`, or widget state
- Enforce authentication in the server, not via client hints
- Use `_meta` for sensitive data (widget-only, not sent to model)
- Implement proper authorization checks
- Validate all inputs rigorously

---

## 5. Code Examples

### Complete Example: To-Do List App

#### **MCP Server (Node.js + TypeScript)**

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// In-memory storage
let todos: { id: number; text: string; completed: boolean }[] = [];
let nextId = 1;

// Create MCP server
const server = new Server(
  {
    name: "todo-app",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Register UI template as resource
server.setResourceHandler(async (request) => {
  if (request.params.uri === "ui://widget/todo-list.html") {
    return {
      contents: [
        {
          uri: "ui://widget/todo-list.html",
          mimeType: "text/html+skybridge",
          text: `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui; padding: 20px; }
    .todo-item {
      display: flex;
      gap: 10px;
      padding: 8px;
      border-bottom: 1px solid #eee;
    }
    .todo-item.completed {
      text-decoration: line-through;
      opacity: 0.6;
    }
    input[type="text"] {
      flex: 1;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    button {
      padding: 8px 16px;
      background: #0066cc;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div id="app">
    <form id="add-form">
      <input type="text" id="todo-input" placeholder="Add a new task..." />
      <button type="submit">Add</button>
    </form>
    <div id="todo-list"></div>
  </div>

  <script>
    const data = window.openai.toolOutput;

    function render() {
      const list = document.getElementById('todo-list');
      list.innerHTML = data.todos.map(todo => \`
        <div class="todo-item \${todo.completed ? 'completed' : ''}">
          <input
            type="checkbox"
            \${todo.completed ? 'checked' : ''}
            onchange="toggleTodo(\${todo.id})"
          />
          <span>\${todo.text}</span>
        </div>
      \`).join('');
    }

    async function toggleTodo(id) {
      await window.openai.callTool('complete_todo', { id });
    }

    document.getElementById('add-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = document.getElementById('todo-input');
      await window.openai.callTool('add_todo', { text: input.value });
      input.value = '';
    });

    render();
  </script>
</body>
</html>
          `,
        },
      ],
    };
  }
  throw new Error("Resource not found");
});

// List available tools
server.setToolListHandler(async () => {
  return {
    tools: [
      {
        name: "get_todos",
        description: "Get all todo items",
        inputSchema: z.object({}).shape,
        _meta: {
          "openai/outputTemplate": "ui://widget/todo-list.html",
          "openai/toolInvocation/invoking": "Loading todos...",
          "openai/toolInvocation/invoked": "Here are your todos",
        },
      },
      {
        name: "add_todo",
        description: "Add a new todo item",
        inputSchema: z.object({
          text: z.string().describe("The todo text"),
        }).shape,
        _meta: {
          "openai/outputTemplate": "ui://widget/todo-list.html",
          "openai/widgetAccessible": true,
        },
      },
      {
        name: "complete_todo",
        description: "Mark a todo as complete or incomplete",
        inputSchema: z.object({
          id: z.number().describe("The todo ID"),
        }).shape,
        _meta: {
          "openai/outputTemplate": "ui://widget/todo-list.html",
          "openai/widgetAccessible": true,
        },
      },
    ],
  };
});

// Handle tool calls
server.setToolCallHandler(async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "get_todos":
      return {
        content: [
          {
            type: "text",
            text: `You have ${todos.length} todos (${todos.filter((t) => !t.completed).length} incomplete)`,
          },
        ],
        structuredContent: {
          todos,
        },
      };

    case "add_todo":
      const newTodo = {
        id: nextId++,
        text: args.text,
        completed: false,
      };
      todos.push(newTodo);
      return {
        content: [{ type: "text", text: `Added: ${args.text}` }],
        structuredContent: { todos },
      };

    case "complete_todo":
      const todo = todos.find((t) => t.id === args.id);
      if (todo) {
        todo.completed = !todo.completed;
        return {
          content: [
            {
              type: "text",
              text: `${todo.completed ? "Completed" : "Uncompleted"}: ${todo.text}`,
            },
          ],
          structuredContent: { todos },
        };
      }
      throw new Error("Todo not found");

    default:
      throw new Error("Unknown tool");
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Todo MCP server running on stdio");
}

main();
```

#### **MCP Server (Python + FastMCP)**

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

# Data models
class Todo(BaseModel):
    id: int
    text: str
    completed: bool = False

# In-memory storage
todos: List[Todo] = []
next_id = 1

# Create MCP server
mcp = FastMCP("todo-app")

# UI template
TODO_WIDGET_HTML = """
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Same CSS as TypeScript example */
  </style>
</head>
<body>
  <!-- Same HTML structure -->
  <script>
    // Same JavaScript logic
  </script>
</body>
</html>
"""

# Register UI resource
@mcp.resource("ui://widget/todo-list.html")
def get_todo_widget() -> str:
    """Returns the todo list widget UI"""
    return TODO_WIDGET_HTML

# Tools
@mcp.tool()
def get_todos() -> dict:
    """Get all todo items"""
    return {
        "content": f"You have {len(todos)} todos ({len([t for t in todos if not t.completed])} incomplete)",
        "structuredContent": {
            "todos": [t.dict() for t in todos]
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/todo-list.html",
            "openai/toolInvocation/invoking": "Loading todos...",
            "openai/toolInvocation/invoked": "Here are your todos"
        }
    }

@mcp.tool()
def add_todo(text: str = Field(..., description="The todo text")) -> dict:
    """Add a new todo item"""
    global next_id
    new_todo = Todo(id=next_id, text=text)
    next_id += 1
    todos.append(new_todo)

    return {
        "content": f"Added: {text}",
        "structuredContent": {
            "todos": [t.dict() for t in todos]
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/todo-list.html",
            "openai/widgetAccessible": True
        }
    }

@mcp.tool()
def complete_todo(id: int = Field(..., description="The todo ID")) -> dict:
    """Toggle todo completion status"""
    todo = next((t for t in todos if t.id == id), None)
    if not todo:
        raise ValueError("Todo not found")

    todo.completed = not todo.completed
    status = "Completed" if todo.completed else "Uncompleted"

    return {
        "content": f"{status}: {todo.text}",
        "structuredContent": {
            "todos": [t.dict() for t in todos]
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/todo-list.html",
            "openai/widgetAccessible": True
        }
    }

# Run server
if __name__ == "__main__":
    mcp.run()
```

### React Widget Example

```typescript
// restaurant-widget.tsx
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

interface Restaurant {
  id: number;
  name: string;
  cuisine: string;
  rating: number;
  priceLevel: number;
  location: { lat: number; lng: number };
}

function RestaurantWidget() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [selectedTab, setSelectedTab] = useState('list');
  const [filters, setFilters] = useState({ minRating: 0, maxPrice: 4 });

  useEffect(() => {
    // Load data from OpenAI
    const data = window.openai.toolOutput;
    setRestaurants(data.restaurants || []);

    // Restore widget state
    const state = window.openai.widgetState;
    if (state) {
      setSelectedTab(state.selectedTab || 'list');
      setFilters(state.filters || filters);
    }
  }, []);

  useEffect(() => {
    // Persist state
    window.openai.setWidgetState({ selectedTab, filters });
  }, [selectedTab, filters]);

  const handleFilter = async () => {
    const result = await window.openai.callTool('filter_restaurants', {
      minRating: filters.minRating,
      maxPrice: filters.maxPrice
    });
    setRestaurants(result.restaurants);
  };

  return (
    <div className="restaurant-widget">
      <div className="tabs">
        <button
          onClick={() => setSelectedTab('list')}
          className={selectedTab === 'list' ? 'active' : ''}
        >
          List
        </button>
        <button
          onClick={() => setSelectedTab('map')}
          className={selectedTab === 'map' ? 'active' : ''}
        >
          Map
        </button>
      </div>

      <div className="filters">
        <label>
          Min Rating:
          <input
            type="range"
            min="0"
            max="5"
            step="0.5"
            value={filters.minRating}
            onChange={(e) => setFilters({...filters, minRating: parseFloat(e.target.value)})}
          />
          {filters.minRating}
        </label>
        <button onClick={handleFilter}>Apply Filters</button>
      </div>

      {selectedTab === 'list' ? (
        <div className="restaurant-list">
          {restaurants.map(r => (
            <div key={r.id} className="restaurant-card">
              <h3>{r.name}</h3>
              <p>{r.cuisine} • {'$'.repeat(r.priceLevel)}</p>
              <p>⭐ {r.rating}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="map-view">
          {/* Map implementation */}
          <p>Map showing {restaurants.length} restaurants</p>
        </div>
      )}
    </div>
  );
}

// Mount
const root = createRoot(document.getElementById('root')!);
root.render(<RestaurantWidget />);
```

---

## 6. Comparison with Other Approaches

### OpenAI's Framework Ecosystem

OpenAI offers multiple frameworks for different use cases:

| Framework | Purpose | When to Use |
|-----------|---------|-------------|
| **Apps SDK** | Interactive apps in ChatGPT | Consumer-facing features with UI |
| **Agents SDK** | Multi-agent workflows | Backend automation, orchestration |
| **Assistants API** | Managed assistant services | Stateful assistants (being deprecated) |
| **Responses API** | Modern tool-calling API | Direct API integration |

### Apps SDK vs Agents SDK

#### **Apps SDK**

**Focus**: Consumer-facing applications with rich UI in ChatGPT

**Architecture**:
- MCP server + Web component (iframe)
- Rendered inside ChatGPT conversations
- User-driven, conversational interface

**Key Features**:
- `window.openai` API for UI<->backend communication
- Template-based widget rendering
- Inline and fullscreen display modes
- Integrated into ChatGPT for 800M+ users

**Use Cases**:
- Booking services (rides, hotels, restaurants)
- Data visualization (maps, charts, dashboards)
- Interactive tools (calculators, configurators)
- E-commerce integrations

**Code Example**:
```python
@mcp.tool()
def book_ride(pickup: str, destination: str):
    return {
        "content": f"Booking ride from {pickup} to {destination}",
        "structuredContent": {...},
        "_meta": {
            "openai/outputTemplate": "ui://widget/ride-booking.html"
        }
    }
```

#### **Agents SDK**

**Focus**: Multi-agent orchestration for backend workflows

**Architecture**:
- Python-first framework
- Standalone agents with handoffs
- No UI components

**Key Features**:
- **Agents**: LLMs with instructions and tools
- **Handoffs**: Agent-to-agent delegation
- **Guardrails**: Input/output validation
- **Sessions**: Automatic conversation history
- **Tracing**: Built-in observability

**Use Cases**:
- Customer support automation (triage → specialist agents)
- Data processing pipelines
- Multi-step research and analysis
- Backend automation workflows

**Code Example**:
```python
from agents import Agent, Runner

# Define specialized agents
triage_agent = Agent(
    name="Triage",
    instructions="Route to appropriate specialist",
    handoffs=[sales_agent, support_agent]
)

sales_agent = Agent(
    name="Sales",
    instructions="Handle sales inquiries",
    tools=[get_pricing, create_quote]
)

# Run
result = Runner.run_sync(triage_agent, "I want to upgrade my plan")
```

**Key Difference**: Apps SDK is for **user-facing experiences**, Agents SDK is for **backend orchestration**.

### Apps SDK vs Assistants API

The Assistants API is being **deprecated in mid-2026** in favor of the Responses API.

| Feature | Assistants API | Apps SDK |
|---------|---------------|----------|
| **Status** | Deprecating (sunset mid-2026) | Active, preview (2025) |
| **State Management** | Automatic thread management | MCP + widget state |
| **UI** | No custom UI | Rich web components |
| **Tools** | Function calling | MCP tools + templates |
| **Platform** | API-based, standalone | Integrated in ChatGPT |
| **Migration Path** | → Responses API | N/A (different use case) |

**When Assistants API Was Used**:
- AI assistants with persistent state
- File search and code interpreter
- Multi-turn conversations with history

**Why Apps SDK is Different**:
- Built for ChatGPT integration, not standalone
- Visual, interactive UI components
- Consumer-facing vs developer API

### Apps SDK vs MCP (Pure)

**Model Context Protocol (MCP)** is the foundational open standard. Apps SDK **extends** MCP.

| Aspect | Pure MCP | Apps SDK |
|--------|----------|----------|
| **Scope** | Protocol specification | Framework + Platform |
| **Origin** | Anthropic (Nov 2024) | OpenAI (Oct 2025) |
| **UI** | No UI specification | Widget templates + `window.openai` |
| **Platform** | Model-agnostic (Claude, ChatGPT, etc.) | ChatGPT-specific features |
| **Extensions** | Base tools, resources, prompts | + UI templates, widget runtime |

**MCP provides**:
- JSON-RPC 2.0 protocol
- Tool discovery and invocation
- Resource serving
- Authentication (OAuth 2.1)

**Apps SDK adds**:
- `openai/outputTemplate` metadata
- `openai/widgetAccessible` flag
- `openai/toolInvocation/*` annotations
- Widget sandboxing and runtime
- `window.openai` global API

**Relationship**: Apps SDK is MCP + OpenAI-specific extensions for ChatGPT integration.

### Apps SDK vs A2A (Agent-to-Agent Protocol)

**A2A** (Google's Agent-to-Agent Protocol) solves a **different problem** than Apps SDK.

| Dimension | Apps SDK | A2A |
|-----------|----------|-----|
| **Problem** | User ↔ AI + Tools | Agent ↔ Agent |
| **Scope** | Human-in-loop applications | Agent collaboration |
| **Creator** | OpenAI | Google |
| **Focus** | ChatGPT extensibility | Cross-platform agent communication |
| **Platform** | ChatGPT-specific | Platform-agnostic |

**A2A Purpose**: Enable agents from different vendors (OpenAI, Google, Anthropic, etc.) to communicate and collaborate.

**Example A2A Use Case**:
```
Google ADK Agent ←→ OpenAI Agent ←→ Anthropic Agent
     (A2A Protocol enables cross-platform communication)
```

**Apps SDK Purpose**: Enable developers to build interactive apps that run in ChatGPT.

**Example Apps SDK Use Case**:
```
User in ChatGPT → "Book a ride to airport"
  → ChatGPT invokes ride_booking tool (MCP)
    → MCP server returns data + widget template
      → Interactive booking UI renders in chat
```

**Key Insight**: These protocols serve **complementary purposes**:
- **MCP** (Apps SDK foundation): Tool integration (AI ↔ External Tools)
- **A2A**: Agent interoperability (AI ↔ AI)
- **Apps SDK**: User-facing applications (User ↔ AI ↔ Tools + UI)

### Comparison with Anthropic's MCP Implementation

Both OpenAI and Anthropic have adopted MCP, but with different approaches:

| Aspect | OpenAI (Apps SDK) | Anthropic (Claude + MCP) |
|--------|-------------------|-------------------------|
| **Philosophy** | Centralized, product-first | Decentralized, developer-first |
| **Integration** | ChatGPT-native apps | Desktop app + API integration |
| **UI Layer** | Widget templates + iframe runtime | No standardized UI layer |
| **Extensions** | OpenAI-specific metadata | Pure MCP spec |
| **Distribution** | ChatGPT app store (planned) | Developer self-hosted |
| **Governance** | OpenAI-controlled | Open standard |

**OpenAI's Approach**: "Fast iteration, centralized platform, visual builder"
- Tight ChatGPT integration
- Consumer-facing distribution
- Monetization plans

**Anthropic's Approach**: "Open standard, composable, developer control"
- MCP as universal protocol
- Developer self-hosting
- Vendor-neutral ecosystem

**Quote from research**:
> "At the highest level the difference is governance vs. velocity. AgentKit (OpenAI) — centralized, product-first, fast iteration. It expects you to accept OpenAI's runtime as the easiest path to ship (visual builder + embedded UI + integrated evals). Claude Agents SDK (Anthropic) — decentralized, developer-first, composable."

### Summary Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                    Framework Comparison                      │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│   Feature   │  Apps SDK   │ Agents SDK  │   Pure MCP       │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ UI Support  │ ✅ Rich     │ ❌ None     │ ❌ None          │
│ Platform    │ ChatGPT     │ Standalone  │ Any LLM          │
│ Multi-Agent │ ❌ No       │ ✅ Yes      │ ⚠️ Tool-level   │
│ Consumer UX │ ✅ Optimized│ ❌ Backend  │ ⚠️ Depends      │
│ Handoffs    │ ❌ No       │ ✅ Built-in │ ❌ No            │
│ Guardrails  │ ⚠️ Manual   │ ✅ Built-in │ ❌ No            │
│ Distribution│ ChatGPT App │ Self-deploy │ Self-deploy      │
└─────────────┴─────────────┴─────────────┴──────────────────┘
```

---

## 7. Use Cases and When to Use It

### Ideal Use Cases for Apps SDK

#### **1. Transactional Services**

**Characteristics**: Time-bound actions with clear outcomes

**Examples**:
- **Ride booking**: "Book an Uber to the airport"
- **Food ordering**: "Order pizza from nearby restaurants"
- **Hotel reservations**: "Find hotels in Paris for next week"
- **Appointment scheduling**: "Schedule a haircut for Tuesday"

**Why Apps SDK**:
- Conversational discovery ("I need a ride")
- Interactive booking flow in widget
- Immediate confirmation and tracking
- Natural fit for ChatGPT's 800M users

**Example App Flow**:
```
User: "Book a ride to JFK airport"
  → ChatGPT invokes ride_booking tool
    → Widget shows: pickup location, car options, price estimate
      → User selects option in widget
        → Confirmation with tracking link
```

#### **2. Data Visualization & Exploration**

**Characteristics**: Rich data that benefits from visual representation

**Examples**:
- **Real estate**: Interactive maps of home listings (Zillow example)
- **Analytics dashboards**: Sales metrics, KPIs
- **Financial data**: Stock charts, portfolio performance
- **Weather**: Interactive forecast maps
- **Travel**: Destination comparisons, itinerary views

**Why Apps SDK**:
- Inline visualization in conversation
- Interactive filtering and exploration
- Contextual updates based on conversation
- Fullscreen mode for detailed views

**Example**:
```python
@mcp.tool()
def search_homes(location: str, price_max: int):
    listings = zillow_api.search(location, price_max)

    return {
        "content": f"Found {len(listings)} homes in {location} under ${price_max:,}",
        "structuredContent": {
            "listings": listings,
            "mapCenter": get_center(listings)
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/property-map.html",
            "openai/widgetData": {
                "fullDetails": [l.all_data() for l in listings]
            }
        }
    }
```

#### **3. Content Creation & Editing**

**Characteristics**: Generate and refine content with visual previews

**Examples**:
- **Presentation design**: "Create slides for my pitch" (Canva example)
- **Document formatting**: Resume builders, report templates
- **Image editing**: Photo filters, adjustments
- **Music creation**: Playlist builders (Spotify example)

**Why Apps SDK**:
- WYSIWYG preview in chat
- Iterative refinement through conversation
- Export/save directly from widget
- Template selection and customization

#### **4. Educational & Reference Tools**

**Characteristics**: Interactive learning experiences

**Examples**:
- **Course navigation**: Browse and enroll in courses (Coursera example)
- **Language learning**: Flashcards, quizzes
- **Math tools**: Graphing calculators, equation solvers
- **Science simulations**: 3D models, interactive diagrams

**Why Apps SDK**:
- Conversational Q&A + visual learning
- Interactive practice within chat
- Progress tracking across sessions
- Personalized learning paths

#### **5. Productivity & Workflow Tools**

**Characteristics**: Task management and quick actions

**Examples**:
- **To-do lists**: Add, check, organize tasks
- **Calendar management**: View availability, schedule events
- **Note-taking**: Quick capture with organization
- **Email drafting**: Template-based composition

**Why Apps SDK**:
- Natural language task creation
- Quick updates via widget checkboxes/buttons
- State persistence across conversation
- Minimal context switching

### When NOT to Use Apps SDK

The official guidelines specify these anti-patterns:

#### **❌ Long-form or Static Content**

**Bad Use Cases**:
- Blog posts or articles (use a website)
- Documentation (use docs site)
- Terms of service (link to web page)
- Extended tutorials

**Why**: ChatGPT conversation is not suited for reading long text. Users expect conversational summaries, not full documents.

#### **❌ Complex Multi-step Workflows**

**Bad Use Cases**:
- 10-step onboarding processes
- Complex configuration wizards
- Multi-page checkout flows
- Detailed form submissions

**Why**: Inline and fullscreen modes have space constraints. Complex flows should use dedicated web apps.

#### **❌ Ads, Upsells, or Irrelevant Messaging**

**Bad Use Cases**:
- Promotional content unrelated to user request
- "Upgrade to premium" prompts in results
- Advertising within widgets
- Cross-selling unrelated products

**Why**: Apps should provide value in the moment, not distract with marketing.

#### **❌ Sensitive or Private Information Display**

**Bad Use Cases**:
- Full credit card numbers in cards
- Social security numbers
- Passwords or API keys
- Detailed health records

**Why**: Widget content is visible in conversation history. Use secure links or masked displays.

### Decision Framework

Use this checklist to determine if Apps SDK is appropriate:

```
✅ Good fit if you answer YES to:
  □ Task fits naturally in conversation (booking, ordering, scheduling)?
  □ Information is valuable in the moment (users can act immediately)?
  □ Can be summarized visually (one card, key details, clear CTA)?
  □ Extends ChatGPT in an additive way?
  □ Benefits from ChatGPT's discovery and context?

❌ Poor fit if you answer YES to:
  □ Requires extensive reading or static content?
  □ Involves complex, multi-page workflows?
  □ Primary purpose is advertising or upselling?
  □ Displays highly sensitive information?
  □ Better suited for standalone web/mobile app?
```

### Example Evaluation

**Use Case**: Restaurant recommendations with booking

| Question | Answer | Reasoning |
|----------|--------|-----------|
| Conversational fit? | ✅ Yes | "Find Italian restaurants nearby" is natural |
| Immediate value? | ✅ Yes | User can book right away |
| Visual summary? | ✅ Yes | List/map with ratings, prices |
| Extends ChatGPT? | ✅ Yes | Adds booking capability to search |
| Sensitive data? | ❌ No | Public restaurant info |

**Verdict**: ✅ **Excellent fit for Apps SDK**

---

**Use Case**: Complete accounting software

| Question | Answer | Reasoning |
|----------|--------|-----------|
| Conversational fit? | ❌ No | Requires extensive data entry and navigation |
| Immediate value? | ⚠️ Maybe | Some quick queries yes, full app no |
| Visual summary? | ❌ No | Complex dashboards, multi-page reports |
| Extends ChatGPT? | ⚠️ Partially | Better as standalone with AI assistant |
| Sensitive data? | ✅ Yes | Financial records, tax info |

**Verdict**: ❌ **Poor fit for Apps SDK** (use standalone app with ChatGPT integration via API)

### Real-World Examples

OpenAI has showcased these partner apps:

1. **Zillow**: Browse home listings on interactive map
   - Natural language search
   - Map-based visualization
   - Filter by price, bedrooms, location
   - Direct links to full listings

2. **Canva**: Transform outline into slide deck
   - Conversational design brief
   - AI-generated slides
   - Visual preview and editing
   - Export to Canva for refinement

3. **Coursera**: Browse and enroll in courses
   - Course recommendations
   - Content previews
   - Enrollment flow
   - Integration with learning

4. **Booking.com / Expedia**: Travel booking
   - Destination search
   - Price comparison
   - Booking flow
   - Itinerary management

5. **Spotify**: Playlist creation
   - Natural language music requests
   - Playlist preview
   - Direct playback integration

---

## 8. References and Official Documentation

### Primary Official Resources

#### **OpenAI Apps SDK Documentation**
- **Main docs**: https://developers.openai.com/apps-sdk/
- **Quickstart guide**: https://developers.openai.com/apps-sdk/quickstart/
- **Build MCP server**: https://developers.openai.com/apps-sdk/build/mcp-server/
- **Build ChatGPT UI**: https://developers.openai.com/apps-sdk/build/chatgpt-ui
- **Examples**: https://developers.openai.com/apps-sdk/build/examples/
- **API Reference**: https://developers.openai.com/apps-sdk/reference/
- **Design guidelines**: https://developers.openai.com/apps-sdk/concepts/design-guidelines/
- **Developer guidelines**: https://developers.openai.com/apps-sdk/app-developer-guidelines/

#### **GitHub Repositories**
- **Apps SDK examples**: https://github.com/openai/openai-apps-sdk-examples
- **Apps SDK UI library**: https://github.com/openai/apps-sdk-ui
- **Official announcement**: https://openai.com/index/introducing-apps-in-chatgpt/

### Model Context Protocol (MCP)

#### **Official MCP Resources**
- **OpenAI MCP docs**: https://developers.openai.com/codex/mcp/
- **OpenAI Apps SDK MCP concept**: https://developers.openai.com/apps-sdk/concepts/mcp-server/
- **Platform docs**: https://platform.openai.com/docs/mcp
- **MCP TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk (published as `@modelcontextprotocol/sdk`)
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **FastMCP (Python)**: https://github.com/jlowin/fastmcp

#### **Learning Resources**
- **DataCamp tutorial**: [Model Context Protocol (MCP): A Guide With Demo Project](https://www.datacamp.com/tutorial/mcp-model-context-protocol)
- **Microsoft guide**: [Model Context Protocol (MCP): Integrating Azure OpenAI](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/model-context-protocol-mcp-integrating-azure-openai-for-enhanced-tool-integratio/4393788)
- **Wikipedia**: [Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)

### OpenAI Agents SDK

#### **Official Documentation**
- **Main docs**: https://openai.github.io/openai-agents-python/
- **Quickstart**: https://openai.github.io/openai-agents-python/quickstart/
- **Agents guide**: https://openai.github.io/openai-agents-python/agents/
- **Guardrails**: https://openai.github.io/openai-agents-python/guardrails/
- **Running agents**: https://openai.github.io/openai-agents-python/running_agents/
- **Realtime agents**: https://openai.github.io/openai-agents-python/realtime/quickstart/

#### **GitHub**
- **Python SDK**: https://github.com/openai/openai-agents-python
- **JavaScript SDK**: https://github.com/openai/openai-agents-js
- **Realtime agents**: https://github.com/openai/openai-realtime-agents

#### **Announcements**
- **New tools for building agents**: https://openai.com/index/new-tools-for-building-agents/
- **Community updates**: https://community.openai.com/t/updates-to-building-agents-typescript-agents-sdk-a-new-realtimeagent-feature-for-voice-agents-traces-for-realtime-and-speech-to-speech-improvements/1277152

### Historical Context

#### **ChatGPT Plugins (Deprecated)**
- **Original announcement**: https://openai.com/index/chatgpt-plugins/
- **Quickstart (archived)**: https://github.com/openai/plugins-quickstart
- **Platform docs**: https://platform.openai.com/docs/plugins/introduction
- **Evolution article**: [OpenAI's Transition from ChatGPT Plugins to GPTs](https://article-factory.ai/blog/openais-transition-from-chatgpt-plugins-to-gpts)

#### **Assistants API (Deprecating mid-2026)**
- **Overview**: https://platform.openai.com/docs/assistants/overview
- **API reference**: https://platform.openai.com/docs/api-reference/assistants
- **FAQ**: https://help.openai.com/en/articles/8550641-assistants-api-v2-faq
- **Migration**: Responses API replaces Assistants API

### Technical Deep Dives & Tutorials

#### **Apps SDK Tutorials**
- **Complete developer guide**: [How to Build Your First OpenAI App with the New Apps SDK](https://michaelwapp.medium.com/how-to-build-your-first-openai-app-with-the-new-apps-sdk-a-complete-developer-guide-3de0d20af3fc)
- **The New Stack analysis**: [Inside OpenAI's Apps SDK: Web Architecture Explained](https://thenewstack.io/openai-launches-apps-sdk-for-chatgpt-a-new-app-platform/)
- **Skywork AI guide**: [OpenAI Apps SDK: How Developers Bring Services Into ChatGPT](https://skywork.ai/blog/openai-apps-sdk-chatgpt-integration/)
- **Apps SDK handbook**: [Building Custom Tools and Widgets for ChatGPT](https://medium.com/@sumit-paul/building-custom-tools-and-widgets-for-chatgpt-the-openai-apps-sdk-handbook-fef47a7ba555)
- **Getting started**: [Getting Started with OpenAI Apps SDK](https://www.apps-sdk.dev/getting-started-apps-sdk.html)

#### **MCP Tutorials**
- **FastMCP guide**: [How to Create an MCP Server in Python - FastMCP](https://gofastmcp.com/tutorials/create-mcp-server)
- **Building MCP server**: [Building an MCP server in Python using FastMCP](https://mcpcat.io/guides/building-mcp-server-python-fastmcp/)
- **Comprehensive guide**: [Creating an MCP Server Using FastMCP](https://www.pondhouse-data.com/blog/create-mcp-server-with-fastmcp)
- **DataCamp**: [Building an MCP Server and Client with FastMCP 2.0](https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp)

#### **Agents SDK Tutorials**
- **Technical deep dive**: [Unpacking OpenAI's Agents SDK](https://mtugrull.medium.com/unpacking-openais-agents-sdk-a-technical-deep-dive-into-the-future-of-ai-agents-af32dd56e9d1)
- **Mastering guide**: [Mastering OpenAI's new Agents SDK & Responses API](https://dev.to/bobbyhalljr/mastering-openais-new-agents-sdk-responses-api-part-1-2al8)
- **DataCamp**: [OpenAI Agents SDK Tutorial: Building AI Systems That Take Action](https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial)

### Comparative Analysis

#### **Framework Comparisons**
- **Apps SDK vs Agents SDK vs MCP**: [OpenAI's Agents SDK and Anthropic's Model Context Protocol](https://www.prompthub.us/blog/openais-agents-sdk-and-anthropics-model-context-protocol-mcp)
- **Agents SDK vs MCP**: [OpenAI Agents SDK vs MCP: Feature & Usability Comparison](https://blog.promptlayer.com/openai-agents-sdk-vs-mcp/)
- **MCP vs Work with Apps**: [Model Context Protocol (MCP) vs OpenAI's "Work with Apps"](https://medium.com/@hariharan.eswaran/model-context-protocol-mcp-vs-openais-work-with-apps-7e84f37b7a92)
- **OpenAI vs Anthropic**: [Agents: comparing OpenAI's Operator, Responses API, Agents SDK vs Anthropic's MCP](https://mectors.medium.com/agents-comparing-openais-operator-responses-api-agents-sdk-vs-anthropic-s-mcp-bd6bada18ba6)

#### **Multi-Agent Frameworks**
- **A2A vs OpenAI**: [Google A2A vs OpenAI Agents SDK: Which is Better?](https://www.byteplus.com/en/topic/551079)
- **A2A vs MCP**: [MCP vs A2A: Comprehensive Comparison of AI Agent Protocols](https://www.toolworthy.ai/blog/mcp-vs-a2a-protocol-comparison)
- **Why A2A and MCP**: [Why Agents Need A2A and MCP for AI Solutions](https://getstream.io/blog/agent2agent-vs-mcp/)
- **Framework comparison**: [Which Multi-Agent Framework Should Run Your Enterprise AI?](https://medium.com/@mpuig/which-multi-agent-framework-should-run-your-enterprise-ai-abdc8e09ad89)

### Community & Discussion

#### **OpenAI Community Forums**
- **Apps SDK discussions**: https://community.openai.com/ (search "Apps SDK")
- **Agents SDK discussions**: https://community.openai.com/t/agents-example-multi-agent-via-tools-handoff-multiple-input-output-guardrails-streaming/1144540
- **MCP community**: Various threads on implementation

#### **Additional Resources**
- **Awesome OpenAI Apps SDK examples**: https://github.com/ComposioHQ/awesome-openai-apps-sdk-examples
- **Swarm (predecessor)**: https://github.com/openai/swarm
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector

### Industry Analysis

- **InfoQ**: [OpenAI Launches New API, SDK, and Tools to Develop Custom Agents](https://www.infoq.com/news/2025/03/openai-responses-api-agents-sdk/)
- **VentureBeat**: [OpenAI's Swarm AI agent framework: Routines and handoffs](https://venturebeat.com/ai/openais-swarm-ai-agent-framework-routines-and-handoffs)
- **The New Stack**: [OpenAI's Apps SDK: A Developer's Guide to Getting Started](https://thenewstack.io/openais-apps-sdk-a-developers-guide-to-getting-started/)

---

## Conclusion

OpenAI's **Apps SDK** represents the latest evolution in AI application development, moving from simple plugins to fully-featured, interactive applications embedded directly in ChatGPT. Built on the open **Model Context Protocol (MCP)**, it provides a standardized way to extend ChatGPT with custom logic and rich user interfaces.

### Key Takeaways

1. **First Principles**: Apps SDK solves the distribution, integration, and user experience challenges of AI applications by making them conversation-native and contextually discoverable.

2. **Technical Architecture**: Three-layer system (UI widgets + MCP protocol + backend logic) enables bidirectional communication between ChatGPT, user interfaces, and external services.

3. **Ecosystem Position**: Part of a broader framework family:
   - **Apps SDK**: Consumer-facing UIs in ChatGPT
   - **Agents SDK**: Multi-agent backend orchestration
   - **MCP**: Universal tool integration protocol
   - **Responses API**: Modern API for tool calling

4. **Ideal Use Cases**: Transactional services (booking, ordering), data visualization (maps, charts), content creation (presentations, playlists), and productivity tools (to-do lists, calendars).

5. **Standards-Based**: Built on open MCP standard ensures portability and interoperability across the AI ecosystem.

The Apps SDK marks a significant shift in how developers build and distribute AI-powered applications, transforming ChatGPT into a platform where apps are native capabilities accessible through natural conversation.

---

**Report compiled**: 2025-11-23
**Research scope**: OpenAI Apps SDK, Agents SDK, MCP, historical context, comparisons, and technical implementation
**Primary sources**: Official OpenAI documentation, GitHub repositories, technical tutorials, and industry analysis
