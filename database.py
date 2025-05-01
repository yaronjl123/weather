from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "postgresql://yaron:Y9d6gejABF0RHvmGW23VYdOvMud6g4aG@dpg-d09jve0gjchc7395mga0-a.oregon-postgres.render.com/weather_v4nt"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
