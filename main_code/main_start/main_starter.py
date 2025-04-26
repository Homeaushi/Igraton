import pygame
import sys
import os
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Визуальная новелла")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Шрифты
font = pygame.font.Font(None, 32)
character_font = pygame.font.Font(None, 28)

# Загрузка изображений из папки 'images'
images = []
image_folder = "images"

if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    print(f"Папка '{image_folder}' создана. Добавьте туда фоновые изображения в формате JPG/PNG.")

# Проверяем, есть ли файлы в папке
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

if not image_files:
    print(f"В папке '{image_folder}' нет изображений. Добавьте JPG/PNG файлы.")
    # Создаем заглушку - черный экран
    placeholder = pygame.Surface((WIDTH, HEIGHT))
    placeholder.fill(BLACK)
    images.append(placeholder)
else:
    for img_file in image_files:
        try:
            img_path = os.path.join(image_folder, img_file)
            img = pygame.image.load(img_path).convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            images.append(img)
            print(f"Загружено изображение: {img_file}")
        except pygame.error as e:
            print(f"Ошибка загрузки {img_file}: {e}")
            placeholder = pygame.Surface((WIDTH, HEIGHT))
            placeholder.fill(BLACK)
            images.append(placeholder)

# Если нет изображений, добавляем одно черное
if not images:
    placeholder = pygame.Surface((WIDTH, HEIGHT))
    placeholder.fill(BLACK)
    images.append(placeholder)

# Тексты для каждого экрана (можно расширить)
scenes = [
    {
        "image": 0 % len(images),  # Используем модуль, чтобы не выйти за границы массива
        "character": "Персонаж 1",
        "text": "Привет! Это первое сообщение в нашей визуальной новелле."
    },
    {
        "image": 1 % len(images),
        "character": "Персонаж 2",
        "text": "Второе сообщение с другим персонажем. Текст появляется постепенно!"
    },
    {
        "image": 2 % len(images),
        "character": "Система",
        "text": "Третья сцена. Кликните, чтобы продолжить или выйти."
    }
]

# Настройки текстового окна
text_box_height = 150
text_box = pygame.Rect(50, HEIGHT - text_box_height - 20, WIDTH - 100, text_box_height)
character_box = pygame.Rect(60, HEIGHT - text_box_height - 10, 200, 30)

# Переменные игры
current_scene = 0
current_char = 0
display_text = ""
typing_speed = 30  # символов в секунду
typing_delay = 1000 // typing_speed
last_typing_time = 0
waiting