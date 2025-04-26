import pygame
from main_code.config import Color,ScreenSize


class CharacterBase:
    """Базовый класс для персонажей"""

    def __init__(self, x, y, color, controls, image_path):
        self.rect = pygame.Rect(x, y, 200, 500)
        self.color = color
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.controls = controls
        self.facing_right = color == Color.BLUE.value
        self.attack_cooldown = 0

        # Загрузка изображений
        self.load_character_images(image_path)

    def load_character_images(self, base_path):
        """Загружает все изображения для персонажа"""
        base_path = base_path.replace('.PNG', '').replace('.png', '')

        # Основные изображения
        self.idle_image = self.load_image(f"{base_path}.png", (300, 500))
        self.idle_flipped = pygame.transform.flip(self.idle_image, True, False)

        # Анимации атак
        self.attack_up_image = self.load_image(f"{base_path}_верхний_удар.png", (300, 500))
        self.attack_up_flipped = pygame.transform.flip(self.attack_up_image, True, False)

        self.attack_down_image = self.load_image(f"{base_path}_нижний_удар.png", (300, 500))
        self.attack_down_flipped = pygame.transform.flip(self.attack_down_image, True, False)

    def load_image(self, path, size):
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
        except:
            surface = pygame.Surface(size, pygame.SRCALPHA)
            color = Color.RED.value if "Враг" in path else Color.BLUE.value
            pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
            return surface

    def get_current_image(self):
        """Определяет текущее изображение персонажа"""
        if self.attacking_up:
            return self.attack_up_flipped if not self.facing_right else self.attack_up_image
        elif self.attacking_down:
            return self.attack_down_flipped if not self.facing_right else self.attack_down_image
        else:
            return self.idle_flipped if not self.facing_right else self.idle_image


    def update(self):
        """Обновление состояния персонажа"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking_up = False
            self.attacking_down = False

        self.rect.x = max(0, min(ScreenSize.WIDTH.value - self.rect.width, self.rect.x))

    def draw_health_bar(self, surface):
        """Отрисовка полоски здоровья"""
        health_width = int(self.rect.width * (self.health / self.max_health))
        pygame.draw.rect(surface, Color.RED.value,
                         (self.rect.x, self.rect.y - 20, self.rect.width, 10))
        pygame.draw.rect(surface, Color.GREEN.value,
                         (self.rect.x, self.rect.y - 20, health_width, 10))
