import pygame
import sys
import random
import math
import os

from main_code import config
from main_code.config import ScreenSize

# Инициализация PyGame
pygame.init()
WIDTH, HEIGHT = ScreenSize.WIDTH.value,ScreenSize.HEIGHT.value
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vegetable Defense")
clock = pygame.time.Clock()

# Конфигурация путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "lyla_imag")

# Проверка существования папки с изображениями
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)
    print(f"Создана папка для ассетов: {IMG_DIR}")
    sys.exit()

# Цвета
COLORS = {
    'earth': (74, 45, 38),
    'button': (80, 160, 80),
    'button_hover': (100, 200, 100),
    'button_disabled': (150, 150, 150),
    'text': (255, 255, 255)
}


class AssetLoader:
    def __init__(self):
        self.vegetables = {}
        self.bugs = []
        self.background = None
        self.load_assets()

    def load_png(self, name, size):
        path = os.path.join(IMG_DIR, name)
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Ошибка загрузки {path}: {e}")
            sys.exit()

    def load_assets(self):
        # Загрузка фона
        try:
            bg_path = os.path.join(IMG_DIR, "фончик.png")
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            sys.exit()

        # Загрузка овощей
        self.vegetables = {
            'carrot': self.load_png("морковь.png", (100, 100)),
            'tomato': self.load_png("помидор.png", (100, 100)),
            'cabbage': self.load_png("капуста.png", (100, 100)),
            'potato': self.load_png("картоха.png", (100, 100)),
            'onion': self.load_png("редиска.png", (100, 100))
        }

        # Загрузка жуков
        self.bugs = [
            self.load_png("жук1.PNG", (120, 120)),
            self.load_png("жук2.PNG", (120, 120)),
            self.load_png("жук3.PNG", (120, 120)),
            self.load_png("жук4.PNG", (120, 120)),
            self.load_png("жук5.PNG", (120, 120))
        ]


assets = AssetLoader()


class Vegetable:
    def __init__(self, x, y, veg_type):
        self.x = x
        self.y = y
        self.health = 100
        self.image = assets.vegetables[veg_type]
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        if self.health > 0:
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, (50, 50, 50), (self.rect.centerx - 30, self.rect.top - 25, 60, 5))
            pygame.draw.rect(screen, (0, 200, 0),
                             (self.rect.centerx - 30, self.rect.top - 25, 60 * (self.health / 100), 5))


class Bug:
    def __init__(self, target):

        self.target = target
        self.image = random.choice(assets.bugs)
        self.rect = self.image.get_rect(
            center=(random.choice([-50, WIDTH + 50]),
                    random.choice([-50, HEIGHT + 50]))
        )
        self.speed = 16.75  # Высокая скорость жуков

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.centerx += dx / distance * self.speed
            self.rect.centery += dy / distance * self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class YulaGame:
    def __init__(self):
        self.game_stop = False
        self.vegetables = [
            Vegetable(350, 710, 'carrot'),
            Vegetable(500, 710, 'tomato'),
            Vegetable(650, 710, 'cabbage'),
            Vegetable(800, 710, 'potato'),
            Vegetable(950, 710, 'onion')
        ]
        self.bugs = []
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 50000  # 50 секунд
        self.fertilizer_cooldown = 0
        self.font = pygame.font.Font(None, 24)
        self.fertilizer_btn = pygame.Rect(20, 20, 250, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        for bug in self.bugs[:]:
            if bug.rect.collidepoint(pos):
                self.bugs.remove(bug)
                return

        if self.fertilizer_btn.collidepoint(pos) and self.fertilizer_cooldown <= 0:
            for veg in self.vegetables:
                veg.health = min(100, veg.health + 20)
            self.fertilizer_cooldown = 12000  # 12 секунд

    def draw_interface(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.fertilizer_cooldown > 0:
            btn_color = COLORS['button_disabled']
        else:
            btn_color = COLORS['button_hover' if self.fertilizer_btn.collidepoint(mouse_pos) else 'button']

        pygame.draw.rect(screen, btn_color, self.fertilizer_btn, border_radius=5)

        if self.fertilizer_cooldown > 0:
            cooldown_sec = str(int(self.fertilizer_cooldown / 1000)).zfill(2)
            text = self.font.render(f"Перезарядка: {cooldown_sec}", True, COLORS['text'])
            text_rect = text.get_rect(center=self.fertilizer_btn.center)
            screen.blit(text, text_rect)
        else:
            text = self.font.render("Удобрение (+20)", True, COLORS['text'])
            text_rect = text.get_rect(center=self.fertilizer_btn.center)
            screen.blit(text, text_rect)

        time_left = max(0, self.game_duration - (pygame.time.get_ticks() - self.start_time))
        timer_text = self.font.render(f"Время: {time_left // 1000} сек", True, COLORS['text'])
        screen.blit(timer_text, (WIDTH - 200, 20))

    def game_over(self):
        screen.fill((0, 0, 0))
        texts = [
            "ЖУКИ-БАГИ ПОБЕДИЛИ!",
            "Они уничтожили весь урожай",
            "и стали суперсильными!",
            "Теперь только ты можешь спасти мир!"
        ]

        while not(self.game_stop):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    pygame.quit()
                    self.game_stop = True
                    return True

            screen.fill((0, 0, 0))
            for _ in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                bug_img = random.choice(assets.bugs)
                screen.blit(bug_img, (x - bug_img.get_width() // 2, y - bug_img.get_height() // 2))

            y_pos = HEIGHT // 4
            for text in texts:
                render = self.font.render(text, True, config.Color.WHITE.value)
                screen.blit(render, (WIDTH // 2 - render.get_width() // 2, y_pos))
                y_pos += 40

            pygame.display.flip()
            clock.tick(30)

    def run(self):
        while self.running:
            self.handle_events()

            if pygame.time.get_ticks() - self.start_time > self.game_duration:
                self.running = False
                self.game_over()

            if self.fertilizer_cooldown > 0:
                self.fertilizer_cooldown -= clock.get_time()

            if random.random() < 0.02:
                alive_vegetables = [v for v in self.vegetables if v.health > 0]
                if alive_vegetables:
                    target = random.choice(alive_vegetables)
                    self.bugs.append(Bug(target))

            for bug in self.bugs[:]:
                if bug.target.health <= 0:
                    self.bugs.remove(bug)
                    continue

                bug.update()

                if bug.rect.colliderect(bug.target.rect):
                    bug.target.health -= 1.2
                    # Проверка поражения
                    if all(veg.health <= 0 for veg in self.vegetables):
                        self.running = False
                        self.game_over()
                        return self.game_stop
            screen.blit(assets.background, (0, 0))
            pygame.draw.rect(screen, COLORS['earth'], (0, HEIGHT - 100, WIDTH, 100))

            for veg in self.vegetables:
                veg.draw()

            for bug in self.bugs:
                bug.draw()

            self.draw_interface()
            pygame.display.flip()
            clock.tick(60)