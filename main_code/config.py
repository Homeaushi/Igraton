import enum

import pygame


class Color(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    CACHE = (0, 100, 255)
    GOLD = (255, 215, 0)
    PURPLE = (128, 0, 128)
    PLATFORM = (100, 100, 100)

class ScreenSize(enum.Enum):
    WIDTH, HEIGHT = (pygame.display.set_mode((0, 0), pygame.FULLSCREEN)).get_size()