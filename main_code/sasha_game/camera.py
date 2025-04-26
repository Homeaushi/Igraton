import pygame

class Camera:
    def __init__(self, width, height, level_width, level_height):
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.level_width = level_width
        self.level_height = level_height

    def apply(self, entity):
        """Сдвигает спрайт относительно камеры"""
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        """Центрирует камеру на игроке с ограничениями"""
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)
        
        # Ограничения (не выходим за границы уровня)
        x = min(0, x)  # Левый край
        y = min(0, y)  # Верхний край
        x = max(-(self.level_width - self.width), x)  # Правый край
        y = max(-(self.level_height - self.height), y)  # Нижний край
        
        self.camera_rect = pygame.Rect(x, y, self.width, self.height)