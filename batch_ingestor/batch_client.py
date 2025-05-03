from typing import List

import httpx
from httpx_retries import Retry, RetryTransport

from common.schemas import ExternalBatchResponse, ExternalWeatherDataResponse


class BatchClient:
    API_BASE_URL = "https://us-east1-climacell-platform-production.cloudfunctions.net/weather-data"

    def __init__(self):
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 502, 503, 504, 500, 404])
        self.requests_client = httpx.AsyncClient(transport=RetryTransport(retry=retry))

    async def get_batches(self) -> List[ExternalBatchResponse]:
        response = await self.requests_client.get(f"{self.API_BASE_URL}/batches")
        response.raise_for_status()
        json_response = response.json()

        return [ExternalBatchResponse.model_validate(model_dict) for model_dict in json_response]

    async def get_batch(self, batch_id: str, page: int) -> ExternalWeatherDataResponse:
        response = await self.requests_client.get(f"{self.API_BASE_URL}/batches/{batch_id}", params=dict(page=page))
        response.raise_for_status()
        response_json = response.json()

        return ExternalWeatherDataResponse.model_validate(response_json)
