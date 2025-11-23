# OpenAI Apps SDK Code Examples

Complete examples for building ChatGPT apps with rich UI.

## Basic MCP Server with Widget

### Example 1: Restaurant Finder App (Python)

```python
from fastmcp import FastMCP
import aiohttp

mcp = FastMCP("restaurant-finder")

@mcp.tool()
async def search_restaurants(
    cuisine: str,
    location: str,
    price_range: str = "$$"
) -> dict:
    """
    Search for restaurants by cuisine and location.

    Args:
        cuisine: Type of cuisine (e.g., "Italian", "Japanese")
        location: City or address
        price_range: Price range ($, $$, $$$, $$$$)

    Returns:
        Restaurant list with widget
    """
    # Call restaurant API
    async with aiohttp.ClientSession() as session:
        url = f"https://api.restaurants.com/search"
        params = {
            "cuisine": cuisine,
            "location": location,
            "price": price_range
        }
        async with session.get(url, params=params) as response:
            data = await response.json()

    restaurants = [
        {
            "id": r["id"],
            "name": r["name"],
            "cuisine": r["cuisine"],
            "rating": r["rating"],
            "priceRange": r["price_range"],
            "address": r["address"],
            "lat": r["latitude"],
            "lon": r["longitude"]
        }
        for r in data["results"]
    ]

    return {
        # For the model
        "content": f"Found {len(restaurants)} {cuisine} restaurants in {location}",

        # For both model and widget
        "structuredContent": {
            "restaurants": restaurants,
            "searchParams": {
                "cuisine": cuisine,
                "location": location,
                "priceRange": price_range
            }
        },

        # Widget-only metadata
        "_meta": {
            "openai/outputTemplate": "ui://widget/restaurant-map.html",
            "openai/widgetAccessible": True
        }
    }

@mcp.tool()
async def get_restaurant_details(restaurant_id: str) -> dict:
    """Get detailed information about a specific restaurant"""
    async with aiohttp.ClientSession() as session:
        url = f"https://api.restaurants.com/restaurant/{restaurant_id}"
        async with session.get(url) as response:
            data = await response.json()

    return {
        "content": f"Details for {data['name']}",
        "structuredContent": {
            "restaurant": {
                "id": data["id"],
                "name": data["name"],
                "phone": data["phone"],
                "hours": data["hours"],
                "menu_url": data["menu_url"],
                "photos": data["photos"]
            }
        }
    }

# Run server
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=3000)
```

