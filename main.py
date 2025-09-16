from fastapi import FastAPI
from routes import items
from db import create_db_and_tables
from contextlib import asynccontextmanager

app = FastAPI()

app.include_router(items.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
