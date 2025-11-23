# AI Plugins and Tools: Vendor Guide

## Overview

Comprehensive guide to creating tools and plugins for AI/LLM systems across different vendors. Covers Anthropic, OpenAI, Google, Microsoft, and AWS.

## Contents

1. [First Principles](./01-first-principles.md) - Why AI needs tools
2. [Vendor APIs](./02-vendor-apis.md) - Anthropic, OpenAI, Google, Microsoft, AWS
3. [Code Examples](./03-examples.md) - Implementation for each vendor
4. [Comparison](./04-comparison.md) - How approaches differ
5. [Best Practices](./05-best-practices.md) - Production patterns
6. [References](./06-references.md) - Complete resources

## Quick Reference

### Anthropic (Claude)
- **Native**: Tool Use API with JSON schemas
- **Standard**: MCP (Model Context Protocol)
- **Latest**: Structured Outputs (Nov 2025)

### OpenAI
- **Method**: Function Calling
- **Features**: Parallel calls, strict mode
- **SDK**: Agents SDK (2025)

### Google (Gemini)
- **Method**: Function Calling
- **Unique**: Auto-converts Python functions
- **Latest**: Gemini 3 with automatic calling

### Microsoft
- **Products**: M365 Copilot, Azure AI, GitHub Copilot
- **Approach**: Different APIs per product
- **Latest**: MCP support (Oct 2025)

### AWS Bedrock
- **API**: Converse API (unified)
- **Supports**: Multiple model providers
- **Feature**: Works across Claude, Llama, etc.

## Key Insight

**Three Emerging Standards** (2025):
1. **Function Calling** - Vendor-specific, mature
2. **MCP** - Universal, open (becoming standard)
3. **A2A** - Agent collaboration

Use MCP for cross-platform, function calling for single-vendor optimization.
