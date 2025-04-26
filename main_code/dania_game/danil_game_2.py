import pygame
import random
import sys
from PIL import Image, ImageSequence  # Для работы с GIF

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Включаем полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Получаем размеры экрана

pygame.display.set_caption("Pixel Tanks")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)  # Цвет неба
BROWN = (139, 69, 19)       # Цвет земли
STONE_GRAY = (128, 128, 128)  # Цвет камней

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 60

# Состояния игры
MENU = 0
PLAYING = 1
GAME_OVER = 2
current_state = MENU

# Переменные для игрока
player_size = int(SCREEN_HEIGHT * 0.2)  # Размер игрока зависит от высоты экрана
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - player_size * 2
player_speed = 10
lanes = [SCREEN_WIDTH // 4 - player_size // 2, SCREEN_WIDTH // 2 - player_size // 2, SCREEN_WIDTH * 3 // 4 - player_size // 2]
current_lane = 1  # Игрок начинает в центральной полосе
kill_count = 0

# Загрузка GIF для игрока
def load_gif_frames(gif_path, size):
    gif = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
        pygame_frame = pygame.transform.scale(pygame_frame, size)  # Масштабируем под нужный размер
        frames.append(pygame_frame)
    return frames

# Укажите путь к вашей GIF-картинке персонажа
player_frames = load_gif_frames(r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\animation_person.gif", (player_size, player_size))
current_player_frame = 0

# Переменные для врагов
enemy_size = player_size
enemy_speed = 3
enemies = []  # Список врагов (каждый враг — это словарь с изображением и позицией)
spawn_timer = 0
spawn_interval = 60  # Каждые 60 кадров появляется новый враг

# Массив с путями к PNG-изображениям врагов
enemy_images_paths = [
    r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\vrag1.PNG",  # Убедитесь, что эти файлы существуют
    r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\vrag2.PNG",
    r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\vrag3.PNG",
    r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\vrag4.PNG",
    r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\vrag5.PNG",
]

# Функция для загрузки изображений врагов
def load_enemy_images(paths, size):
    images = []
    for path in paths:
        image = pygame.image.load(path).convert_alpha()  # Загружаем изображение
        image = pygame.transform.scale(image, size)  # Масштабируем под нужный размер
        images.append(image)
    return images

# Загружаем все изображения врагов
enemy_images = load_enemy_images(enemy_images_paths, (enemy_size, enemy_size))

# Переменные для снарядов
bullet_size = player_size // 3
bullet_speed = 7
bullets = []

# Шрифт для текста
font = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.05))  # Размер шрифта зависит от высоты экрана

