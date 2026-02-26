import httpx
import os
from typing import List, Optional, Dict, Any
from .models import Alarm, AlarmSummary, SearchRequest
from dotenv import load_dotenv

import logging
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("opengate_alarms.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("opengate_alarms.client")

class OpenGateAlarmClient:

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENGATE_API_KEY")
        # Use provided base_url, or env var, or default to production
        env_url = os.getenv("OPENGATE_BASE_URL")
        if env_url:
            # Ensure we append the path if it's just the host
            if not env_url.endswith("/north/v80"):
                env_url = env_url.rstrip("/") + "/north/v80"
            self.base_url = env_url
        else:
            self.base_url = base_url or "https://api.opengate.es/north/v80"
        
        self.verify_ssl = os.getenv("OPENGATE_VERIFY_SSL", "True").lower() == "true"
        
        self.headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def query_alarms(self, search_request: Optional[SearchRequest] = None) -> List[Alarm]:
        if search_request is None:
            search_request = SearchRequest()

        url = f"{self.base_url}/search/entities/alarms"
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            payload = search_request.model_dump(by_alias=True, exclude_none=True)
            # If payload is just default values (empty filter and default pagination), some APIs prefer empty dict
            if not payload.get("filter") and payload.get("limit", {}).get("size") == 50 and payload.get("limit", {}).get("start") == 1:
                payload = {}
            
            logger.info(f"Querying alarms - URL: {url} - Payload: {payload}")

            
            response = await client.post(url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                logger.error(f"API Error {response.status_code}: {response.text}")
            
            response.raise_for_status()
            data = response.json()

            # The API usually returns a list of alarms directly or inside a field
            # Based on docs, it returns a list of alarms
            if isinstance(data, list):
                return [Alarm(**item) for item in data]
            elif "alarms" in data:
                return [Alarm(**item) for item in data["alarms"]]
            return []

    async def get_summary(self, filter_data: Optional[Dict[str, Any]] = None) -> AlarmSummary:
        url = f"{self.base_url}/search/entities/alarms/summary"
        payload = {"filter": filter_data or {}}
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return AlarmSummary(**data["summary"])

    async def change_state(self, action: str, alarm_ids: List[str], notes: Optional[str] = None) -> bool:
        url = f"{self.base_url}/alarms"
        payload = {
            "action": action, # ATTEND or CLOSE
            "alarms": alarm_ids,
            "notes": notes
        }
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            return response.status_code == 200

