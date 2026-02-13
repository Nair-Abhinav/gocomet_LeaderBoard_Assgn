from fastapi import FastAPI, Depends
from db import get_db
from schemas import SubmitScoreRequest
from crud import submit_score

app = FastAPI()

@app.post("/api/leaderboard/submit")
async def submit_score_api(payload: SubmitScoreRequest, db=Depends(get_db)):
    await submit_score(db, payload.user_id, payload.score, payload.game_mode)
    return {"status": "ok"}
