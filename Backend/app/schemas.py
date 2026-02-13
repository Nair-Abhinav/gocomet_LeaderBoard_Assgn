from pydantic import BaseModel

class SubmitScoreRequest(BaseModel):
    user_id: int
    score: int
    game_mode: str = "solo"
