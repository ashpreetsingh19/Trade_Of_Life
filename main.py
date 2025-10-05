import sys
import random
import pygame
import json
import numpy
from typing import Optional
import importlib.util

if importlib.util.find_spec("config") is None:
    from config import *
else:

    WIDTH, HEIGHT = 800, 600
    FPS = 60
    MAX_HP = 100
    ITEM_SPAWN_INTERVAL = 50
    HP_DRAIN_RATE = 0.5 / 10
    PLAYER_SPEED = 7
    PLATFORM_DEFAULT_WIDTH = 150
    PLATFORM_HEIGHT = 20

    BG_COLOR = (20, 22, 30)
    PLAYER_COLOR = (120, 180, 255)
    ITEM_GREEN = (0, 255, 120)
    ITEM_RED = (255, 60, 60)
    WHITE = (255, 255, 255)

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Trade of Life")
        self.clock = pygame.time.Clock()
        self.font_cache = {}
        self.setup_audio()
        self.reset_game()
        
    def setup_audio(self) -> None:

        pygame.mixer.music.load('assets/music/background.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
            
        self.sounds = {
            'good_item': self.create_beep_sound(700, 100),
            'bad_item': self.create_beep_sound(400, 100)
        }

    def create_beep_sound(self, frequency: int, duration: int) -> pygame.mixer.Sound:
        sample_rate = 44100
        samples = int(duration * sample_rate / 1000) 

        buf = numpy.zeros((samples, 2), dtype=numpy.int16)
        max_sample = 2**(16 - 1) - 1
        for i in range(samples):
            t = float(i) / sample_rate
            buf[i][0] = int(max_sample * numpy.sin(2.0 * numpy.pi * frequency * t))
            buf[i][1] = buf[i][0]

        return pygame.mixer.Sound(buffer=buf)

    def get_font(self, size: int) -> pygame.font.Font:
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.SysFont(None, size)
        return self.font_cache[size]

    def draw_text(self, text: str, size: int, x: int, y: int, 
                 color: tuple[int, int, int] = WHITE, center: bool = False) -> None:
        font = self.get_font(size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)

    def draw_hp_bar(self, player) -> None:
        bar_x, bar_y, bar_w, bar_h = 20, 20, 200, 20
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        ratio = player.hp / MAX_HP
        pygame.draw.rect(self.screen, (200, 60, 60), (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)

    def reset_game(self) -> None:
        self.state = "waiting"
        self.player = Player()
        self.items = pygame.sprite.Group()
        self.spawn_counter = 0
        self.high_score = self.load_high_score()

    def load_high_score(self) -> int:
        try:
            with open('high_score.json', 'r') as f:
                return int(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return 0

    def save_high_score(self, score: int) -> int:
        current_high = self.load_high_score()
        if score > current_high:
            try:
                with open('high_score.json', 'w') as f:
                    json.dump(score, f)
                return score
            except OSError:
                return current_high
        return current_high

    def handle_input(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    self.toggle_game_state()
        return True

    def toggle_game_state(self) -> None:
        if self.state == "waiting":
            self.state = "playing"
            pygame.mixer.music.unpause()
        elif self.state == "playing":
            self.state = "paused"
            pygame.mixer.music.pause()
        elif self.state == "paused":
            self.state = "playing"
            pygame.mixer.music.unpause()
        elif self.state == "game_over":
            self.reset_game()
            self.state = "playing"
            pygame.mixer.music.play(-1)

    def spawn_item(self, fall_speed: float, item_size: int) -> None:
        is_good = random.random() < max(0.4, 0.7 - self.player.score / 500)
        color = ITEM_GREEN if is_good else ITEM_RED
        x = random.randint(20, WIDTH - 20)
        self.items.add(Item(x, 0, color, fall_speed, item_size))

    def update(self, dt: float) -> None:
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        self.player.hp -= HP_DRAIN_RATE * dt * FPS
        self.player.hp = max(0, self.player.hp)

        fall_speed = 4 + self.player.score // 50
        spawn_interval = max(15, ITEM_SPAWN_INTERVAL - self.player.score // 20)
        item_size = max(15, 30 - self.player.score // 100)

        self.spawn_counter += 1
        if self.spawn_counter >= spawn_interval:
            self.spawn_counter = 0
            self.spawn_item(fall_speed, item_size)

        self.items.update()
        self.handle_collisions()

        if self.player.hp <= 0:
            self.state = "game_over"
            self.high_score = self.save_high_score(self.player.score)

    def handle_collisions(self) -> None:
        for item in pygame.sprite.spritecollide(self.player, self.items, True):
            if item.color == ITEM_GREEN:
                self.player.hp = min(MAX_HP, self.player.hp + 5)
                self.player.score += 10
                self.sounds['good_item'].play()
                if self.player.resize(self.player.width - 10):
                    self.state = "game_over"
                    self.high_score = self.save_high_score(self.player.score)
            else:
                self.player.hp = max(0, self.player.hp - 5)
                self.sounds['bad_item'].play()
                if self.player.resize(self.player.width + 10):
                    self.state = "game_over"
                    self.high_score = self.save_high_score(self.player.score)

    def draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.items.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_hp_bar(self.player)
        self.draw_text(f"Score: {self.player.score}", 26, WIDTH - 180, 18)

        if self.state == "waiting":
            self.draw_text("Press SPACEBAR to Start", 36, WIDTH // 2, HEIGHT // 2, center=True)
        elif self.state == "paused":
            self.draw_text("Paused - Press SPACEBAR to Resume", 36, WIDTH // 2, HEIGHT // 2, center=True)
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_game_over(self) -> None:
        self.draw_text("Game Over", 60, WIDTH // 2, HEIGHT // 2 - 60, center=True)
        self.draw_text(f"Final Score: {self.player.score}", 36, WIDTH // 2, HEIGHT // 2, center=True)
        
        color = ITEM_GREEN if self.player.score >= self.high_score else WHITE
        self.draw_text(f"High Score: {self.high_score}", 36, WIDTH // 2, HEIGHT // 2 + 40, center=True, color=color)
        
        if self.player.score >= self.high_score and self.player.score > 0:
            self.draw_text("New High Score!", 36, WIDTH // 2, HEIGHT // 2 + 80, center=True)
        
        self.draw_text("Press SPACEBAR to Restart or ESC to Quit", 36, WIDTH // 2, HEIGHT // 2 + 120, center=True)

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_input()
            self.update(dt)
            self.draw()
            pygame.display.flip()

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = PLATFORM_DEFAULT_WIDTH
        self.image = pygame.Surface((self.width, PLATFORM_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.hp = float(MAX_HP)
        self.score = 0

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def resize(self, new_width: int) -> bool:
        test_width = max(0, min(300, new_width))
        if test_width == 0:
            self.hp = 0
            return True
            
        self.width = max(5, min(300, new_width))  # Actual limits for visual
        self.image = pygame.Surface((self.width, PLATFORM_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        old_center = self.rect.centerx
        self.rect = self.image.get_rect(midbottom=(old_center, HEIGHT - 50))
        return False


class Item(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: tuple[int, int, int], speed: float, size: int) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.speed = speed

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


if __name__ == "__main__":
    game = Game()
    game.run()