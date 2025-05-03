from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class WeatherResponse(BaseModel):
    forecast_time: datetime
    Temperature: float
    Humidity: float
    Precipitation_rate: float


class ExternalWeatherDataMetadata(BaseModel):
    batch_id: str
    count: int
    page: int
    total_items: int
    total_pages: int


class ExternalWeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    humidity: float
    precipitation_rate: float


class ExternalWeatherDataResponse(BaseModel):
    metadata: ExternalWeatherDataMetadata
    data: List[ExternalWeatherResponse]


class ExternalBatchResponse(BaseModel):
    batch_id: str
    forecast_time: datetime


class WeatherSummary(BaseModel):
    max: dict
    min: dict
    avg: dict


class BatchResponse(BaseModel):
    batch_id: str
    forecast_time: datetime
    number_of_rows: int
    start_ingest_time: datetime
    end_ingest_time: Optional[datetime]
    status: str
