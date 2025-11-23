# Claude Agent SDK

## Overview

The Claude Agent SDK is Anthropic's framework for building autonomous AI agents with sophisticated capabilities. It evolved from Claude Code and represents the infrastructure that powers Anthropic's frontier products.

## Core Philosophy

> "Give your agents a computer, allowing them to work like humans do."

The SDK provides agents with the same tools developers use: terminal access, file system operations, and iterative execution.

## Contents

1. [First Principles](./01-first-principles.md) - Evolution and motivation
2. [Architecture](./02-architecture.md) - Technical design
3. [Code Examples](./03-examples.md) - Practical implementations
4. [Differences from MCP/A2A](./04-differences-from-mcp-and-a2a.md) - How it compares
5. [References](./05-references.md) - Resources

## Quick Start

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import anyio

async def main():
    client = ClaudeSDKClient(api_key="your-api-key")
    
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful coding assistant",
        allowed_tools=["Read", "Write", "Bash"],
        working_directory="/workspace"
    )
    
    async for message in client.send_message(
        prompt="Analyze the codebase and suggest improvements",
        options=options
    ):
        print(message)

anyio.run(main())
```

## Key Features

- **Context Management**: Automatic compaction for long sessions
- **Built-in Tools**: File I/O, Bash, WebFetch, WebSearch
- **Custom Tools**: Add your own via MCP
- **Hooks**: Deterministic validation and logging
- **Subagents**: Specialized agents with isolated context
- **Production Ready**: Error handling, security, monitoring

## Official Resources

- [Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk/overview)
- [Building Agents Blog](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)
