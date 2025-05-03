import datetime
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from batch_ingestor.exceptions import BatchAlreadyProcessed
from common.database.base import SessionMaker
from common.database.models import Batch, WeatherData, IngestionStatus
from common.schemas import ExternalBatchResponse


logger = logging.getLogger()


async def save_batch_metadata(batch_metadata: ExternalBatchResponse):
    try:
        async with SessionMaker(expire_on_commit=False) as db_session:
            logger.info(f"saving batch metadata to DB, batch: {batch_metadata.batch_id}")
            batch = Batch(
                batch_id=batch_metadata.batch_id,
                forecast_time=batch_metadata.forecast_time,
                status="RUNNING"
            )
            db_session.add(batch)
            await db_session.commit()

            return batch
    except IntegrityError:
        raise BatchAlreadyProcessed(message=f"Batch {batch_metadata.batch_id} was already processed")


async def save_weather_data(batch, page, weather_response):
    async with SessionMaker() as db_session:
        logger.info(f"saving weather data to DB, batch: {batch.batch_id} page: {page}")
        db_session.add_all([WeatherData(
            lon=weather_data.longitude,
            lat=weather_data.latitude,
            forecast_time=batch.forecast_time,
            temperature=weather_data.temperature,
            precipitation_rate=weather_data.precipitation_rate,
            humidity=weather_data.humidity,
            batch_id=batch.batch_id) for weather_data in weather_response.data])
        await db_session.commit()


async def update_ingestion_end(batch: Batch, status: IngestionStatus, number_of_rows: int):
    async with SessionMaker() as db_session:
        batch.status = status
        batch.end_ingest_time = datetime.datetime.utcnow()
        batch.number_of_rows = number_of_rows
        db_session.merge(batch)
        await db_session.commit()


async def get_old_batch_ids():
    async with SessionMaker() as db_session:
        query = Query(Batch).where(Batch.status == IngestionStatus.ACTIVE).order_by(Batch.forecast_time).limit(6)
        results = await db_session.execute(query)
        latest_batches = results.scalars().all()

        if len(latest_batches) > 3:
            old_batch_ids = []
            for batch in latest_batches[3:]:
                batch.status = IngestionStatus.INACTIVE
                old_batch_ids.append(batch.batch_id)
            await db_session.commit()

            return old_batch_ids

        return []
