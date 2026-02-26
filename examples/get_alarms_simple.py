import httpx
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def get_open_alarms_simple():
    """
    SIMPLE EXAMPLE: Direct REST API call with an embedded filter.
    Get all open alarms from the OpenGate platform.
    """
    # 1. Configuration from .env
    base_url = os.getenv("OPENGATE_BASE_URL", "https://api.opengate.es")
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
    
    # 2. Define the filter directly in the code
    payload = {
        "filter": {
            "eq": {
                "alarm.status": "OPEN"
            }
        },
        "limit": {
            "size": 10,
            "start": 1
        }
    }
    
    print(f"--- Simple Alarm Search ---")
    print(f"URL: {url}")
    
    async with httpx.AsyncClient(verify=verify_ssl) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            alarms = data if isinstance(data, list) else data.get("alarms", [])
            
            print(f"Found {len(alarms)} alarms.\n")
            for alarm in alarms:
                name = alarm.get("alarm.name", alarm.get("name", "N/A"))
                severity = alarm.get("alarm.severity", alarm.get("severity", "N/A"))
                print(f"- [{severity}] {name}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_open_alarms_simple())
