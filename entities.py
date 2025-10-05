from typing import Union
import pygame
from config import (
    PLATFORM_DEFAULT_WIDTH, PLATFORM_HEIGHT, PLAYER_COLOR,
    WIDTH, HEIGHT, MAX_HP, PLAYER_SPEED
)

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width: int = PLATFORM_DEFAULT_WIDTH
        self.image: pygame.Surface = pygame.Surface((self.width, PLATFORM_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.hp: float = float(MAX_HP)
        self.score: int = 0

    def move(self, keys: pygame.key.ScancodeType) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def resize(self, new_width: int) -> None:
        self.width = max(60, min(300, new_width))  # limits
        self.image = pygame.Surface((self.width, PLATFORM_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        old_center = self.rect.centerx
        self.rect = self.image.get_rect(midbottom=(old_center, HEIGHT - 50))


class Item(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: tuple[int, int, int], speed: Union[int, float], size: int) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.color: tuple[int, int, int] = color
        self.speed: Union[int, float] = speed

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()