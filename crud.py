from sqlalchemy.orm import Session
from models import WeatherData, Batch
from schemas import WeatherDataResponse, BatchOut
from typing import List
from sqlalchemy import func

def get_weather_data_by_location(db: Session, lat: float, lon: float) -> List[WeatherData]:
    return db.query(WeatherData).filter(
        WeatherData.lat == lat, WeatherData.lon == lon
    ).order_by(WeatherData.forecast_time).all()

def summarize_weather_data_by_location(db: Session, lat: float, lon: float):
    q = db.query(
        func.max(WeatherData.temperature).label('max_temp'),
        func.max(WeatherData.precipitation_rate).label('max_precip'),
        func.max(WeatherData.humidity).label('max_hum'),
        func.min(WeatherData.temperature).label('min_temp'),
        func.min(WeatherData.precipitation_rate).label('min_precip'),
        func.min(WeatherData.humidity).label('min_hum'),
        func.avg(WeatherData.temperature).label('avg_temp'),
        func.avg(WeatherData.precipitation_rate).label('avg_precip'),
        func.avg(WeatherData.humidity).label('avg_hum'),
    ).filter(
        WeatherData.lat == lat,
        WeatherData.lon == lon
    ).one()

    result = {
        "max": {
            "Temperature": q.max_temp,
            "Precipitation_rate": q.max_precip,
            "Humidity": q.max_hum
        },
        "min": {
            "Temperature": q.min_temp,
            "Precipitation_rate": q.min_precip,
            "Humidity": q.min_hum
        },
        "avg": {
            "Temperature": q.avg_temp,
            "Precipitation_rate": q.avg_precip,
            "Humidity": q.avg_hum
        }
    }
    return result

def list_batches(db: Session):
    batches = db.query(Batch).all()
    return batches