from fastapi import FastAPI, Depends
from sqlalchemy import text
from db import get_db
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/db-health")
async def db_health(db=Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"db": "connected"}