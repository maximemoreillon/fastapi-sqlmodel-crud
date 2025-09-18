from fastapi import FastAPI
from routes import items
from db import create_tables

app = FastAPI()

app.include_router(items.router)


@app.on_event("startup")
def on_startup():
    create_tables()
