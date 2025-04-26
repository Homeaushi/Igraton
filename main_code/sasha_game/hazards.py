import pygame

from main_code.config import Color


class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hazard_type):
        super().__init__()
        self.type = hazard_type
        self.image = pygame.Surface((width, height))
        self.image.fill(Color.RED.value)  # Красный цвет для шипов
        self.rect = self.image.get_rect(topleft=(x, y))
