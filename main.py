import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing import List
from common.database import weather_data
from common import schemas
from common.database.weather_data import create_summary_materialized_view
from common.schemas import WeatherResponse

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_summary_materialized_view()
    yield


app = FastAPI(docs_url="/index",
              lifespan=lifespan)


@app.get("/weather/data", response_model=List[WeatherResponse])
async def get_weather_data(lat: float, lon: float):
    data = await weather_data.get_weather_data_by_location(lat=lat, lon=lon)

    return [
        schemas.WeatherResponse(forecast_time=item.forecast_time,
                                Temperature=item.temperature,
                                Humidity=item.humidity,
                                Precipitation_rate=item.precipitation_rate)
        for item in data
    ]


@app.get("/weather/summarize", response_model=schemas.WeatherSummary)
async def get_weather_summary(lat: float, lon: float):
    summary = await weather_data.summarize_weather_data_by_location(lat=lat, lon=lon)

    return {
        "max": {
            "Temperature": summary.max_temp,
            "Precipitation_rate": summary.max_precip,
            "Humidity": summary.max_hum
        },
        "min": {
            "Temperature": summary.min_temp,
            "Precipitation_rate": summary.min_precip,
            "Humidity": summary.min_hum
        },
        "avg": {
            "Temperature": summary.avg_temp,
            "Precipitation_rate": summary.avg_precip,
            "Humidity": summary.avg_hum
        }
    }


@app.get("/batches", response_model=List[schemas.BatchResponse])
async def get_batches():
    batches = await weather_data.list_batches()
    return [
        schemas.BatchResponse(
            batch_id=batch.batch_id,
            forecast_time=batch.forecast_time,
            number_of_rows=batch.number_of_rows,
            start_ingest_time=batch.start_ingest_time,
            end_ingest_time=batch.end_ingest_time,
            status=batch.status.name,
        ) for batch in batches
    ]

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
