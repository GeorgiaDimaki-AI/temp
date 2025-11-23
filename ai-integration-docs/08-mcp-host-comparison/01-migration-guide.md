# Migration Guide: OpenAI Apps SDK → MCP Webview Host

## Executive Summary

**Migration Difficulty: EASY to MODERATE** ⭐⭐⭐☆☆

**Why it's relatively easy:**
- ✅ Both use MCP protocol (same foundation)
- ✅ Both use HTML/JS widgets
- ✅ Backend MCP servers are ~95% compatible
- ✅ Main changes are in widget JavaScript only

**What needs to change:**
- Widget communication API (window.openai → direct fetch)
- Response metadata format
- Security/trust configuration

**Estimated migration time:** 2-4 hours per app

## Compatibility Analysis

### What's 100% Compatible

#### 1. MCP Server Core Logic

```python
# This code works IDENTICALLY in both systems
from fastmcp import FastMCP

mcp = FastMCP("restaurant-server")

@mcp.tool()
async def search_restaurants(cuisine: str, location: str) -> dict:
    """Search for restaurants"""
    results = await restaurant_api.search(cuisine, location)

    # THIS PART IS IDENTICAL
    restaurants = [
        {
            "id": r.id,
            "name": r.name,
            "cuisine": r.cuisine,
            "rating": r.rating
        }
        for r in results
    ]
```

**Compatibility: 100%** ✅ No changes needed

#### 2. Business Logic

All your actual functionality (database queries, API calls, calculations) works identically.

#### 3. HTML Structure

```html
<!-- This HTML works in both systems -->
<div class="restaurant-card">
    <h3>{{name}}</h3>
    <p>{{cuisine}} • {{rating}}⭐</p>
    <button onclick="selectRestaurant('{{id}}')">View Details</button>
</div>
```

**Compatibility: 100%** ✅ No changes needed

### What Needs Modification

#### 1. Response Metadata (Easy)

**Apps SDK:**
```python
return {
    "content": "Found 5 restaurants",
    "structuredContent": {
        "restaurants": restaurants
    },
    "_meta": {
        "openai/outputTemplate": "ui://widget/restaurant-map.html",
        "openai/widgetAccessible": True
    }
}
```

**MCP Host:**
```python
return {
    "content": [
        {
            "type": "text",
            "text": "Found 5 restaurants"
        },
        {
            "type": "resource",
            "resource": {
                "uri": "webview://restaurant-map",
                "mimeType": "text/html",
                "text": read_html_file("restaurant-map.html")
            }
        }
    ]
}
```

**Migration effort:** 15 minutes per tool

#### 2. Widget Data Access (Easy)

**Apps SDK:**
```javascript
// Access data via window.openai global
const data = window.openai.toolOutput;
const restaurants = data.restaurants;
```

**MCP Host:**
```javascript
// Access data via DOM element or URL parameter
const webviewElement = document.querySelector('[data-webview-data]');
const data = JSON.parse(webviewElement.dataset.webviewData);
const restaurants = data.restaurants;
```

**Migration effort:** 10 minutes per widget

#### 3. Widget-to-Backend Communication (Moderate)

**Apps SDK:**
```javascript
// Call via window.openai API
const result = await window.openai.callTool('get_details', {
    restaurant_id: id
});
```

**MCP Host:**
```javascript
// Direct POST to backend
const result = await fetch('/api/mcp/tools/call', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        serverName: 'restaurant-server',
        toolName: 'get_details',
        args: { restaurant_id: id }
    })
});

const data = await result.json();
```

**Migration effort:** 30 minutes per widget

#### 4. State Management (Easy)

**Apps SDK:**
```javascript
// Persist via window.openai
window.openai.setWidgetState({ selectedId: id });
const state = window.openai.getWidgetState();
```

**MCP Host:**
```javascript
// Persist via localStorage or pass to backend
localStorage.setItem('widgetState', JSON.stringify({ selectedId: id }));
const state = JSON.parse(localStorage.getItem('widgetState') || '{}');

// Or send to backend for server-side persistence
```

**Migration effort:** 20 minutes per widget

## Step-by-Step Migration

### Phase 1: Backend MCP Server (30 min)

#### Step 1: Update Response Format

**Before (Apps SDK):**
```python
@mcp.tool()
async def search_restaurants(cuisine: str) -> dict:
    results = get_results(cuisine)

    return {
        "content": f"Found {len(results)} restaurants",
        "structuredContent": {"restaurants": results},
        "_meta": {
            "openai/outputTemplate": "ui://widget/map.html",
            "openai/widgetAccessible": True
        }
    }
```

**After (MCP Host):**
```python
@mcp.tool()
async def search_restaurants(cuisine: str) -> dict:
    results = get_results(cuisine)

    # Read HTML file
    html_content = read_file("widgets/restaurant-map.html")

    # Inject data into HTML (or pass separately)
    html_with_data = html_content.replace(
        '<!-- DATA_PLACEHOLDER -->',
        f'<script>const restaurantData = {json.dumps(results)};</script>'
    )

    return {
        "content": [
            {
                "type": "text",
                "text": f"Found {len(results)} restaurants"
            },
            {
                "type": "resource",
                "resource": {
                    "uri": f"webview://restaurant-map-{uuid.uuid4()}",
                    "mimeType": "text/html",
                    "text": html_with_data
                }
            }
        ]
    }
```

