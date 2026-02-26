import pytest
import respx
import httpx
from opengate_alarms.client import OpenGateAlarmClient
from opengate_alarms.models import Alarm, SearchRequest
from datetime import datetime

@pytest.mark.asyncio
async def test_query_alarms_mock():
    client = OpenGateAlarmClient(api_key="fake-key")
    url = f"{client.base_url}/search/entities/alarms"
    
    mock_response = [
        {
            "alarm.identifier": "AL-001",
            "alarm.entityIdentifier": "DEV-01",
            "alarm.name": "Test Alarm",
            "alarm.severity": "CRITICAL",
            "alarm.status": "OPEN",
            "alarm.creationDate": "2023-10-27T10:00:00Z"
        }
    ]

    async with respx.mock:
        respx.post(url).mock(return_value=httpx.Response(200, json=mock_response))
        
        alarms = await client.query_alarms()
        
        assert len(alarms) == 1
        assert alarms[0].id == "AL-001"
        assert alarms[0].severity == "CRITICAL"

@pytest.mark.asyncio
async def test_get_summary_mock():
    client = OpenGateAlarmClient(api_key="fake-key")
    url = f"{client.base_url}/search/entities/alarms/summary"
    
    mock_response = {
        "summary": {
            "date": "2023-10-27T10:00:00Z",
            "count": 1,
            "summaryGroup": [
                {
                    "severity": {
                        "count": 1,
                        "list": [{"count": 1, "name": "CRITICAL"}]
                    }
                }
            ]
        }
    }

    async with respx.mock:
        respx.post(url).mock(return_value=httpx.Response(200, json=mock_response))
        
        summary = await client.get_summary()
        
        assert summary.count == 1
        assert len(summary.summary_group) == 1
