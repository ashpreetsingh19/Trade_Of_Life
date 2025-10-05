from typing import Tuple

# Window settings
WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60

# Game settings
MAX_HP: float = 100.0
ITEM_SPAWN_INTERVAL: int = 50
HP_DRAIN_RATE: float = 0.5 / 10  # lose 0.5 HP every 10 seconds smoothly
PLAYER_SPEED: int = 7
PLATFORM_DEFAULT_WIDTH: int = 150
PLATFORM_HEIGHT: int = 20

# Colors
BG_COLOR: Tuple[int, int, int] = (20, 22, 30)
PLAYER_COLOR: Tuple[int, int, int] = (120, 180, 255)
ITEM_GREEN: Tuple[int, int, int] = (0, 255, 120)
ITEM_RED: Tuple[int, int, int] = (255, 60, 60)
WHITE: Tuple[int, int, int] = (255, 255, 255)

# File paths
HIGH_SCORE_FILE: str = 'high_score.json'