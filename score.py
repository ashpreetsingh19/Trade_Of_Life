import json
import os
from typing import Optional
from config import HIGH_SCORE_FILE

class ScoreManager:
    @staticmethod
    def load_high_score() -> int:
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    return int(json.load(f))
            except (json.JSONDecodeError, ValueError, OSError) as e:
                print(f"Error loading high score: {e}")
                return 0
        return 0

    @staticmethod
    def save_high_score(score: int) -> int:
        current_high = ScoreManager.load_high_score()
        if score > current_high:
            try:
                with open(HIGH_SCORE_FILE, 'w') as f:
                    json.dump(score, f)
                return score
            except OSError as e:
                print(f"Error saving high score: {e}")
                return current_high
        return current_high