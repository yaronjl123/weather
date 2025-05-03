class FailedToIngestWeatherData(Exception):
    def __init__(self, page, batch_id, error):
        message = f"Failed to ingest page {page} of batch {batch_id}, got error: {error}"
        super().__init__(message)


class BatchFailedToProcessException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BatchAlreadyProcessed(Exception):
    def __init__(self, message):
        super().__init__(message)
