from opengate_data import OpenGateClient
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger("opengate_alarms.og_data")

class OpenGateDataHelper:
    def __init__(self, api_key: Optional[str] = None):
        try:
            self.api_key = api_key or os.getenv("OPENGATE_API_KEY")
            self.organization = os.getenv("OPENGATE_ORGANIZATION")
            env_url = os.getenv("OPENGATE_BASE_URL")
            
            # The opengate-data client seems to append its own path (e.g., /north/v80)
            # so we should provide just the base host/URL as RESOURCE.
            if env_url:
                self.base_url = env_url.rstrip("/")
            else:
                self.base_url = "https://api.opengate.es"
                
            self.verify_ssl = os.getenv("OPENGATE_VERIFY_SSL", "True").lower() == "true"
            
            logger.info(f"Initializing OpenGateDataHelper - Base URL: {self.base_url} - Org: {self.organization} - Verify SSL: {self.verify_ssl}")
            
            # The opengate-data client: url parameter is actually the 'resource' (base url)
            self.client = OpenGateClient(api_key=self.api_key, url=self.base_url)

        except Exception as e:
            logger.error(f"Error initializing OpenGateClient: {e}", exc_info=True)

    def search_entities(self, search_request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search entities using the opengate-data library builder pattern."""
        logger.info(f"search_entities called with: {search_request}")
        try:
            # Call the method to get a new builder instance
            builder = self.client.new_entities_search_builder()
            
            if self.organization:
                logger.debug(f"Adding organization: {self.organization}")
                builder.with_organization_name(self.organization)
            
            if "filter" in search_request:
                logger.debug(f"Adding filter: {search_request['filter']}")
                builder.with_filter(search_request["filter"])
            
            if "select" in search_request:
                logger.debug(f"Adding select: {search_request['select']}")
                builder.with_select(search_request["select"])
                
            if "limit" in search_request:
                limit_data = search_request["limit"]
                if isinstance(limit_data, dict):
                    size = limit_data.get("size", 25)
                    start = limit_data.get("start", 1)
                    builder.with_limit(size, start)
                    logger.debug(f"Applied limit size from request: {size}, start: {start}")
            else:
                # Enforce default limit to avoid loading too many entities
                logger.info("No limit provided in request, applying default size of 25")
                builder.with_limit(25, 1)
            
            logger.info("Building and executing entity search...")
            # The library returns a JSON string when formatted as 'dict'
            results_raw = builder.with_format("dict").build_execute()
            
            if isinstance(results_raw, str):
                import json
                try:
                    data = json.loads(results_raw)
                    # The response key can be 'entities', 'devices', etc.
                    results = []
                    for key in ["entities", "devices", "alarms", "datapoints", "operations"]:
                        if key in data and isinstance(data[key], list):
                            results = data[key]
                            logger.info(f"Search successful. Parsed {len(results)} items from '{key}' key.")
                            break
                    return results
                except Exception as e:
                    logger.error(f"Failed to parse entities JSON: {e}")
                    return []
            
            # Fallback if it's already a list or other format
            logger.info(f"Search completed. Found {len(results_raw) if results_raw else 0} results.")
            return results_raw if isinstance(results_raw, list) else []
        except Exception as e:
            logger.error(f"Error in search_entities: {e}", exc_info=True)
            return []





