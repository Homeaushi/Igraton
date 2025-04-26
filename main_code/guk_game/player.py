import pygame
from character import CharacterBase


class Player(CharacterBase):
    """Класс игрока"""

    def __init__(self, x, y, color, controls, image_path):
        super().__init__(x, y, color, controls, image_path)
        self.attacking_up = False
        self.attacking_down = False

    def attack_up(self):
        if self.attack_cooldown == 0:
            self.attacking_up = True
            self.attack_cooldown = 20

    def attack_down(self):
        if self.attack_cooldown == 0:
            self.attacking_down = True
            self.attack_cooldown = 20

    def draw(self, surface):
        """Отрисовка игрока"""
        surface.blit(self.get_current_image(), (self.rect.x, self.rect.y))
        self.draw_health_bar(surface)

        # Возвращаем хитбокс атаки
        attack_rect = None
        if self.attacking_up or self.attacking_down:
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.y + 20, 100, 20)
            else:
                attack_rect = pygame.Rect(self.rect.left - 100, self.rect.y + 20, 100, 20)

        return attack_rect

    def move(self, keys, other_player):
        """Общая логика движения для всех персонажей"""
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
