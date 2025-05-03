import asyncio
import logging
from asyncio import Semaphore, FIRST_EXCEPTION, ALL_COMPLETED

from batch_ingestor.batch_client import BatchClient
from batch_ingestor.exceptions import BatchFailedToProcessException, FailedToIngestWeatherData, BatchAlreadyProcessed
from common.database.batches import save_batch_metadata, save_weather_data, update_ingestion_end
from common.database.models import Batch, IngestionStatus
from common.schemas import ExternalWeatherDataResponse, ExternalBatchResponse


logger = logging.getLogger()


async def ingest_page(page_semaphore: Semaphore, batch_client: BatchClient, batch: Batch, page):
    try:
        async with page_semaphore:
            logger.info(f"ingesting batch: {batch.batch_id} page: {page}")
            weather_response: ExternalWeatherDataResponse = await batch_client.get_batch(batch.batch_id, page)
        await save_weather_data(batch, page, weather_response)

        return len(weather_response.data), weather_response.metadata.total_pages

    except Exception as e:
        raise FailedToIngestWeatherData(page=page, batch_id=batch.batch_id, error=str(e))


async def process_batch(page_semaphore: Semaphore, batch_ingestion_timeout: int, batch_client: BatchClient, batch_metadata: ExternalBatchResponse):
    try:
        batch: Batch = await save_batch_metadata(batch_metadata)
    except BatchAlreadyProcessed as e:
        logger.error(str(e))
        raise BatchFailedToProcessException(message=str(e))

    total_ingested = 0
    try:
        total_ingested, total_pages = await ingest_page(page_semaphore, batch_client, batch, page=0)
        tasks = [asyncio.create_task(ingest_page(page_semaphore, batch_client, batch, page)) for page in range(1, total_pages+1)]
        done, not_done = await asyncio.wait(tasks, timeout=batch_ingestion_timeout, return_when=FIRST_EXCEPTION)
        total_ingested += sum([task.result()[0] for task in done if task.exception() is None])

        await update_ingestion_end(batch, IngestionStatus.ACTIVE, total_ingested)
    except FailedToIngestWeatherData as e:
        logger.exception(e)
        await update_ingestion_end(batch, IngestionStatus.INACTIVE, total_ingested)
        raise BatchFailedToProcessException(message=str(e))

    return total_ingested


async def process_batches(page_semaphore, total_ingestion_timeout, batch_ingestion_timeout, batch_client, batch_metadatas):
    logger.info(f"Processing {len(batch_metadatas)} batches...")
    tasks = [asyncio.create_task(process_batch(page_semaphore, batch_ingestion_timeout, batch_client, batch_metadata)) for batch_metadata in batch_metadatas]
    done, not_done = await asyncio.wait(tasks, timeout=total_ingestion_timeout, return_when=ALL_COMPLETED)
    results = [task.result() for task in done if task.exception() is None]

    return len(results), sum(results)
