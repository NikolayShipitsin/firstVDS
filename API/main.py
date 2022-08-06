from typing import Dict, Union
from click import argument
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel


from . import workers

class Argument(BaseModel):
    first: int
    second: int


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from Celery"}


@app.post("/Createtask", status_code=201)
async def create_task(arguments: Argument):
    task = workers.sum.delay(arguments.first, arguments.second)
    return JSONResponse({"task_id": task.id})
