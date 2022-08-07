import os
import time

from celery import Celery
from celery import states
from celery.exceptions import Ignore

CELERY_BROKER_URL =  os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
FILE_DIR = "data"
app = Celery('workers', broker=CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)


# @app.task
# def sum(x, y):
#     time.sleep(55)
#     return x + y

@app.task(bind=True)
def sum(self, filename):
    file_path = os.path.join(FILE_DIR, filename)
    try:
        file = open(file_path)
    except IOError as e:
        self.update_state(state="FAIL", meta={"custom": "Problem with file"})
        raise Ignore()
    else:
        with file:
            result = processing_file(file)
    
    return result


def processing_file(file_obj):
    first_line = True
    accum = []
    for line in file_obj:
        line = line.replace('"', '')
        if first_line:
            columns = line.split(",")
            columns = columns[1::10]
            for _ in range(len(columns)):
                accum.append(0)
            first_line = False
            continue
        columns = line.split(",")
        columns = columns[1::10]
        print(columns)
        accum = [x + 0 if y == '' else x + float(y)  for x, y in zip(accum, columns)]
    
    return accum