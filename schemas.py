from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WeatherDataResponse(BaseModel):
    forecastTime: datetime
    Temperature: float
    Precipitation_rate: float
    Humidity: float

    class Config:
        orm_mode = True

class WeatherSummary(BaseModel):
    max: dict
    min: dict
    avg: dict

class BatchOut(BaseModel):
    batch_id: str
    forecast_time: datetime
    number_of_rows: int
    start_ingest_time: datetime
    end_ingest_time: Optional[datetime]
    status: str

    class Config:
        orm_mode = True