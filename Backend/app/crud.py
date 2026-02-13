from sqlalchemy import select
from models import GameSession, Leaderboard, User

async def submit_score(db, user_id: int, score: int, game_mode: str):
    # Ensure user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(id=user_id, username=f"user_{user_id}")
        db.add(user)
        await db.flush()  # ensures user_id exists before FK insert

    # Insert game session
    session = GameSession(
        user_id=user_id,
        score=score,
        game_mode=game_mode
    )
    db.add(session)

    # Upsert leaderboard
    result = await db.execute(
        select(Leaderboard).where(Leaderboard.user_id == user_id)
    )
    leaderboard = result.scalar_one_or_none()

    if leaderboard:
        leaderboard.total_score += score
    else:
        leaderboard = Leaderboard(user_id=user_id, total_score=score)
        db.add(leaderboard)

    await db.commit()
