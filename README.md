# OpenGate Alarms & Entities TUI

A TUI (Terminal User Interface) tool to manage alarms and search for entities in the OpenGate IoT platform by Amplia.

## Features

- **Alarm Management**: Real-time visualization and filtering of alarms.
- **Entity Search**: Advanced device and asset search using the `opengate-data` builder.
- **Custom Filters**: Support for complex JSON filters with field selection (`select`) and aliases.
- **Automatic Pagination**: Default limits to ensure a smooth interface.

## Project Structure

The UI's behavior is driven by JSON configuration files located in the `filters/` directory:

- **`filters/alarms/`**: Contains search criteria for the Alarms tab.
- **`filters/entities/`**: Defines filters, pagination settings, and field selection (`select`) for the Entities tab.

Any `.json` file added to these directories will automatically appear in the TUI's sidebar.

## Requirements and Configuration

The project uses `uv` for dependency management.

1. **Install uv**:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **Configure environment variables**:
    Create a `.env` file in the root directory with:

    ```env
    OPENGATE_API_KEY=your_api_key
    OPENGATE_BASE_URL=https://api.opengate.es
    OPENGATE_ORGANIZATION=your_organization
    OPENGATE_VERIFY_SSL=False
    ```

## TUI Usage

To run the application:

```bash
uv run opengate-tui
```

- **q**: Quit.
- **r**: Refresh data for the selected filter.
- **Tab**: Switch between Alarms and Entities.

---

## Examples (Standalone Scripts)

The project includes ready-to-use scripts in the `examples/` directory that demonstrate API usage independently of the TUI. These scripts reuse the JSON configurations from the `filters/` folder.

To run them with `uv`:

```bash
# RECOMENDED: Simplified examples with filters inside the code
uv run examples/get_alarms_simple.py
uv run examples/search_entities_simple.py

# Advanced examples loading filters from JSON files
uv run examples/get_alarms.py
uv run examples/search_entities.py
```

## Integration Examples (API)

### 1. Retrieving Alarms (REST with httpx)

Example of how to retrieve open alarms. You can load a filter from a JSON file or define it directly in your code.

> [!TIP]
> **Recommended**: See [examples/get_alarms_simple.py](file:///home/charlie/Dropbox/Charlie/0-Env/amplia/1-Projects/endesa-ai-data/opengate-alarms/examples/get_alarms_simple.py) for the simplest version.
> See [examples/get_alarms.py](file:///home/charlie/Dropbox/Charlie/0-Env/amplia/1-Projects/endesa-ai-data/opengate-alarms/examples/get_alarms.py) for loading filters from files.

```python
import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def get_open_alarms():
    url = f"{os.getenv('OPENGATE_BASE_URL')}/north/v80/search/entities/alarms"
    headers = {"X-ApiKey": os.getenv("OPENGATE_API_KEY"), "Content-Type": "application/json"}
    
    # Simplified: Define filter directly
    payload = {
        "filter": {"eq": {"alarm.status": "OPEN"}},
        "limit": {"size": 10, "start": 1}
    }
    
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()
```

### 2. Searching Entities (with opengate-data)

Using the search builder to retrieve active devices.

> [!TIP]
> **Recommended**: See [examples/search_entities_simple.py](file:///home/charlie/Dropbox/Charlie/0-Env/amplia/1-Projects/endesa-ai-data/opengate-alarms/examples/search_entities_simple.py) for the simplest version.
> See [examples/search_entities.py](file:///home/charlie/Dropbox/Charlie/0-Env/amplia/1-Projects/endesa-ai-data/opengate-alarms/examples/search_entities.py) for the advanced version.

```python
from opengate_data import OpenGateClient
import os
import json

client = OpenGateClient(
    api_key=os.getenv("OPENGATE_API_KEY"), 
    url=os.getenv("OPENGATE_BASE_URL")
)

def search_devices():
    builder = client.new_entities_search_builder()
    
    # Simplified: Build query directly
    results = (builder
        .with_organization_name(os.getenv("OPENGATE_ORGANIZATION"))
        .with_filter({"eq": {"resourceType": "entity.device"}})
        .with_limit(10, 1)
        .with_format("dict")
        .build_execute()
    )
    return json.loads(results)
```

> [!TIP]
> The `opengate-data` library returns a JSON string when using `.with_format("dict")`. Don't forget to parse it with `json.loads()`!
