# Model Context Protocol (MCP)

## Overview

The Model Context Protocol (MCP) is an open-source standard created by Anthropic in November 2024 to solve the fundamental problem of connecting AI systems to external data sources and tools. Like USB-C standardized physical connectivity, MCP standardizes how AI applications integrate with the systems where data lives.

## Contents

1. [First Principles & Motivation](./01-first-principles.md) - Why MCP exists and the problems it solves
2. [Architecture & Design](./02-architecture.md) - Technical architecture and protocol design
3. [Code Examples](./03-examples.md) - Practical implementations in Python and TypeScript
4. [Use Cases](./04-use-cases.md) - Real-world applications and adoption
5. [References](./05-references.md) - Complete documentation and resources

## Quick Start

### What is MCP?

MCP is a universal protocol that enables AI applications to connect to any data source or tool through a standardized interface. Instead of building custom integrations for each AI-data pairing, you build once against the MCP standard.

### The Problem

**Without MCP**: N AI applications × M data sources = N×M custom integrations

**With MCP**: N + M implementations (each app implements MCP once, each data source implements MCP once)

### Key Concepts

- **Protocol Layer**: JSON-RPC 2.0 messaging between clients and servers
- **Transport Layer**: STDIO (local) or HTTP (remote) communication
- **Three Primitives**:
  - **Resources**: Read-only data for context
  - **Tools**: Executable functions the AI can invoke
  - **Prompts**: Reusable interaction templates

### Simple Example

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.resource("config://app")
def get_config() -> dict:
    """Get application configuration"""
    return {"version": "1.0.0"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Core Value Proposition

1. **Universal Standard**: Works with Claude, GPT-4, and open-source models
2. **Reduced Complexity**: 85%+ reduction in integration effort
3. **Open Source**: Free to use, modify, and contribute
4. **Battle-Tested**: Powers production systems at Block, Apollo, and more
5. **Growing Ecosystem**: 100+ pre-built servers available

## Getting Started

Choose your path:

- **Learn the concepts**: Start with [First Principles](./01-first-principles.md)
- **Understand the design**: Read [Architecture](./02-architecture.md)
- **Start coding**: Jump to [Examples](./03-examples.md)
- **See applications**: Explore [Use Cases](./04-use-cases.md)

## Official Resources

- [Model Context Protocol Website](https://modelcontextprotocol.io/)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [GitHub - Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GitHub - TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
