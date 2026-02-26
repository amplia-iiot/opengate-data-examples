import httpx
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def get_open_alarms():
    """
    Example of how to retrieve alarms using direct REST API calls with httpx.
    Reuses the filter definition from filters/alarms/open_alarms.json.
    """
    # Configuration
    base_url = os.getenv("OPENGATE_BASE_URL", "https://api.opengate.es")
    # Ensure the URL is correctly formed for the search endpoint
    if not base_url.endswith("/north/v80"):
        base_url = base_url.rstrip("/") + "/north/v80"
    
    url = f"{base_url}/search/entities/alarms"
    api_key = os.getenv("OPENGATE_API_KEY")
    verify_ssl = os.getenv("OPENGATE_VERIFY_SSL", "True").lower() == "true"
    
    headers = {
        "X-ApiKey": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Load filter from the project's filter directory
    filter_path = Path(__file__).parent.parent / "filters" / "alarms" / "open_alarms.json"
    if not filter_path.exists():
        print(f"Error: Filter file not found at {filter_path}")
        return

    with open(filter_path, "r") as f:
        payload = json.load(f)
    
    print(f"Querying {url}...")
    print(f"Using filter: {json.dumps(payload, indent=2)}")
    
    async with httpx.AsyncClient(verify=verify_ssl) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # The response is usually a list of alarms or a dict containing them
            alarms = data if isinstance(data, list) else data.get("alarms", [])
            
            print(f"\nFound {len(alarms)} open alarms:")
            for alarm in alarms:
                # Handle both direct field access and 'alarm.' prefixed fields
                alarm_id = alarm.get("identifier") or alarm.get("alarm.identifier", "N/A")
                entity_id = alarm.get("entityIdentifier") or alarm.get("alarm.entityIdentifier", "N/A")
                name = alarm.get("name") or alarm.get("alarm.name", "N/A")
                severity = alarm.get("severity") or alarm.get("alarm.severity", "N/A")
                
                print(f"- [{severity}] {name} (ID: {alarm_id}, Entity: {entity_id})")
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_open_alarms())
