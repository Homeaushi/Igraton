import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Цвет платформы
        self.rect = self.image.get_rect(topleft=(x, y))

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, move_range, speed, axis):
        super().__init__(x, y, width, height)
        self.move_range = move_range
        self.speed = speed
        self.axis = axis  # Направление движения: "x" или "y"
        self.initial_pos = (x, y)
        self.current_pos = (x, y)
        self.direction = 1  # 1 - вправо/вниз, -1 - влево/вверх

    def update(self):
        if self.axis == "x":
            self.current_pos = (self.current_pos[0] + self.speed * self.direction, self.current_pos[1])
        elif self.axis == "y":
            self.current_pos = (self.current_pos[0], self.current_pos[1] + self.speed * self.direction)
    
    # Проверка на пределы движения
        if self.axis == "x" and abs(self.current_pos[0] - self.initial_pos[0]) >= self.move_range:
            self.direction *= -1
        elif self.axis == "y" and abs(self.current_pos[1] - self.initial_pos[1]) >= self.move_range:
            self.direction *= -1
    
        self.rect.topleft = self.current_pos
    
    # Добавь вывод в консоль для проверки
        print(f"Moving Platform at {self.rect.topleft}")  # Это покажет позицию платформы