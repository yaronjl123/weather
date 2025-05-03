# Batch Ingestor Service

The **Batch Ingestor** is a service responsible for fetching weather data from external sources in batch form and writing it to the shared database. This process enables efficient, periodic updates of location-based weather history and summaries.

## What it does

- Uses an asynchronous client to fetch weather data for each batch.
- Processes all pages from the external batch source.
- Persists both metadata and detailed weather records to the database (see `common/database`).
- Updates ingestion status (active, inactive) and handles failures robustly.
- Can be run in a Docker container for reliable, repeatable batch ingestion.

---

## Building the Docker Image

Make sure your working directory is the project root (so that both `batch_ingestor`, `common`, and `requirements.txt` are accessible).  
Then, build the Docker image for the batch ingestor:

```bash
docker build -t batch-ingestor -f .\batch_ingestor\Dockerfile .
```

*This uses the provided `Dockerfile`, which copies `batch_ingestor`, the shared `common` library, and installs all requirements.*

---

## Running the Batch Ingestor Container

After building, you can run the service with:

```bash
docker run \
  --name batch-ingestor \
  -e DATABASE_URL="postgresql+psycopg_async://user:password@host:port/dbname" \
  batch-ingestor
```

- Set the `DATABASE_URL` (or any additional required environment variables for your configuration).
- By default, the container runs `python ./batch_ingestor/main.py` as the entrypoint.

---

## Source Code Structure

- `main.py`: Entrypoint for the service; orchestrates batch ingestion.
- `helpers.py`: Core logic for batch downloading and DB operations.
- `batch_client.py`: Handles API communication with the upstream weather batch provider.
- Uses shared code and models from `../common`.

---

For more API and schema details, refer to the root project [README.md](../README.md) and in-code docstrings.