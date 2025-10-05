from typing import Optional
import pygame
from config import WHITE, MAX_HP

class UI:
    def __init__(self) -> None:
        self._font_cache: dict[int, pygame.font.Font] = {}

    def get_font(self, size: int) -> pygame.font.Font:
        if size not in self._font_cache:
            self._font_cache[size] = pygame.font.SysFont(None, size)
        return self._font_cache[size]

    def draw_text(self, surface: pygame.Surface, text: str, size: int, x: int, y: int,
                color: tuple[int, int, int] = WHITE, center: bool = False) -> None:
        font = self.get_font(size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        surface.blit(text_surface, rect)

    def draw_hp_bar(self, surface: pygame.Surface, x: int, y: int, w: int, h: int,
                    player_hp: float) -> None:
        pygame.draw.rect(surface, (60, 60, 60), (x, y, w, h))
        ratio = player_hp / MAX_HP
        pygame.draw.rect(surface, (200, 60, 60), (x, y, int(w * ratio), h))
        pygame.draw.rect(surface, WHITE, (x, y, w, h), 2)