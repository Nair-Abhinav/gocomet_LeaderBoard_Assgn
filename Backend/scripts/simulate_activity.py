import requests
import random
import time

API_BASE_URL = "http://127.0.0.1:8000/api/leaderboard"

def submit_score(user_id, score):
    requests.post(f"{API_BASE_URL}/submit", json={
        "user_id": user_id,
        "score": score,
        "game_mode": random.choice(["solo", "team"])
    })

def get_top_players():
    return requests.get(f"{API_BASE_URL}/top").json()

if __name__ == "__main__":
    while True:
        top = get_top_players()

        if random.random() < 0.6 and top:
            # testing top 10 users for shuffling of leader board
            user_id = random.choice(top)["user_id"]
            score = random.randint(1000, 5000)
        else:
            user_id = random.randint(1, 10000)
            score = random.randint(10000, 30000)

        submit_score(user_id, score)
        time.sleep(1)
