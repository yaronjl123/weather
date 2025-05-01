from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine
import models, schemas, crud

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/weather/data", response_model=List[schemas.WeatherDataResponse])
def get_weather_data(lat: float, lon: float, db: Session = Depends(get_db)):
    data = crud.get_weather_data_by_location(db, lat=lat, lon=lon)
    return [
        schemas.WeatherDataResponse(
            forecastTime=item.forecast_time,
            Temperature=item.temperature,
            Precipitation_rate=item.precipitation_rate,
            Humidity=item.humidity
        ) for item in data
    ]


@app.get("/weather/summarize", response_model=schemas.WeatherSummary)
def get_weather_summary(lat: float, lon: float, db: Session = Depends(get_db)):
    summary = crud.summarize_weather_data_by_location(db, lat=lat, lon=lon)
    return summary


@app.get("/batches", response_model=List[schemas.BatchOut])
def get_batches(db: Session = Depends(get_db)):
    batches = crud.list_batches(db)
    return [
        schemas.BatchOut(
            batch_id=batch.batch_id,
            forecast_time=batch.forecast_time,
            number_of_rows=batch.number_of_rows,
            start_ingest_time=batch.start_ingest_time,
            end_ingest_time=batch.end_ingest_time,
            status=batch.status,
        ) for batch in batches
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#TODO- use Materialized View to cache average/min/max data and refresh it on ingestion
# nginx???
# lambda for ingestion?
