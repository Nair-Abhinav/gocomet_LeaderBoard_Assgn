from fastapi import FastAPI, Depends
from db import get_db
from schemas import SubmitScoreRequest
from crud import submit_score
from sqlalchemy import select, desc , func
from models import Leaderboard
from cache import redis_client
import json

app = FastAPI()

# testing redis
@app.get("/redis-health")
def redis_health():
    redis_client.set("ping", "pong")
    return {"redis": redis_client.get("ping")}


@app.get("/api/leaderboard/top")
async def get_top_leaderboard(db=Depends(get_db)):
    cache_key = "leaderboard:top10"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Leaderboard.user_id, Leaderboard.total_score)
        .order_by(desc(Leaderboard.total_score))
        .limit(10)
    )
    rows = result.all()

    data = [{"user_id": r[0], "total_score": r[1]} for r in rows]

    redis_client.setex(cache_key, 60, json.dumps(data))  # 5s TTL
    return data

@app.get("/api/leaderboard/rank/{user_id}")
async def get_player_rank(user_id: int, db=Depends(get_db)):
    # Get user's score
    result = await db.execute(
        select(Leaderboard.total_score).where(Leaderboard.user_id == user_id)
    )
    row = result.first()

    if not row:
        return {"error": "User not found on leaderboard"}

    user_score = row[0]

    # Count how many have higher score
    result = await db.execute(
        select(func.count()).select_from(Leaderboard)
        .where(Leaderboard.total_score > user_score)
    )
    higher_count = result.scalar_one()

    return {
        "user_id": user_id,
        "rank": higher_count + 1,
        "total_score": user_score
    }

# @app.get("/api/leaderboard/top")
# async def get_top_leaderboard(db=Depends(get_db)):
#     result = await db.execute(
#         select(Leaderboard.user_id, Leaderboard.total_score)
#         .order_by(desc(Leaderboard.total_score))
#         .limit(10)
#     )
#     rows = result.all()
#     return [{"user_id": r[0], "total_score": r[1]} for r in rows]


@app.post("/api/leaderboard/submit")
async def submit_score_api(payload: SubmitScoreRequest, db=Depends(get_db)):
    await submit_score(db, payload.user_id, payload.score, payload.game_mode)
    redis_client.delete("leaderboard:top10")
    return {"status": "ok"}

