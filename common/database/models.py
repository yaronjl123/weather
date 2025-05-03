import enum

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Index
from common.database.base import Base
import datetime


class IngestionStatus(enum.Enum):
    RUNNING = 1
    ACTIVE = 2
    INACTIVE = 3


class Batch(Base):
    __tablename__ = 'batches'

    batch_id = Column(String, primary_key=True, index=True, nullable=False)
    forecast_time = Column(DateTime, nullable=False)
    number_of_rows = Column(Integer, default=0)
    start_ingest_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_ingest_time = Column(DateTime, nullable=True)
    status = Column(Enum(IngestionStatus), default=IngestionStatus.RUNNING)


class WeatherData(Base):
    __tablename__ = 'weather_data'
    __table_args__ = (Index('lon_lat', "lon", "lat"),)

    id = Column(Integer, primary_key=True, index=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    forecast_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    precipitation_rate = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    batch_id = Column(String, ForeignKey('batches.batch_id'))


class MaterializedWeatherDataSummary(Base):
    __tablename__ = "weather_data_summary"
    __table_args__ = (Index('lon_lat', "lon", "lat"),)

    lon = Column(Float, primary_key=True)
    lat = Column(Float, primary_key=True)
    max_temp = Column(Float)
    max_precip = Column(Float)
    max_hum = Column(Float)
    min_temp = Column(Float)
    min_precip = Column(Float)
    min_hum = Column(Float)
    avg_temp = Column(Float)
    avg_precip = Column(Float)
    avg_hum = Column(Float)
