import pygame
from color import Color
from main_code.guk_game.screen_size import Screen_size


def load_image(path, size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение {path}: {e}")
        # Создаем заглушку
        surface = pygame.Surface((100, 500), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0) if "Враг" in path else (0, 0, 255), (0, 0, 100, 500))
        return surface

class Fighter:
    def __init__(self, x, y, color, controls, image_path):
        self.rect = pygame.Rect(x, y, 100, 500)
        self.color = color
        self.speed = 5
        self.health = 100
        self.controls = controls
        self.attacking_up = False
        self.attacking_down = False
        self.attack_cooldown = 0
        self.facing_right = color == Color.BLUE.value  # Синий смотрит вправо, красный - влево

        # Загрузка изображения персонажа
        self.image = load_image(image_path, (300, 500))
        self.flipped_image = pygame.transform.flip(self.image, True, False)

    def move(self, keys, other_player):
        if keys[self.controls["left"]]:
            self.rect.x -= self.speed
            if self.rect.colliderect(other_player.rect):
                self.facing_right = False
        if keys[self.controls["right"]]:
            self.rect.x += self.speed
            if self.rect.colliderect(other_player.rect):
                self.facing_right = True

        if self.rect.colliderect(other_player.rect):
            if self.rect.centerx < other_player.rect.centerx:
                self.facing_right = True
            else:
                self.facing_right = False

    def attack_up(self):
        if self.attack_cooldown == 0:
            self.attacking_up = True
            self.attack_cooldown = 20

    def attack_down(self):
        if self.attack_cooldown == 0:
            self.attacking_down = True
            self.attack_cooldown = 20

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 2
        else:
            self.attacking_up = False
            self.attacking_down = False

        self.rect.x = max(0, min(Screen_size.WIDTH.value - self.rect.width, self.rect.x))

    def draw(self, surface):
        # Отрисовка персонажа
        if self.facing_right:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.flipped_image, (self.rect.x, self.rect.y))

        # Полоска здоровья
        pygame.draw.rect(surface, Color.RED.value, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(surface, Color.GREEN.value, (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))

        attack_rect = None

        # Верхняя атака
        if self.attacking_up:
            if self.facing_right:
                attack_rect = pygame.Rect(
                    self.rect.x + self.rect.width,
                    self.rect.y + 20,
                    100,
                    20
                )
            else:
                attack_rect = pygame.Rect(
                    self.rect.x - 100,
                    self.rect.y + 20,
                    100,
                    20
                )
            pygame.draw.rect(surface, Color.WHITE.value, attack_rect)

        # Нижняя атака
        elif self.attacking_down:
            if self.facing_right:
                attack_rect = pygame.Rect(
                    self.rect.x + self.rect.width,
                    self.rect.y + self.rect.height - 40,
                    100,
                    40
                )
            else:
                attack_rect = pygame.Rect(
                    self.rect.x - 100,
                    self.rect.y + self.rect.height - 40,
                    100,
                    40
                )
            pygame.draw.rect(surface, (255, 255, 0), attack_rect)

        return attack_rect
