import datetime
import uuid

from database import SessionLocal
from models import WeatherData, Batch

if __name__ == "__main__":
    # Create a new database session
    session = SessionLocal()
    try:
        # Create a WeatherData instance with example data
        batch_id = str(uuid.uuid4())
        batch = Batch(
            batch_id=batch_id,
            forecast_time = datetime.datetime.utcnow(),
            end_ingest_time = datetime.datetime.utcnow(),
        )

        data = WeatherData(
            lon=1.0,
            lat=2.0,
            forecast_time=datetime.datetime.utcnow(),
            temperature=23,
            precipitation_rate=12,
            humidity=14,
            batch_id=batch_id
        )

        # Add and commit the new WeatherData instance
        session.add(batch)
        session.add(data)
        session.commit()
        print("Inserted WeatherData:", data)
    except Exception as e:
        session.rollback()
        print(f"Failed to insert WeatherData: {e}")
    finally:
        session.close()
