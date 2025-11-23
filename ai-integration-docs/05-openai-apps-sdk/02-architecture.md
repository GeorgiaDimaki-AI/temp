# OpenAI Apps SDK Architecture

## Three-Layer System

```
┌────────────────────────────────────────┐
│  Widget Layer (Frontend)               │
│  - HTML/CSS/JavaScript                 │
│  - React, Vue, or vanilla JS           │
│  - Runs in sandboxed iframe            │
│  - window.openai API for communication │
└─────────────┬──────────────────────────┘
              │
┌─────────────▼──────────────────────────┐
│  Protocol Layer (MCP)                  │
│  - JSON-RPC 2.0                        │
│  - Tool discovery and invocation       │
│  - Structured data exchange            │
└─────────────┬──────────────────────────┘
              │
┌─────────────▼──────────────────────────┐
│  Backend Layer (Your Server)           │
│  - Python, TypeScript, or any language │
│  - Business logic                      │
│  - Data processing                     │
└────────────────────────────────────────┘
```

## Widget Layer

### window.openai API

**Available globals:**

```javascript
// Access tool output
window.openai.toolOutput
// { restaurants: [{name: "Pizza Place", ...}] }

// Set widget state (persisted)
window.openai.setWidgetState({ selectedId: "123" })

// Get current state
const state = window.openai.getWidgetState()

// Call backend tool
const result = await window.openai.callTool("search_nearby", {
  lat: 37.7749,
  lon: -122.4194
})
```

### Example Widget

```html
<!DOCTYPE html>
<html>
<head>
  <title>Restaurant Map</title>
  <style>
    #map { width: 100%; height: 400px; }
    .restaurant { padding: 10px; border: 1px solid #ccc; margin: 5px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <div id="restaurants"></div>

  <script>
    // Get data from backend
    const restaurants = window.openai.toolOutput.restaurants;

    // Render list
    const container = document.getElementById('restaurants');
    restaurants.forEach(r => {
      const div = document.createElement('div');
      div.className = 'restaurant';
      div.innerHTML = `<h3>${r.name}</h3><p>${r.cuisine}</p>`;
      div.onclick = () => selectRestaurant(r);
      container.appendChild(div);
    });

    function selectRestaurant(restaurant) {
      // Save state
      window.openai.setWidgetState({ selected: restaurant.id });

      // Call backend for details
      window.openai.callTool("get_restaurant_details", {
        id: restaurant.id
      }).then(details => {
        alert(`${details.name}\n${details.phone}\n${details.hours}`);
      });
    }
  </script>
</body>
</html>
```

## MCP Layer

### Tool Response Structure

**Three content types:**

```python
{
  # For the model (conversational)
  "content": "Found 5 Italian restaurants",

  # For both model and widget
  "structuredContent": {
    "restaurants": [
      {"name": "Bella Italia", "rating": 4.5},
      {"name": "Pasta Palace", "rating": 4.2}
    ]
  },

  # Widget-only (not sent to model)
  "_meta": {
    "openai/outputTemplate": "ui://widget/restaurant-map.html",
    "openai/widgetAccessible": True,
    "apiKeys": ["secret-key"],  # Never sent to model!
    "largePlaintextData": "..."  # Keep out of model context
  }
}
```

### Why Three Content Types?

**content**: What the model "sees" and reasons about
**structuredContent**: Shared data for both model and UI
**_meta**: Widget configuration and sensitive data

## Data Flow

### User Interaction Flow

```
1. User: "Find Italian restaurants near me"
   ↓
2. ChatGPT calls your MCP tool: search_restaurants
   ↓
3. Your backend:
   - Queries restaurant API
   - Returns structured data + widget template
   ↓
4. ChatGPT:
   - Renders widget with data
   - Shows conversational response
   ↓
5. User interacts with widget
   - Clicks restaurant
   - Widget calls callTool()
   ↓
6. Backend returns details
   ↓
7. Widget updates display
```

### State Persistence

```javascript
// Widget sets state
window.openai.setWidgetState({
  selectedRestaurant: "123",
  filters: { cuisine: "italian", priceRange: "$$" }
});

// State persisted across:
// - Page refreshes
// - Conversation continuation
// - Widget re-renders

// Widget retrieves state
const state = window.openai.getWidgetState();
// Use state to restore UI
```

## Security Model

### Sandboxed Execution

**Widgets run in isolated iframes:**
- No access to parent page DOM
- No access to cookies or localStorage
- Limited API surface (window.openai only)
- CORS restrictions apply

### Data Validation

```python
# Backend must validate all widget inputs
@mcp.tool()
async def book_restaurant(restaurant_id: str, party_size: int):
    # ALWAYS validate
    if not is_valid_restaurant_id(restaurant_id):
        raise ValueError("Invalid restaurant ID")

    if party_size < 1 or party_size > 20:
        raise ValueError("Party size must be 1-20")

    # Proceed with booking
    ...
```

### Sensitive Data Handling

```python
# Use _meta for sensitive data
return {
    "content": "Booking confirmed",
    "structuredContent": {
        "confirmation": "ABC123",
        "restaurant": "Bella Italia"
    },
    "_meta": {
        # Not sent to model - only to widget
        "creditCardLast4": "4242",
        "internalCustomerId": "CUST-9876",
        "apiKeys": {"stripe": "sk_test_..."}
    }
}
```

## MCP Server Implementation

### Python with FastMCP

```python
from fastmcp import FastMCP

mcp = FastMCP("restaurant-app")

@mcp.tool()
async def search_restaurants(
    cuisine: str,
    location: str,
    price_range: str = "$$"
) -> dict:
    """Search for restaurants"""

    # Query API
    results = await restaurant_api.search(
        cuisine=cuisine,
        location=location,
        price_range=price_range
    )

    return {
        "content": f"Found {len(results)} {cuisine} restaurants",
        "structuredContent": {
            "restaurants": [
                {
                    "id": r.id,
                    "name": r.name,
                    "cuisine": r.cuisine,
                    "rating": r.rating,
                    "priceRange": r.price_range
                }
                for r in results
            ]
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/restaurant-map.html",
            "openai/widgetAccessible": True
        }
    }

# Run server
mcp.run(transport="streamable-http", port=3000)
```

## Best Practices

### 1. Widget Size

**Recommended:**
- Width: Adapt to container (100%)
- Height: 300-600px
- Avoid scrolling if possible

**Bad:**
```html
<div style="height: 2000px">  <!-- Too tall! -->
```

**Good:**
```html
<div style="height: 400px; overflow-y: auto">  <!-- Scrollable if needed -->
```

### 2. Error Handling

```javascript
// Widget should handle errors gracefully
async function fetchDetails(id) {
  try {
    const result = await window.openai.callTool("get_details", { id });
    return result;
  } catch (error) {
    console.error("Failed to fetch:", error);
    showErrorMessage("Unable to load details. Please try again.");
    return null;
  }
}
```

### 3. Loading States

```javascript
function showLoading() {
  document.getElementById('content').innerHTML = `
    <div class="loading">Loading...</div>
  `;
}

async function loadData() {
  showLoading();
  const data = await window.openai.callTool("fetch_data", {});
  renderData(data);
}
```

### 4. Responsive Design

```css
/* Mobile-first responsive design */
.restaurant-card {
  width: 100%;
  padding: 10px;
}

@media (min-width: 600px) {
  .restaurant-card {
    width: 48%;
    display: inline-block;
  }
}
```

This architecture enables rich, interactive experiences within ChatGPT while maintaining security and performance.
