# OpenAI Apps SDK

## Overview

The OpenAI Apps SDK enables building interactive web applications that run directly inside ChatGPT conversations, reaching 800M+ users organically.

## Evolution

1. **ChatGPT Plugins** (Mar 2023) - First extensibility
2. **Custom GPTs** (Nov 2023) - ~3M created
3. **Apps SDK** (Oct 2025) - Full-featured apps with rich UI

## Core Value Proposition

### Distribution
- 800M+ ChatGPT users
- Organic discovery (ChatGPT suggests apps)
- No separate marketplace needed

### Rich UI
- Interactive widgets (maps, forms, charts)
- HTML/CSS/JS in ChatGPT
- React, Vue, vanilla JS supported

### Built on MCP
- Standard tool protocol
- Anthropic's open standard
- Works across platforms

## Quick Example

```python
from fastmcp import FastMCP

mcp = FastMCP("my-app")

@mcp.tool()
async def search_restaurants(cuisine: str, location: str) -> dict:
    results = await restaurant_api.search(cuisine, location)
    
    return {
        "content": f"Found {len(results)} restaurants",
        "structuredContent": {"restaurants": results},
        "_meta": {
            "openai/outputTemplate": "ui://widget/map.html",
            "openai/widgetAccessible": True
        }
    }
```

## Contents

1. [First Principles](./01-first-principles.md)
2. [Architecture](./02-architecture.md)
3. [Code Examples](./03-examples.md)
4. [Comparison](./04-comparison.md)
5. [References](./05-references.md)

## Real-World Examples

- **Zillow**: Interactive home listing maps
- **Canva**: Outline → slide deck conversion
- **Coursera**: Course browsing
- **Booking.com**: Travel booking
- **Spotify**: Playlist creation

## When to Use

✅ **Perfect for**:
- Transactional services (booking, ordering)
- Data visualization (maps, charts)
- Content creation tools
- Productivity apps

❌ **Not suitable for**:
- Long-form content
- Multi-page workflows
- Advertising/upselling
- Highly sensitive data display

## Official Resources

- [Apps SDK Docs](https://developers.openai.com/apps-sdk/)
- [Announcement](https://openai.com/index/introducing-apps-in-chatgpt/)
- [Examples](https://github.com/openai/openai-apps-sdk-examples)