**Alternative (cleaner):**
```python
# Pass data via data attribute
html_with_data = f"""
<div id="webview-root" data-webview-data='{json.dumps(results)}'>
    {html_content}
</div>
"""
```

#### Step 2: Add MCP Host Configuration

Create `backend/mcp-config.json`:

```json
{
  "mcpServers": {
    "restaurant-server": {
      "command": "python",
      "args": ["restaurant_server.py"],
      "description": "Restaurant search and reservations",
      "trustLevel": "verified"
    }
  }
}
```

### Phase 2: Widget Migration (1-2 hours)

#### Step 1: Update Data Access

**Create a compatibility layer:**

```javascript
// compatibility.js - makes migration easier
const WebviewAdapter = {
    getData: function() {
        // Try OpenAI format first
        if (window.openai && window.openai.toolOutput) {
            return window.openai.toolOutput;
        }

        // Try MCP Host format
        const element = document.querySelector('[data-webview-data]');
        if (element) {
            return JSON.parse(element.dataset.webviewData);
        }

        // Try global variable
        if (window.restaurantData) {
            return window.restaurantData;
        }

        throw new Error('No data found');
    },

    callTool: async function(toolName, args) {
        // Try OpenAI API first
        if (window.openai) {
            return await window.openai.callTool(toolName, args);
        }

        // Use MCP Host direct POST
        const response = await fetch('/api/mcp/tools/call', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                serverName: 'restaurant-server', // Configure this
                toolName: toolName,
                args: args
            })
        });

        if (!response.ok) {
            throw new Error(`Tool call failed: ${response.statusText}`);
        }

        const result = await response.json();
        return result;
    },

    setState: function(state) {
        if (window.openai) {
            window.openai.setWidgetState(state);
        } else {
            localStorage.setItem('widgetState', JSON.stringify(state));
        }
    },

    getState: function() {
        if (window.openai) {
            return window.openai.getWidgetState();
        } else {
            const stored = localStorage.getItem('widgetState');
            return stored ? JSON.parse(stored) : {};
        }
    }
};
```

#### Step 2: Update Widget Code

**Before:**
```javascript
// Apps SDK version
const data = window.openai.toolOutput;
const restaurants = data.restaurants;

async function viewDetails(id) {
    const details = await window.openai.callTool('get_details', {
        restaurant_id: id
    });
    displayDetails(details);
}
```

**After (using adapter):**
```javascript
// Works with both!
const data = WebviewAdapter.getData();
const restaurants = data.restaurants;

async function viewDetails(id) {
    const details = await WebviewAdapter.callTool('get_details', {
        restaurant_id: id
    });
    displayDetails(details);
}
```

### Phase 3: Testing (30 min)

1. **Test in MCP Host:**
```bash
cd backend && npm run dev
# Open http://localhost:3000
```

2. **Verify functionality:**
   - Widget displays correctly
   - Data loads properly
   - Tool calls work
   - State persists

3. **Test edge cases:**
   - Error handling
   - Network failures
   - Large datasets

### Phase 4: Deployment (15 min)

1. **Deploy MCP Host:**
```bash
npm run build
npm start
```

2. **Configure servers in production**

3. **Test with production data**

## Automated Migration Script

Here's a script to help automate the migration:

```python
import json
import re
from pathlib import Path

def migrate_mcp_server(input_file: Path, output_file: Path):
    """Convert Apps SDK server to MCP Host format"""

    content = input_file.read_text()

    # Replace response format
    apps_sdk_pattern = r'''return \{
        "content": (.+?),
        "structuredContent": (.+?),
        "_meta": \{
            "openai/outputTemplate": "(.+?)",
            "openai/widgetAccessible": True
        \}
    \}'''

    def replacement(match):
        content_text = match.group(1)
        structured_data = match.group(2)
        template_path = match.group(3).replace('ui://widget/', '')

        return f'''
    html_content = read_file("widgets/{template_path}")
    html_with_data = inject_data(html_content, {structured_data})

    return {{
        "content": [
            {{"type": "text", "text": {content_text}}},
            {{
                "type": "resource",
                "resource": {{
                    "uri": "webview://{template_path.replace('.html', '')}",
                    "mimeType": "text/html",
                    "text": html_with_data
                }}
            }}
        ]
    }}'''

    migrated = re.sub(apps_sdk_pattern, replacement, content, flags=re.DOTALL)
    output_file.write_text(migrated)

def migrate_widget(input_file: Path, output_file: Path):
    """Convert Apps SDK widget to MCP Host format"""

    content = input_file.read_text()

    # Add compatibility layer
    if 'window.openai' in content:
        # Inject adapter at the beginning
        adapter_script = Path('compatibility.js').read_text()
        content = content.replace(
            '<script>',
            f'<script>\n{adapter_script}\n',
            1
        )

        # Replace window.openai calls
        content = content.replace(
            'window.openai.toolOutput',
            'WebviewAdapter.getData()'
        )
        content = content.replace(
            'window.openai.callTool(',
            'WebviewAdapter.callTool('
        )
        content = content.replace(
            'window.openai.setWidgetState(',
            'WebviewAdapter.setState('
        )
        content = content.replace(
            'window.openai.getWidgetState()',
            'WebviewAdapter.getState()'
        )

    output_file.write_text(content)

# Usage
migrate_mcp_server(
    Path('apps_sdk/restaurant_server.py'),
    Path('mcp_host/restaurant_server.py')
)

migrate_widget(
    Path('apps_sdk/restaurant-map.html'),
    Path('mcp_host/widgets/restaurant-map.html')
)
```

