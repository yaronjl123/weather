from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
import datetime

class Batch(Base):
    __tablename__ = 'batches'
    batch_id = Column(String, primary_key=True, index=True, nullable=False)
    forecast_time = Column(DateTime, nullable=False)
    number_of_rows = Column(Integer, default=0)
    start_ingest_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_ingest_time = Column(DateTime, nullable=True)
    status = Column(String, default="RUNNING")  # RUNNING, ACTIVE, INACTIVE


class WeatherData(Base):
    __tablename__ = 'weather_data'
    #TODO - index for (lon, lat)?
    id = Column(Integer, primary_key=True, index=True)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    forecast_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
    precipitation_rate = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

    batch_id = Column(String, ForeignKey('batches.batch_id'), index=True)
