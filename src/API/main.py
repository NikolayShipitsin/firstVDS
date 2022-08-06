
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from celery.result import AsyncResult


import workers

class Argument(BaseModel):
    first: int
    second: int

class Status(BaseModel):
    task_id: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from Celery"}


@app.post("/Createtask")
async def create_task(arguments: Argument):
    task = workers.sum.delay(arguments.first, arguments.second)
    return JSONResponse(status_code=201, content = {"task_id": task.id})

@app.post("/getstatus")
async def get_status(status: Status):
    task_result = AsyncResult(status.task_id)
    result = {
        "task_id": status.task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)

@app.get("/gettasks")
async def get_tasks():
    inspect = workers.app.control.inspect()
    active = inspect.active()
    task_count = 0
    for value in active.values():
        task_count += len(value)
    
    return JSONResponse({"task_count": task_count})
    #return JSONResponse(active)