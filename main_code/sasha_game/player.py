import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Загружаем оригинальную картинку
        original_image = pygame.image.load(r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\guk_Images\Персонаж.PNG").convert_alpha()
        
        # Размер персонажа (изменяй под себя)
        size = (50, 50)

        # Здоровье персонажа
        self.max_health = 100
        self.current_health = self.max_health
        self.is_dead = False

        # Уменьшаем картинку
        scaled_image = pygame.transform.scale(original_image, size)

        self.images = {
            "normal": scaled_image,
            "double_jump": scaled_image,
            "buffed": scaled_image
        }
        self.current_image = self.images["normal"]
        self.image = self.current_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_right = True

        # Физика
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.velocity_y = 0
        self.on_ground = True

        # Горизонтальная скорость
        self.velocity_x = 0

        # Система прыжков
        self.has_double_jump = False
        self.jumps_used = 0
        self.max_air_jumps = 1

    def update(self, platforms, hazards=None):
        self.handle_input()

    # Горизонтальное движение
        self.rect.x += self.velocity_x
        self.flip_sprite()
        self.check_collisions_x(platforms)

    # Вертикальное движение
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.check_collisions_y(platforms)

    # Сброс прыжков при приземлении
        if self.on_ground:
            self.jumps_used = 0
            self.image = self.images["normal"]  # Вернуть обычную картинку

    # Проверка смерти
        if self.current_health <= 0 or self.rect.top > 1000:
            self.is_dead = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_right = True

    def jump(self):
        if self.on_ground:
            self.execute_jump("Основной прыжок")
        elif self.has_double_jump and self.jumps_used < self.max_air_jumps + 1:
            self.execute_jump("Двойной прыжок!", "double_jump")

    def execute_jump(self, jump_type, img_key=None):
        self.velocity_y = self.jump_power
        self.on_ground = False
        self.jumps_used += 1
        if img_key:
            self.current_image = self.images[img_key]
            self.flip_sprite()
        print(jump_type)

    def check_collisions_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

    def check_collisions_y(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def flip_sprite(self):
        if self.facing_right:
            self.image = self.current_image
        else:
            self.image = pygame.transform.flip(self.current_image, True, False)

    def apply_buff(self, buff_type):
        if buff_type == "double_jump":
            self.has_double_jump = True
            self.current_state = "buffed"
        elif buff_type == "cache":
            self.speed += 3
        elif buff_type == "multithreading":
            pass

        self.flip_sprite()

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
