import pygame
import sys
import subprocess

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Портал в Ошибку")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Игрок
player = pygame.Rect(400, 500, 40, 60)
player_speed = 5
jump_power = -15
gravity = 0.8
velocity_y = 0

# Платформы
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(200, 450, 100, 20),
    pygame.Rect(400, 350, 100, 20),
    pygame.Rect(100, 250, 100, 20),
]

# Портал
portal = pygame.Rect(700, 200, 50, 50)

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.bottom >= 550:
                velocity_y = jump_power

    # Движение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Гравитация
    velocity_y += gravity
    player.y += velocity_y

    # Коллизии с платформами
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # Попадание в портал
    if player.colliderect(portal):
        pygame.quit()
        subprocess.Popen(["python", "error_game.py"])  # Запуск игры с ошибками
        sys.exit()

    # Отрисовка
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.ellipse(screen, PURPLE, portal)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()