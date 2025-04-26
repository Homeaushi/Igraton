import pygame
import sys
import random
import math
import os

# Инициализация PyGame
pygame.init()
WIDTH, HEIGHT = 800, 600
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
    'sky': (135, 206, 235),
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
        self.load_assets()

    def load_png(self, name, size):
        """Загрузка PNG с обработкой ошибок"""
        path = os.path.join(IMG_DIR, name)
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Ошибка загрузки {path}: {e}")
            sys.exit()

    def load_assets(self):
        # Загрузка овощей
        self.vegetables = {
            'carrot': self.load_png("морковь.png", (60, 60)),
            'tomato': self.load_png("помидор.png", (60, 60)),
            'cabbage': self.load_png("капуста.png", (60, 60)),
            'potato': self.load_png("картоха.png", (60, 60)),
            'onion': self.load_png("редиска.png", (60, 60))
        }

        # Загрузка жуков с увеличенной скоростью
        self.bugs = [
            self.load_png("жук1.PNG", (50, 50)),
            self.load_png("жук2.PNG", (50, 50)),
            self.load_png("жук3.PNG", (50, 50)),
            self.load_png("жук4.PNG", (50, 50)),
            self.load_png("жук5.PNG", (50, 50))
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
            # Полоска здоровья
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
        self.speed = 1.725  # Увеличенная скорость на 15%

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.centerx += dx / distance * self.speed
            self.rect.centery += dy / distance * self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.vegetables = [
            Vegetable(150, 450, 'carrot'),
            Vegetable(300, 450, 'tomato'),
            Vegetable(450, 450, 'cabbage'),
            Vegetable(600, 450, 'potato'),
            Vegetable(750, 450, 'onion')
        ]
        self.bugs = []
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 50000  # 50 секунд
        self.fertilizer_cooldown = 0
        self.font = pygame.font.Font(None, 36)
        self.fertilizer_btn = pygame.Rect(20, 20, 180, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        # Уничтожение жуков
        for bug in self.bugs[:]:
            if bug.rect.collidepoint(pos):
                self.bugs.remove(bug)
                return

        # Активация удобрения
        if self.fertilizer_btn.collidepoint(pos) and self.fertilizer_cooldown <= 0:
            for veg in self.vegetables:
                veg.health = min(100, veg.health + 20)
            self.fertilizer_cooldown = 7000  # 7 секунд перезарядки

    def draw_interface(self):
        # Кнопка удобрения
        mouse_pos = pygame.mouse.get_pos()
        if self.fertilizer_cooldown > 0:
            btn_color = COLORS['button_disabled']
        else:
            btn_color = COLORS['button_hover' if self.fertilizer_btn.collidepoint(mouse_pos) else 'button']

        pygame.draw.rect(screen, btn_color, self.fertilizer_btn, border_radius=5)

        # Текст кнопки
        if self.fertilizer_cooldown > 0:
            cooldown_sec = str(int(self.fertilizer_cooldown / 1000)).zfill(2)
            text = self.font.render(f"Перезарядка: {cooldown_sec}", True, COLORS['text'])
        else:
            text = self.font.render("Удобрение (+20)", True, COLORS['text'])
        screen.blit(text, (self.fertilizer_btn.x + 10, self.fertilizer_btn.y + 5))

        # Таймер игры
        time_left = max(0, self.game_duration - (pygame.time.get_ticks() - self.start_time))
        timer_text = self.font.render(f"Время: {time_left // 1000} сек", True, COLORS['text'])
        screen.blit(timer_text, (WIDTH - 200, 20))

    def game_over(self):
        screen.fill((0, 0, 0))
        texts = [
            "ЖУКИ-БАГИ ПОБЕДИЛИ!",
            "Они уничтожили весь урожай",
            "и стали суперсильными!",
            "Теперь только ты можешь спасти мир!",
            "Нажмите ЛКМ для выхода"
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    pygame.quit()
                    sys.exit()

            # Анимация жуков
            screen.fill((0, 0, 0))
            for _ in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                bug_img = random.choice(assets.bugs)
                screen.blit(bug_img, (x - bug_img.get_width() // 2, y - bug_img.get_height() // 2))

            # Текст поражения
            y_pos = HEIGHT // 4
            for text in texts:
                render = self.font.render(text, True, (200, 0, 0))
                screen.blit(render, (WIDTH // 2 - render.get_width() // 2, y_pos))
                y_pos += 40

            pygame.display.flip()
            clock.tick(30)

    def run(self):
        while self.running:
            self.handle_events()

            # Проверка времени игры
            if pygame.time.get_ticks() - self.start_time > self.game_duration:
                self.running = False
                self.game_over()

            # Обновление перезарядки удобрений
            if self.fertilizer_cooldown > 0:
                self.fertilizer_cooldown -= clock.get_time()

            # Спавн новых жуков
            if random.random() < 0.02:
                alive_vegetables = [v for v in self.vegetables if v.health > 0]
                if alive_vegetables:
                    target = random.choice(alive_vegetables)
                    self.bugs.append(Bug(target))

            # Обновление жуков
            for bug in self.bugs[:]:
                if bug.target.health <= 0:
                    self.bugs.remove(bug)
                    continue

                bug.update()

                # Проверка атаки
                if bug.rect.colliderect(bug.target.rect):
                    bug.target.health -= 1

            # Проверка поражения
            if all(veg.health <= 0 for veg in self.vegetables):
                self.running = False
                self.game_over()

            # Отрисовка
            screen.fill(COLORS['sky'])
            pygame.draw.rect(screen, COLORS['earth'], (0, HEIGHT - 100, WIDTH, 100))

            # Отрисовка овощей
            for veg in self.vegetables:
                veg.draw()

            # Отрисовка жуков
            for bug in self.bugs:
                bug.draw()

            # Отрисовка интерфейса
            self.draw_interface()

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    Game().run()