import pygame
from main_code.config import ScreenSize


class Projectile:
    def __init__(self, x, y, direction, speed=10):
        self.rect = pygame.Rect(x, y, 30, 20)
        self.direction = direction  # 1 для вправо, -1 для влево
        self.speed = speed
        self.active = True

        # Загрузка изображения снаряда
        try:
            self.image = pygame.image.load(
                r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\guk_Images\Слюня.png"
            ).convert_alpha()
            self.image = pygame.transform.scale(self.image,(200, 200))

            # Отражаем изображение если летит влево
            if direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        except pygame.error as e:
            print(f"Не удалось загрузить изображение снаряда: {e}")
            # Создаем заглушку если изображение не загрузилось
            self.image = pygame.Surface((30, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 200, 0), (15, 10), 10)

    def _update(self):
        self.rect.x += self.speed * self.direction
        # Деактивировать если улетел за экран
        if self.rect.right < 0 or self.rect.left > ScreenSize.WIDTH.value:
            self.active = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)