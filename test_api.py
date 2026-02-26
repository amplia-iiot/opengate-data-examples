import asyncio
import os
import json
from opengate_alarms.client import OpenGateAlarmClient
from opengate_alarms.models import SearchRequest
from dotenv import load_dotenv

async def test_retrieval():
    load_dotenv()
    client = OpenGateAlarmClient()
    print(f"Base URL: {client.base_url}")
    print(f"API Key: {client.api_key[:4]}..." if client.api_key else "No API Key")
    
    try:
        url = f"{client.base_url}/search/entities/alarms"
        print(f"Querying URL: {url}")
        
        import httpx
        async with httpx.AsyncClient(verify=client.verify_ssl) as hclient:
            # Try different payloads
            payloads = [
                {"filter": {}, "limit": 10, "offset": 0},
                {},
                {"filter": {"and": []}},
                {"filter": {"eq": {"alarm.status": "OPEN"}}}
            ]
            
            for p in payloads:
                print(f"\nTesting Payload: {json.dumps(p)}")
                try:
                    response = await hclient.post(url, headers=client.headers, json=p)
                    print(f"Status Code: {response.status_code}")
                    if response.status_code == 200:
                        print("SUCCESS!")
                        data = response.json()
                        if isinstance(data, list):
                            print(json.dumps(data[:1], indent=2))
                        else:
                            print(json.dumps(data, indent=2))
                        break
                    else:
                        print(f"Error: {response.text}")
                except Exception as e:
                    print(f"Request failed: {e}")

                
            # Now try with the client
            alarms = await client.query_alarms()
            print(f"Retrieved {len(alarms)} alarms via client")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_retrieval())
