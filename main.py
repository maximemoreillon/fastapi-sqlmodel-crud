from fastapi import FastAPI
from routes import items
from db import create_tables
from contextlib import asynccontextmanager

app = FastAPI()

app.include_router(items.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
