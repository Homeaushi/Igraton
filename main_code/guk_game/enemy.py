import pygame
import random
from character import CharacterBase
from projectile import Projectile


class Enemy(CharacterBase):
    """Класс врага с ИИ управлением"""

    def __init__(self, x, y, color, controls=None, image_path=None):
        super().__init__(x, y, color, {}, image_path)  # Убираем controls, так как ИИ не нужны клавиши
        self.attacking_up = False
        self.projectiles = []
        self.special_attack_cooldown = 0
        self.ai_timer = 0
        self.ai_decision_delay = 30  # Частота принятия решений (в кадрах)
        self.aggression = 0.5  # Агрессивность ИИ (0-1)
        self.attack_range = 1300  # Дистанция для атаки

    def make_decision(self, player):
        """Принимает решение на основе положения игрока"""
        distance = abs(self.rect.centerx - player.rect.centerx)

        # Движение к игроку
        if distance > self.attack_range * 0.8:
            if self.rect.centerx < player.rect.centerx:
                self.move_right = True
                self.move_left = False
                self.facing_right = True
            else:
                self.move_right = False
                self.move_left = True
                self.facing_right = False
        else:
            self.move_left = False
            self.move_right = False

            # Случайное движение для создания "живого" поведения
            if random.random() < 0.05:
                self.move_left = random.choice([True, False])
                self.move_right = not self.move_left
                self.facing_right = self.move_right

        # Атака с некоторой вероятностью
        if distance < self.attack_range and random.random() < self.aggression:
            if random.random() < 0.7:  # 70% chance для специальной атаки
                self.attack_up()

    def attack_up(self):
        if self.attack_cooldown == 0:
            self.attacking_up = True
            self.attack_cooldown = 20
            self.special_attack_cooldown = 60
            # Запуск снаряда
            x = self.rect.right if self.facing_right else self.rect.left - 30
            self.projectiles.append(Projectile(x, self.rect.centery, 1 if self.facing_right else -1))

    def update(self, player=None):
        """Обновление состояния с учетом игрока"""
        super().update()

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1

        # Обновление снарядов
        for proj in self.projectiles[:]:
            proj._update()
            if not proj.active:
                self.projectiles.remove(proj)

        # Принятие решений ИИ
        if player:  # Проверяем, передан ли игрок
            self.ai_timer += 1
            if self.ai_timer >= self.ai_decision_delay:
                self.ai_timer = 0
                self.make_decision(player)

    def get_current_image(self):
        """Переопределяем для отображения специальной атаки"""
        if self.special_attack_cooldown > 0:
            return self.attack_up_flipped if not self.facing_right else self.attack_up_image
        return super().get_current_image()

    def draw(self, surface):
        """Отрисовка врага и его снарядов"""
        surface.blit(self.get_current_image(), (self.rect.x, self.rect.y))
        self.draw_health_bar(surface)

        for proj in self.projectiles:
            proj.draw(surface)

        # Возвращаем хитбокс атаки
        attack_rect = None
        if self.attacking_up or self.special_attack_cooldown > 0:
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.y + 20, 100, 20)
            else:
                attack_rect = pygame.Rect(self.rect.left - 100, self.rect.y + 20, 100, 20)

        return attack_rect