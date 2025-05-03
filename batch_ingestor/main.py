import asyncio
import logging
import os
import sys
from typing import List

from batch_ingestor.batch_client import BatchClient
from batch_ingestor.helpers import process_batches
from common.database.base import init_db
from common.database.weather_data import refresh_summary_materialized_view, delete_old_weather_data
from common.schemas import ExternalBatchResponse

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

logger = logging.getLogger()


async def main():
    await init_db()
    batch_client = BatchClient()
    page_semaphore = asyncio.Semaphore(os.environ.get("CONCURRENT_PAGES", 5))
    total_ingestion_timeout = os.environ.get("TOTAL_INGESTION_TIMEOUT", 300)
    batch_ingestion_timeout = os.environ.get("BATCH_INGESTION_TIMEOUT", 30)

    batch_metadatas: List[ExternalBatchResponse] = await batch_client.get_batches()
    ingested_batches, ingested_rows = await process_batches(page_semaphore, total_ingestion_timeout, batch_ingestion_timeout, batch_client, batch_metadatas)
    logger.info(f"ingested {ingested_rows} rows from {ingested_batches} batches")
    await delete_old_weather_data()
    await refresh_summary_materialized_view()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
