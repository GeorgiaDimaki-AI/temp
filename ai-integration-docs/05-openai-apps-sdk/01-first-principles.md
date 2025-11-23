# Apps SDK First Principles

## The Problem Apps SDK Solves

### Distribution Friction

**Before Apps**:
- Build AI feature → Deploy separately → Market to users → Hope they find it
- Fragmented user experience
- Low discoverability

**With Apps**:
- Build once → ChatGPT suggests it → 800M+ users
- Organic discovery
- Integrated experience

### Interactive Data Presentation

**Conversational AI limits**:
- Text-only responses
- No interactive elements
- Hard to present complex data

**Apps SDK solution**:
- Rich widgets (maps, charts, forms)
- Interactive UI in chat
- Better UX for complex tasks

### Context Management

**Without SDK**:
- Manual conversation history tracking
- State management complexity
- Parsing unstructured outputs

**With SDK**:
- Automatic context persistence
- Structured data via MCP
- `window.openai` API for state

## Why October 2025?

Convergence of trends:
1. **MCP adoption** - Open standard mature
2. **ChatGPT scale** - 800M+ users
3. **Enterprise demand** - Need for custom apps
4. **Standards alignment** - OpenAI adopted MCP (Mar 2025)

## Design Philosophy

### Built on MCP

**Why MCP?**
- Open standard (Anthropic)
- Already gaining adoption
- Tool/data access solved
- Cross-platform potential

**Strategic**:
- Not proprietary
- Ecosystem benefits
- Future-proof

### Widget-First

**Insight**: Some tasks need UI, not just text

Examples:
- Choosing from map locations
- Filling forms
- Visualizing data
- Interactive configurations

### Sandboxed Execution

Security model:
- Widgets run in isolated iframes
- No direct DOM access
- `window.openai` API only
- Server-side validation

## Three-Layer Architecture

```
1. Widget (Frontend)
   ↓ window.openai API
2. MCP Protocol
   ↓ JSON-RPC 2.0
3. Your Backend
```

**Benefits**:
- Clear separation
- Standard protocol
- Flexible backend

## Real-World Motivation

### Travel Booking Example

**Before Apps**:
```
User: "Find hotels in Paris"
ChatGPT: "Here are some hotels:
1. Hotel A - $200/night
2. Hotel B - $150/night
..."
User: "Book Hotel B"
ChatGPT: "I can't actually book. Visit hotel-b.com"
```

**With Apps**:
```
User: "Find hotels in Paris"
[Interactive map widget shows hotels]
User: Clicks Hotel B
[Booking form appears]
User: Fills form, completes booking
ChatGPT: "Booked! Confirmation: #12345"
```

## Key Insight

**Apps SDK democratizes AI-powered applications by removing distribution barriers and enabling rich interactions within the world's most popular AI interface.**

Like:
- **App Store** made iPhone app distribution accessible
- **Chrome Web Store** for browser extensions
- **Slack App Directory** for workspace tools

**Apps SDK** does this for AI applications.
