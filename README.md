# Weather Data Platform

This project provides an asynchronous, batch-based weather data ingestion and querying API built on SQLAlchemy and modern async Python tooling. The system consists of an ingestion service that loads weather data batches, makes them queryable through summary and granular weather endpoints, and manages historical/archival weather information in a relational database.

## Main Application — Overview

- **Data Ingestion**: The platform uses batch ingestion jobs to fetch weather data and persist it into the database. Each batch is associated with metadata such as ingestion time, forecast period, and status.
- **Weather Data Storage**: Weather data is stored in relational tables, along with materialized view summaries for efficient queries.
- **Query API**: The main app exposes endpoints for retrieving weather data and summaries by location, and for listing recent ingestion batches.

## Configuration via Environment Variables

The main application can be configured via the following environment variables:

| Variable                  | Description                                                                                  | Default      |
|---------------------------|----------------------------------------------------------------------------------------------|--------------|
| `DATABASE_URL`            | The async database connection string. Example: `postgresql+asyncpg://user:pass@host:port/db` | — (required) |
| `CONCURRENT_PAGES`        | The number of concurrent pages to ingest, set according to external api capability.          | 5            |
| `TOTAL_INGESTION_TIMEOUT` | Total timeout (in seconds) for processing all batches in one run.                            | 300          |
| `BATCH_INGESTION_TIMEOUT` | Timeout (in seconds) for processing a single batch.                                          | 30           |

You can set these via the shell before running the app, for example:

```bash
export DATABASE_URL="postgresql+psycopg_async://user:pass@localhost:5432/weatherdb"
export CONCURRENT_PAGES=10
export TOTAL_INGESTION_TIMEOUT=600
export BATCH_INGESTION_TIMEOUT=60
```

Or use a `.env` file or Docker environment configuration as appropriate.

## How to Use the API

The main application's API allows you to:

### 1. Get Historical Weather Data by Location

**Endpoint:**
```
GET /weather_data?lat=<latitude>&lon=<longitude>
```

**Description:**  
Returns time-series weather data (temperature, precipitation rate, humidity) for a given coordinate (latitude, longitude).

**Example:**
```
GET /weather_data?lat=40.7128&lon=-74.0060
```

**Response:**
```json
[
  {
    "forecast_time": "2024-06-01T13:00:00Z",
    "temperature": 22.5,
    "precipitation_rate": 0.1,
    "humidity": 58,
    "batch_id": "batch_123"
  },
  ...
]
```

### 2. Get Weather Data Summary by Location

**Endpoint:**
```
GET /weather_summary?lat=<latitude>&lon=<longitude>
```

**Description:**  
Returns max, min, and average weather parameters for the specified coordinates, aggregated from all batches.

**Example:**
```
GET /weather_summary?lat=40.7128&lon=-74.0060
```

**Response:**
```json
{
  "lat": 40.7128,
  "lon": -74.0060,
  "max_temp": 31.2,
  "min_temp": 17.6,
  "avg_temp": 24.3,
  "max_precip": 2.4,
  "min_precip": 0.0,
  "avg_precip": 0.35,
  "max_hum": 93,
  "min_hum": 45,
  "avg_hum": 64
}
```

### 3. List Ingestion Batches

**Endpoint:**
```
GET /batches
```

**Description:**  
Returns metadata for all weather data batches currently tracked in the system.

**Response:**
```json
[
  {
    "batch_id": "batch_123",
    "forecast_time": "2024-06-01T00:00:00Z",
    "number_of_rows": 241,
    "start_ingest_time": "2024-06-01T00:05:00Z",
    "end_ingest_time": "2024-06-01T00:08:00Z",
    "status": "ACTIVE"
  },
  ...
]
```

## Running the Service

1. Clone the repository and install dependencies (see `requirements.txt`).
2. Set the required environment variables.
3. Start the main app. 
4. Use the endpoints described above to interact with the weather data API.

## Batch Ingestor

For details about running ingestion jobs and using the associated Docker container, see the batch ingestor documentation or the Dockerfile for build instructions.

---

For further endpoint documentation or questions, please refer to the inline docstrings or open an issue!
