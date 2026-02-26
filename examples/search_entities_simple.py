from opengate_data import OpenGateClient
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_devices_simple():
    """
    SIMPLE EXAMPLE: Using opengate-data library with embedded filters.
    Search for devices in a specific organization.
    """
    # 1. Configuration
    base_url = os.getenv("OPENGATE_BASE_URL", "https://api.opengate.es")
    if "/north/v80" in base_url:
        base_url = base_url.replace("/north/v80", "")
    
    api_key = os.getenv("OPENGATE_API_KEY")
    organization = os.getenv("OPENGATE_ORGANIZATION")
    
    # 2. Initialize the client
    client = OpenGateClient(api_key=api_key, url=base_url)
    
    print(f"--- Simple Entity Search ---")
    print(f"Searching in Org: {organization}")
    
    # 3. Build the search with embedded criteria
    try:
        builder = client.new_entities_search_builder()
        
        results_raw = (builder
            .with_organization_name(organization)
            .with_filter({"eq": {"resourceType": "entity.device"}})
            .with_select([
                {"name": "provision.device.identifier", "fields": [{"field": "value", "alias": "ID"}]},
                {"name": "provision.device.name", "fields": [{"field": "value", "alias": "NAME"}]}
            ])
            .with_limit(10, 1)
            .with_format("dict")
            .build_execute()
        )
        
        data = json.loads(results_raw)
        entities = data.get("entities", data.get("devices", []))
        
        print(f"Found {len(entities)} devices.\n")
        for entity in entities:
            print(f"- ID: {entity.get('ID')}, Name: {entity.get('NAME')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_devices_simple()
