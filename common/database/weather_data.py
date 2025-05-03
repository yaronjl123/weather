import logging

from sqlalchemy.orm import Query

from common.database.base import SessionMaker
from common.database.batches import get_old_batch_ids
from common.database.models import Batch, WeatherData, MaterializedWeatherDataSummary
from typing import List
from sqlalchemy import text, delete

logger = logging.getLogger()

async def get_weather_data_by_location(lat: float, lon: float) -> List[WeatherData]:
    async with SessionMaker() as db_session:
        query = Query(WeatherData).where(WeatherData.lat == lat, WeatherData.lon == lon) \
            .order_by(WeatherData.forecast_time)
        results = await db_session.execute(query)

        return results.scalars().all()


async def summarize_weather_data_by_location(lat: float, lon: float):
    async with SessionMaker() as db_session:
        query = Query(MaterializedWeatherDataSummary).where(MaterializedWeatherDataSummary.lat == lat,
                                                            MaterializedWeatherDataSummary.lon == lon)
        results = await db_session.execute(query)

        return results.scalars().all()[0]


async def list_batches():
    async with SessionMaker() as db_session:
        results = await db_session.execute(Query(Batch))

        return results.scalars().all()


async def delete_old_weather_data():
    old_batch_ids = await get_old_batch_ids()
    logger.info(f"found {len(old_batch_ids)} old batches, deleting weather data. batch_ids: {old_batch_ids}")
    async with SessionMaker() as db_session:
        query = delete(WeatherData).where(WeatherData.batch_id.in_(old_batch_ids))
        await db_session.execute(query)
        await db_session.commit()


async def create_summary_materialized_view():
    async with SessionMaker() as db_session:
        statement = text("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS weather_data_summary AS
        SELECT
            lat,
            lon,
            MAX(temperature) AS max_temp,
            MAX(precipitation_rate) AS max_precip,
            MAX(humidity) AS max_hum,
            MIN(temperature) AS min_temp,
            MIN(precipitation_rate) AS min_precip,
            MIN(humidity) AS min_hum,
            AVG(temperature) AS avg_temp,
            AVG(precipitation_rate) AS avg_precip,
            AVG(humidity) AS avg_hum
        FROM weather_data
        GROUP BY lat, lon
        WITH DATA;
        CREATE INDEX IF NOT EXISTS mview_lat_lon ON weather_data_summary (lat, lon);
        """)

        await db_session.execute(statement)
        await db_session.commit()


async def refresh_summary_materialized_view():
    async with SessionMaker() as db_session:
        statement = text("REFRESH MATERIALIZED VIEW weather_data_summary;")
        await db_session.execute(statement)
        await db_session.commit()
