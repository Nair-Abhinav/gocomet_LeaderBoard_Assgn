from fastapi import FastAPI, Depends
from sqlalchemy import text
from db import engine
from models import Base

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/db-health")
async def db_health():
    return {"db": "connected"}
