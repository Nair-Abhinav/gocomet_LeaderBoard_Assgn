# Multiplayer Leaderboard System

## Overview
A scalable multiplayer gaming leaderboard built with FastAPI, PostgreSQL, and Redis.  
Supports score submission, top leaderboard retrieval, and player rank lookup with performance optimizations for high read/write traffic.

## Tech Stack
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Cache: Redis
- ORM: SQLAlchemy (Async)
- Tooling: Redis Insight, pgAdmin

## API Endpoints
- POST `/api/leaderboard/submit`  
  Submit a new game score for a user.
- GET `/api/leaderboard/top`  
  Fetch top 10 users by total score (cached with Redis).
- GET `/api/leaderboard/rank/{user_id}`  
  Fetch rank of a specific user.

## Data Model
- users(id, username, join_date)
- game_sessions(id, user_id, score, game_mode, timestamp)
- leaderboard(id, user_id UNIQUE, total_score)

## Performance Optimizations
- **Indexes** on:
  - `leaderboard(total_score DESC)`
  - `leaderboard(user_id UNIQUE)`
  - `game_sessions(user_id)`
- **Redis caching** for read-heavy `/top` endpoint with TTL.
- **Cache invalidation** on score submission to maintain near real-time consistency.

## Consistency & Concurrency
- Atomic DB writes for score submission.
- Leaderboard upserts using `ON CONFLICT (user_id)` to prevent duplicates.
- Cache invalidation ensures leaderboard freshness.

## Load Simulation
- Database seeded with ~10k users and ~50k game sessions locally.
- Python script used to simulate continuous score submissions and leaderboard reads.
- Redis Insight used to verify cache keys and TTL behavior.

## Trade-offs & Decisions
- Rank is computed dynamically using SQL instead of storing rank in DB to avoid denormalization issues.
- Redis TTL kept short to balance freshness and performance.
- Full-scale (1M+ users) load testing not run locally due to resource constraints; system design supports scale via indexing and caching.

## How to Run
```bash
# Start API
uvicorn app.main:app --reload

# Ensure PostgreSQL and Redis are running