# Функция для отрисовки фона
def draw_background():
    # Небо
    pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Земля по бокам дорожек
    pygame.draw.rect(screen, GREEN, (0, 0, SCREEN_WIDTH // 4 - player_size // 2, SCREEN_HEIGHT))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH * 3 // 4 + player_size // 2, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Дорожки
    for i in range(3):  # Три дорожки
        lane_x = lanes[i]
        pygame.draw.rect(screen, WHITE, (lane_x, 0, player_size, SCREEN_HEIGHT))

    # Камни на дорожках
    for i in range(3):
        lane_x = lanes[i]
        for _ in range(10):  # Добавляем случайные камни
            x = lane_x + random.randint(-player_size // 2, player_size // 2)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(5, 15)
            pygame.draw.circle(screen, RED, (x, y), size)

# Функция для отрисовки игрока
def draw_player(x, y):
    global current_player_frame
    screen.blit(player_frames[current_player_frame], (x, y))
    current_player_frame = (current_player_frame + 1) % len(player_frames)  # Переход к следующему кадру

# Функция для отрисовки врагов
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy["image"], (enemy["rect"].x, enemy["rect"].y))

# Функция для отрисовки снарядов
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet)

# Функция для проверки столкновений
def check_collision(rect, targets):
    for target in targets:
        if rect.colliderect(target["rect"]):
            return True, target
    return False, None

# Функция для отрисовки кнопок
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Основной игровой цикл
running = True
score = 0

while running:
    if current_state == MENU:
        # Меню
        screen.fill(SKY_BLUE)
        draw_button("Начать игру", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, WHITE)
        draw_button("Выйти", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Проверка нажатия на кнопку "Начать игру"
                if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and
                        SCREEN_HEIGHT // 2 - 50 <= mouse_y <= SCREEN_HEIGHT // 2):
                    current_state = PLAYING
                # Проверка нажатия на кнопку "Выйти"
                elif (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and
                      SCREEN_HEIGHT // 2 + 20 <= mouse_y <= SCREEN_HEIGHT // 2 + 70):
                    running = False

    elif current_state == PLAYING:
        # Игровой процесс
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Выстрел при нажатии пробела
                bullet_x = player_x + player_size // 2 - bullet_size // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_size, bullet_size))

        keys = pygame.key.get_pressed()

        # Логика переключения между полосами
        if keys[pygame.K_LEFT]:
            if current_lane > 0:
                current_lane -= 1
        elif keys[pygame.K_RIGHT]:
            if current_lane < 2:
                current_lane += 1

        # Обновление позиции игрока
        player_x = lanes[current_lane]

        # Генерация врагов
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            lane = random.randint(0, 2)
            enemy_x = lanes[lane]
            enemy_y = -enemy_size
            # Выбираем случайное изображение для врага
            enemy_image = random.choice(enemy_images)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
            enemies.append({"image": enemy_image, "rect": enemy_rect})
            spawn_timer = 0

        # Обновление позиций врагов
        for enemy in enemies:
            enemy["rect"].y += enemy_speed

        # Удаление врагов, которые вышли за пределы экрана
        enemies = [enemy for enemy in enemies if enemy["rect"].y < SCREEN_HEIGHT]

        # Обновление позиций снарядов
        for bullet in bullets:
            bullet.y -= bullet_speed

        # Удаление снарядов, которые вышли за пределы экрана
        bullets = [bullet for bullet in bullets if bullet.y > -bullet_size]

        # Проверка столкновений снарядов с врагами
        for bullet in bullets[:]:
            hit, enemy = check_collision(bullet, enemies)
            if hit:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                score *= 12
                kill_count += 1

        # Проверка столкновений игрока с врагами
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if check_collision(player_rect, enemies)[0]:
            current_state = GAME_OVER

        # Отрисовка игрока, врагов и снарядов
        draw_player(player_x, player_y)
        draw_enemies(enemies)
        draw_bullets(bullets)

        # Подсчет очков
        score_text = font.render(f"Score: {score}", True, BLACK)
        kill_count_text = font.render(f"Истребленные вирусы: {kill_count}", True, BLACK)
        screen.blit(score_text, (10, 40))
        screen.blit(kill_count_text,(10,10))

    elif current_state == GAME_OVER:
        # Экран конца игры
        screen.fill(SKY_BLUE)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, BLACK)
        kill_count_text = font.render(f"Истребленные вирусы: {kill_count}", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(kill_count_text, (SCREEN_WIDTH // 2 - kill_count_text.get_width() // 2, SCREEN_HEIGHT // 2))

        draw_button("Рестарт", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50, WHITE)
        draw_button("Выйти", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 200, 50, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Проверка нажатия на кнопку "Рестарт"
                if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and
                        SCREEN_HEIGHT // 2 + 70 <= mouse_y <= SCREEN_HEIGHT // 2 + 120):
                    # Сброс игры
                    current_state = PLAYING
                    score = 0
                    enemies = []
                    bullets = []
                    spawn_timer = 0
                    kill_count = 0
                    player_x = lanes[current_lane]
                # Проверка нажатия на кнопку "Выйти"
                elif (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and
                      SCREEN_HEIGHT // 2 + 140 <= mouse_y <= SCREEN_HEIGHT // 2 + 190):
                    running = False

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

# Завершение игры
pygame.quit()
sys.exit()