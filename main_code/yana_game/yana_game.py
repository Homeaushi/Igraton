import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Беги от ошибок!")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройки игры
FPS = 60
gravity = 0.5
player_speed = 5
platform_speed = 3

# Загрузка изображений
player_img = pygame.image.load(r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\guk_Images\Персонаж.PNG")  # Замените на свой файл изображения игрока

# Масштабирование изображений
player_img = pygame.transform.scale(player_img, (70, 70))

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 100)
        self.velocity_y = 0
        self.on_ground = False
        self.velocity_x = 0  # Горизонтальная скорость

    def update(self, platforms):
        # Горизонтальное движение
        self.rect.x += self.velocity_x

        # Гравитация
        self.velocity_y += gravity
        self.rect.y += self.velocity_y

        # Проверка столкновений с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:  # Касание платформы сверху
                if self.rect.bottom <= platform.rect.bottom:  # Убедимся, что игрок сверху
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Проверка на падение ниже экрана
        if self.rect.top > HEIGHT:  # Если игрок полностью выходит за нижнюю границу экрана
            print("Вы упали!")
            return True  # Возвращаем флаг проигрыша

        return False  # Игра продолжается

    def jump(self):
        if self.on_ground:
            self.velocity_y = -15

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Создание начальных платформ
def create_platforms():
    platforms = [
        Platform(0, HEIGHT - 20, WIDTH, 20),  # Нижняя платформа (постоянная)
        Platform(200, random.randint(HEIGHT - 300, HEIGHT - 50), random.randint(100, 200), 20),
        Platform(400, random.randint(HEIGHT - 300, HEIGHT - 50), random.randint(100, 200), 20),
        Platform(600, random.randint(HEIGHT - 300, HEIGHT - 50), random.randint(100, 200), 20),
    ]
    return platforms

platforms_list = create_platforms()
for platform in platforms_list:
    platforms.add(platform)
    all_sprites.add(platform)

# Таймер для создания новых элементов
error_timer = 0

# Уровень длится ровно минуту
start_time = pygame.time.get_ticks()
level_duration = 40000  # 40 секунд в миллисекундах

# Класс портала
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 100))  # Размеры портала
        self.image.fill(BLUE)  # Цвет портала (можно заменить на изображение)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Группа спрайтов для портала
portal_group = pygame.sprite.Group()

# Флаг для отображения портала
portal_spawned = False

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Обработка нажатия клавиш для горизонтального движения
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.velocity_x = -5
    elif keys[pygame.K_RIGHT]:
        player.velocity_x = 5
    else:
        player.velocity_x = 0

    # Текущее время
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, level_duration - elapsed_time)

    # Проверка на окончание уровня
    if elapsed_time >= level_duration and not portal_spawned:
        print("Уровень завершен! Ищите портал!")
        # Создаем портал в случайном месте справа от экрана
        portal = Portal(WIDTH - 50, random.randint(HEIGHT - 300, HEIGHT - 150))
        portal_group.add(portal)
        all_sprites.add(portal)
        portal_spawned = True

    # Обновление игрока
    game_over = player.update(platforms)
    if game_over:  # Если игрок упал
        print("Игра окончена! Вы упали.")
        running = False

    # Движение платформы влево
    for platform in platforms:
        platform.rect.x -= platform_speed
        if platform.rect.right < 0:
            platform.kill()

    # Создание новых платформ
    if len(platforms) < 5:
        new_platform = Platform(
            WIDTH,
            random.randint(HEIGHT - 300, HEIGHT - 20),  # Расширенный диапазон высот
            random.randint(100, 200),
            20
        )
        platforms.add(new_platform)
        all_sprites.add(new_platform)

    # Проверка столкновения игрока с порталом
    if portal_spawned:
        if pygame.sprite.spritecollide(player, portal_group, False):
            print("Вы вошли в портал! Переход на следующую локацию...")
            # Здесь можно добавить переход на следующий уровень или завершение игры
            running = False

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Отображение счета
    font = pygame.font.Font(None, 36)

    # Отображение таймера
    time_text = font.render(f"Time: {remaining_time // 1000}", True, BLACK)
    screen.blit(time_text, (WIDTH - 150, 10))

    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()
