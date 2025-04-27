import pygame
import json
from main_code.sasha_game.buffs import Buff
from main_code.sasha_game.hazards import Hazard  # Для шипов
from main_code.sasha_game.platforms import Platform, MovingPlatform  # Для платформ

class Level:
    def __init__(self, map_file):
        with open(map_file) as f:
            self.map_data = json.load(f)
        
        self.level_width = 2000  # Общая ширина уровня
        self.level_height = 1000  # Общая высота
        
        self.platforms = self._create_objects("platforms")
        self.buffs = self._create_objects("buffs")
        self.hazards = self._create_objects("hazards")

    def _create_objects(self, obj_type):
        group = pygame.sprite.Group()
        for obj in self.map_data[obj_type]:
            if obj_type == "buffs":
                group.add(Buff(obj["x"], obj["y"], obj["type"]))
            elif obj_type == "platforms":
                if "type" in obj and obj["type"] == "moving":
                    platform = MovingPlatform(obj["x"], obj["y"], obj["width"], obj["height"], obj["range"], obj["speed"], obj["axis"])
                else:
                    platform = Platform(obj["x"], obj["y"], obj["width"], obj["height"])
                group.add(platform)
            elif obj_type == "hazards":
                hazard = Hazard(obj["x"], obj["y"], obj["width"], obj["height"], obj["type"])
                group.add(hazard)
        return group
