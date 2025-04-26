import pygame

BUFF_COLORS = {
    "cache": (0, 100, 255),          # Синий - скорость
    "double_jump": (255, 215, 0),     # Золотой - двойной прыжок
    "multithreading": (128, 0, 128)   # Фиолетовый
}

class Buff(pygame.sprite.Sprite):
    def __init__(self, x, y, buff_type):
        super().__init__()
        self.type = buff_type
        
        # Защита от неизвестного баффа
        color = BUFF_COLORS.get(buff_type, (255, 0, 0))  # Если нет такого баффа, сделать красный квадрат
        
        self.image = pygame.Surface((24, 24))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
