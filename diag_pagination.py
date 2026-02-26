import logging
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from opengate_alarms.og_data import OpenGateDataHelper

logging.basicConfig(level=logging.ERROR)

def main():
    helper = OpenGateDataHelper()
    # Request with a very small limit
    request = {
        "filter": {"eq": {"resourceType": "entity.device"}},
        "limit": {"size": 2, "start": 1}
    }
    print("Starting search with limit 2...")
    results = helper.search_entities(request)
    print(f"Results raw type: {type(results)}")
    
    if isinstance(results, list):
        print(f"Entities found: {len(results)}")
        if len(results) > 0:
            print(f"First result keys: {list(results[0].keys())}")
    else:
        print(f"Unexpected result type: {type(results)}")

if __name__ == "__main__":
    main()
