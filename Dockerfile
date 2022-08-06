FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install -r requirements.txt && pip cache purge && rm requirements.txt
WORKDIR /app/
COPY src/workers/workers.py workers.py

ENTRYPOINT ["celery", "-A", "workers", "worker", "--loglevel=INFO"]