import os
import time

from celery import Celery

CELERY_BROKER_URL =  os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
app = Celery('workers', broker=CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)


@app.task
def sum(x, y):
    time.sleep(55)
    return x + y