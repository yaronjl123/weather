FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY common_requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./batch_ingestor /app/batch_ingestor
COPY ./common /app/common

CMD ["python", "-m", "batch_ingestor.main"]
