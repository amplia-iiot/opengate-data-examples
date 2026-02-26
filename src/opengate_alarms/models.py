from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class Alarm(BaseModel):
    id: str = Field(alias="identifier")
    entity_id: str = Field(alias="entityIdentifier")
    name: str
    severity: str
    status: str
    creation_date: datetime = Field(alias="openingDate")
    rule: Optional[str] = None
    description: Optional[str] = None

    
    class Config:
        populate_by_name = True

class AlarmSummaryGroup(BaseModel):
    name: str
    count: int

class AlarmSummaryItem(BaseModel):
    count: int
    list: List[AlarmSummaryGroup]

class AlarmSummary(BaseModel):
    date: datetime
    count: int
    summary_group: List[Dict[str, AlarmSummaryItem]] = Field(alias="summaryGroup")

    class Config:
        populate_by_name = True

class Filter(BaseModel):
    and_: Optional[List[Any]] = Field(None, alias="and")
    or_: Optional[List[Any]] = Field(None, alias="or")
    eq: Optional[Dict[str, Any]] = None
    neq: Optional[Dict[str, Any]] = None
    gt: Optional[Dict[str, Any]] = None
    lt: Optional[Dict[str, Any]] = None
    gte: Optional[Dict[str, Any]] = None
    lte: Optional[Dict[str, Any]] = None
    like: Optional[Dict[str, Any]] = None
    in_: Optional[Dict[str, Any]] = Field(None, alias="in")
    nin: Optional[Dict[str, Any]] = Field(None, alias="nin")
    exists: Optional[Dict[str, Any]] = None

class SearchSort(BaseModel):
    field: str
    order: str = "DESC"

class Pagination(BaseModel):
    size: int = 50
    start: int = 1

class SearchRequest(BaseModel):
    filter: Dict[str, Any] = Field(default_factory=dict)
    limit: Pagination = Field(default_factory=Pagination)
    sort: Optional[List[SearchSort]] = None
    select: Optional[List[str]] = None