### Widget (restaurant-map.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Map</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 16px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .search-info {
            background: #f5f5f5;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 16px;
        }

        .restaurant-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
        }

        .restaurant-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            cursor: pointer;
            transition: box-shadow 0.2s;
        }

        .restaurant-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .restaurant-card.selected {
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
        }

        .restaurant-name {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .restaurant-info {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }

        .rating {
            color: #f59e0b;
            font-weight: 600;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .details-panel {
            position: fixed;
            right: -400px;
            top: 0;
            width: 400px;
            height: 100%;
            background: white;
            box-shadow: -2px 0 8px rgba(0,0,0,0.1);
            padding: 24px;
            transition: right 0.3s;
            overflow-y: auto;
        }

        .details-panel.open {
            right: 0;
        }

        .close-btn {
            position: absolute;
            top: 16px;
            right: 16px;
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-info" id="search-info"></div>
        <div class="restaurant-grid" id="restaurants"></div>
    </div>

    <div class="details-panel" id="details-panel">
        <button class="close-btn" onclick="closeDetails()">×</button>
        <div id="details-content"></div>
    </div>

    <script>
        // Get data from backend
        const data = window.openai.toolOutput;
        const restaurants = data.restaurants;
        const searchParams = data.searchParams;

        // Get or initialize state
        let state = window.openai.getWidgetState() || {
            selectedRestaurant: null
        };

        // Display search info
        document.getElementById('search-info').innerHTML = `
            <strong>Search:</strong> ${searchParams.cuisine} in ${searchParams.location}
            (${searchParams.priceRange})
        `;

        // Render restaurant list
        const container = document.getElementById('restaurants');

        if (restaurants.length === 0) {
            container.innerHTML = '<p>No restaurants found</p>';
        } else {
            restaurants.forEach(restaurant => {
                const card = document.createElement('div');
                card.className = 'restaurant-card';
                if (state.selectedRestaurant === restaurant.id) {
                    card.classList.add('selected');
                }

                card.innerHTML = `
                    <div class="restaurant-name">${restaurant.name}</div>
                    <div class="restaurant-info">
                        <div><span class="rating">★ ${restaurant.rating}</span></div>
                        <div>${restaurant.cuisine} • ${restaurant.priceRange}</div>
                        <div>${restaurant.address}</div>
                    </div>
                `;

                card.onclick = () => selectRestaurant(restaurant);
                container.appendChild(card);
            });
        }

        async function selectRestaurant(restaurant) {
            // Save state
            state.selectedRestaurant = restaurant.id;
            window.openai.setWidgetState(state);

            // Update UI
            document.querySelectorAll('.restaurant-card').forEach(card => {
                card.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');

            // Show loading
            const detailsPanel = document.getElementById('details-panel');
            const detailsContent = document.getElementById('details-content');
            detailsContent.innerHTML = '<div class="loading">Loading details...</div>';
            detailsPanel.classList.add('open');

            try {
                // Call backend for details
                const details = await window.openai.callTool('get_restaurant_details', {
                    restaurant_id: restaurant.id
                });

                const restaurantDetails = details.restaurant;

                // Display details
                detailsContent.innerHTML = `
                    <h2>${restaurantDetails.name}</h2>
                    <p><strong>Phone:</strong> ${restaurantDetails.phone}</p>
                    <p><strong>Hours:</strong> ${restaurantDetails.hours}</p>
                    <p><a href="${restaurantDetails.menu_url}" target="_blank">View Menu</a></p>
                `;

                if (restaurantDetails.photos && restaurantDetails.photos.length > 0) {
                    detailsContent.innerHTML += '<h3>Photos:</h3>';
                    restaurantDetails.photos.forEach(photo => {
                        detailsContent.innerHTML += `<img src="${photo}" style="width:100%;margin:8px 0;border-radius:4px;">`;
                    });
                }
            } catch (error) {
                detailsContent.innerHTML = `<p style="color:red;">Error loading details: ${error.message}</p>`;
            }
        }

        function closeDetails() {
            document.getElementById('details-panel').classList.remove('open');
        }
    </script>
</body>
</html>
```

## Example 2: Task Manager App (TypeScript)

### MCP Server (TypeScript)

```typescript
import { FastMCP } from "fastmcp";

const mcp = new FastMCP("task-manager");

interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  dueDate?: string;
}

// In-memory storage (use database in production)
const tasks: Map<string, Task> = new Map();
let taskCounter = 1;

mcp.tool(
  "create_task",
  async (args: {
    title: string;
    description?: string;
    priority?: string;
    dueDate?: string;
  }) => {
    const task: Task = {
      id: `task-${taskCounter++}`,
      title: args.title,
      description: args.description || "",
      status: "todo",
      priority: (args.priority as Task["priority"]) || "medium",
      dueDate: args.dueDate,
    };

    tasks.set(task.id, task);

    return {
      content: `Created task: ${task.title}`,
      structuredContent: {
        task: task,
        allTasks: Array.from(tasks.values()),
      },
      _meta: {
        "openai/outputTemplate": "ui://widget/task-board.html",
        "openai/widgetAccessible": true,
      },
    };
  },
  {
    description: "Create a new task",
    parameters: {
      type: "object",
      properties: {
        title: { type: "string", description: "Task title" },
        description: { type: "string", description: "Task description" },
        priority: {
          type: "string",
          enum: ["low", "medium", "high"],
          description: "Task priority",
        },
        dueDate: {
          type: "string",
          description: "Due date (YYYY-MM-DD format)",
        },
      },
      required: ["title"],
    },
  }
);

mcp.tool(
  "update_task_status",
  async (args: { taskId: string; status: string }) => {
    const task = tasks.get(args.taskId);
    if (!task) {
      throw new Error(`Task ${args.taskId} not found`);
    }

    task.status = args.status as Task["status"];
    tasks.set(args.taskId, task);

    return {
      content: `Updated task status to ${args.status}`,
      structuredContent: {
        task: task,
        allTasks: Array.from(tasks.values()),
      },
      _meta: {
        "openai/outputTemplate": "ui://widget/task-board.html",
        "openai/widgetAccessible": true,
      },
    };
  }
);

mcp.tool(
  "list_tasks",
  async (args: { status?: string }) => {
    let filteredTasks = Array.from(tasks.values());

    if (args.status) {
      filteredTasks = filteredTasks.filter((t) => t.status === args.status);
    }

    return {
      content: `Found ${filteredTasks.length} tasks`,
      structuredContent: {
        tasks: filteredTasks,
      },
      _meta: {
        "openai/outputTemplate": "ui://widget/task-board.html",
        "openai/widgetAccessible": true,
      },
    };
  }
);

// Run server
mcp.run({ transport: "streamable-http", port: 3000 });
```

## Example 3: Data Visualization App

### MCP Server

```python
from fastmcp import FastMCP
import pandas as pd
import json

mcp = FastMCP("data-visualizer")

@mcp.tool()
async def analyze_csv(file_url: str) -> dict:
    """
    Analyze a CSV file and create visualizations.

    Args:
        file_url: URL to CSV file

    Returns:
        Analysis results with interactive charts
    """
    # Load CSV
    df = pd.read_csv(file_url)

    # Basic statistics
    stats = {
        "rows": len(df),
        "columns": list(df.columns),
        "summary": df.describe().to_dict()
    }

    # Prepare chart data
    chart_data = []

    # For numeric columns, create histograms
    for col in df.select_dtypes(include=['number']).columns:
        hist_data = df[col].value_counts().head(10).to_dict()
        chart_data.append({
            "type": "bar",
            "title": f"Distribution of {col}",
            "data": {
                "labels": list(hist_data.keys()),
                "values": list(hist_data.values())
            }
        })

    return {
        "content": f"Analyzed CSV with {stats['rows']} rows and {len(stats['columns'])} columns",
        "structuredContent": {
            "statistics": stats,
            "charts": chart_data,
            "preview": df.head(10).to_dict('records')
        },
        "_meta": {
            "openai/outputTemplate": "ui://widget/data-viz.html",
            "openai/widgetAccessible": True
        }
    }
```

### Widget (data-viz.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Data Visualization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .chart-container {
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background: #f5f5f5;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <h2>Data Analysis Results</h2>

    <div id="stats"></div>
    <div id="charts"></div>
    <div id="preview"></div>

    <script>
        const data = window.openai.toolOutput;

        // Display statistics
        const statsDiv = document.getElementById('stats');
        statsDiv.innerHTML = `
            <p><strong>Rows:</strong> ${data.statistics.rows}</p>
            <p><strong>Columns:</strong> ${data.statistics.columns.join(', ')}</p>
        `;

        // Render charts
        const chartsDiv = document.getElementById('charts');

        data.charts.forEach((chart, index) => {
            const container = document.createElement('div');
            container.className = 'chart-container';
            container.innerHTML = `<h3>${chart.title}</h3>`;

            const canvas = document.createElement('canvas');
            canvas.id = `chart-${index}`;
            container.appendChild(canvas);
            chartsDiv.appendChild(container);

            new Chart(canvas, {
                type: chart.type,
                data: {
                    labels: chart.data.labels,
                    datasets: [{
                        label: chart.title,
                        data: chart.data.values,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        });

        // Display preview table
        const previewDiv = document.getElementById('preview');
        previewDiv.innerHTML = '<h3>Data Preview</h3>';

        if (data.preview.length > 0) {
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');

            // Header
            const headerRow = document.createElement('tr');
            Object.keys(data.preview[0]).forEach(key => {
                const th = document.createElement('th');
                th.textContent = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);

            // Rows
            data.preview.forEach(row => {
                const tr = document.createElement('tr');
                Object.values(row).forEach(value => {
                    const td = document.createElement('td');
                    td.textContent = value;
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });

            table.appendChild(thead);
            table.appendChild(tbody);
            previewDiv.appendChild(table);
        }
    </script>
</body>
</html>
```

## Best Practices from Examples

### 1. State Management

```javascript
// Initialize state
let state = window.openai.getWidgetState() || {
    selectedId: null,
    filters: {},
    view: "grid"
};

// Update state
function updateState(updates) {
    state = { ...state, ...updates };
    window.openai.setWidgetState(state);
}

// Use state
function restoreUIFromState() {
    if (state.selectedId) {
        selectItem(state.selectedId);
    }
    if (state.view === "list") {
        switchToListView();
    }
}
```

### 2. Error Handling

```javascript
async function callBackend(toolName, args) {
    try {
        const result = await window.openai.callTool(toolName, args);
        return result;
    } catch (error) {
        console.error(`Error calling ${toolName}:`, error);
        showErrorMessage(`Failed to ${toolName}. Please try again.`);
        return null;
    }
}
```

### 3. Loading States

```javascript
function showLoading(message = "Loading...") {
    document.getElementById('content').innerHTML = `
        <div style="text-align:center;padding:40px;">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
}

async function loadData() {
    showLoading("Fetching data...");
    const data = await callBackend("get_data", {});
    if (data) {
        renderData(data);
    }
}
```

These examples demonstrate the full capability of the Apps SDK for creating rich, interactive experiences in ChatGPT.