## Dual-Mode Support (Best Approach)

**Support BOTH platforms with one codebase:**

```python
def create_response(text: str, data: dict, widget: str, mode: str = 'auto'):
    """
    Create response that works with both Apps SDK and MCP Host

    Args:
        text: Text response
        data: Structured data
        widget: Widget HTML filename
        mode: 'apps-sdk', 'mcp-host', or 'auto' (detect)
    """

    if mode == 'auto':
        # Detect based on environment or request
        mode = os.getenv('DEPLOYMENT_MODE', 'mcp-host')

    if mode == 'apps-sdk':
        # OpenAI Apps SDK format
        return {
            "content": text,
            "structuredContent": data,
            "_meta": {
                "openai/outputTemplate": f"ui://widget/{widget}",
                "openai/widgetAccessible": True
            }
        }

    else:  # mcp-host
        # MCP Host format
        html_content = read_file(f"widgets/{widget}")
        html_with_data = inject_data(html_content, data)

        return {
            "content": [
                {"type": "text", "text": text},
                {
                    "type": "resource",
                    "resource": {
                        "uri": f"webview://{widget.replace('.html', '')}",
                        "mimeType": "text/html",
                        "text": html_with_data
                    }
                }
            ]
        }

# Use it
@mcp.tool()
async def search_restaurants(cuisine: str) -> dict:
    results = get_results(cuisine)

    return create_response(
        text=f"Found {len(results)} restaurants",
        data={"restaurants": results},
        widget="restaurant-map.html",
        mode='auto'  # Works with both!
    )
```

**Widget (dual-mode):**
```html
<script src="compatibility.js"></script>
<script>
    // Works with both Apps SDK and MCP Host!
    const data = WebviewAdapter.getData();

    async function selectRestaurant(id) {
        const details = await WebviewAdapter.callTool('get_details', {
            restaurant_id: id
        });
        displayDetails(details);
    }
</script>
```

## Migration Checklist

### Backend (30 min)
- [ ] Update response format (Apps SDK → MCP Host)
- [ ] Create mcp-config.json
- [ ] Set trust levels
- [ ] Test MCP server locally
- [ ] Verify tool discovery

### Widgets (1-2 hours per widget)
- [ ] Add compatibility layer (compatibility.js)
- [ ] Update data access (window.openai → adapter)
- [ ] Update tool calls (callTool → adapter)
- [ ] Update state management (setState → adapter)
- [ ] Test widget rendering
- [ ] Test tool calls
- [ ] Test error handling

### Configuration (15 min)
- [ ] Set up MCP Host environment
- [ ] Configure servers
- [ ] Set environment variables
- [ ] Configure security/CORS

### Testing (30 min)
- [ ] Test all widgets load
- [ ] Test all tool calls work
- [ ] Test data flows correctly
- [ ] Test error cases
- [ ] Test on different browsers

### Deployment (15 min)
- [ ] Deploy MCP Host
- [ ] Deploy MCP servers
- [ ] Configure production settings
- [ ] Monitor logs

## Estimated Timeline

| Component | Complexity | Time |
|-----------|------------|------|
| Simple widget (1-2 tools) | Easy | 1-2 hours |
| Medium widget (3-5 tools) | Moderate | 2-4 hours |
| Complex widget (6+ tools) | Moderate | 4-6 hours |
| Backend MCP server | Easy | 30-60 min |
| Testing & QA | - | 1-2 hours |
| Deployment | - | 30 min |

**Total per app:** 3-8 hours depending on complexity

## Conclusion

### ✅ **YES, migration is EASY and PRACTICAL**

**Key reasons:**
1. **Shared foundation**: Both use MCP protocol
2. **Minimal code changes**: Mostly JavaScript API calls
3. **Compatibility layer**: Can support both simultaneously
4. **Incremental migration**: Can migrate one widget at a time
5. **Automated tooling**: Scripts can handle most conversion

**Recommendation:**
- Use the **dual-mode approach** to support both platforms
- **Compatibility layer** makes widgets work everywhere
- **Gradual migration** reduces risk
- Keep **one codebase** for both deployments

**Migration difficulty: ⭐⭐⭐☆☆ (3/5)**
- Easy for simple apps (1-2 hours)
- Moderate for complex apps (4-6 hours)
- Well worth it for privacy/control benefits!
