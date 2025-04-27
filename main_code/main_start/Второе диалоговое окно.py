import pygame
from PIL import Image, ImageSequence
import sys
import os

# Инициализация Pygame
pygame.init()

# Полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Визуальная новелла с анимированным GIF")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50, 200)  # С альфа-каналом для прозрачности

# Шрифты (адаптивные к размеру экрана)
try:
    font_size = HEIGHT // 20
    font = pygame.font.Font(None, font_size)
    character_font = pygame.font.Font(None, int(font_size * 0.9))
except:
    font = pygame.font.SysFont('arial', HEIGHT // 20)
    character_font = pygame.font.SysFont('arial', int(HEIGHT // 20 * 0.9))

# Загрузка GIF
def load_gif_frames(gif_path):
    frames = []
    try:
        with Image.open(gif_path) as gif:
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                frame_data = frame.tobytes()
                size = frame.size
                pygame_frame = pygame.image.fromstring(frame_data, size, "RGBA")
                pygame_frame = pygame.transform.scale(pygame_frame, (WIDTH, HEIGHT))
                frames.append(pygame_frame)
    except Exception as e:
        print(f"Ошибка загрузки GIF: {e}")
        placeholder = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        placeholder.fill(BLACK)
        frames.append(placeholder)
    return frames

# Проверка существования файла GIF
gif_path = r"C:\Users\danil\PycharmProjects\Igraton\main_code\main_start\frames\gge30af3a644.gif"
if not os.path.exists(gif_path):
    print(f"Файл GIF не найден: {gif_path}")
    frames = [pygame.Surface((WIDTH, HEIGHT))]
    frames[0].fill(BLACK)
else:
    frames = load_gif_frames(gif_path)

# Настройки анимации
FPS = 10
frame_delay = 1000 // FPS
last_frame_time = 0
current_frame = 0

# Текстовые сцены
scenes = [
    {"character": "Акакаий", "text": "Вау, да, ты хорош!"},
    {"character": "Акакий", "text": "Помоги мне спасти уничтожить жуков-багов до конца..."},
    {"character": "Акакий", "text": "И мы снова будем жить в комфорте"},
    {"character": "ЖУКИ-БАГИ", "text": "АХАХАХАХ, наивные)))))"},
    {"character": "Акакий", "text": "Будь аккуратен, это зло снесло все текстуры!!"},
    {"character": "", "text": "Нажмите, чтобы продолжить >:)"}
]

# Настройки текстового окна (адаптивные)
text_box_height = HEIGHT // 4
text_box = pygame.Rect(WIDTH//20, HEIGHT - text_box_height - HEIGHT//20,
                      WIDTH - WIDTH//10, text_box_height)
character_box = pygame.Rect(WIDTH//20 + 10, HEIGHT - text_box_height - HEIGHT//20 - 10,
                          WIDTH//4, HEIGHT//20)

# Переменные игры
current_scene = 0
current_char = 0
display_text = ""
typing_speed = 30  # символов в секунду
typing_delay = 1000 // typing_speed
last_typing_time = 0
waiting_for_click = False

# Задержка между нажатиями
last_click_time = 0
click_delay = 300  # Задержка в миллисекундах

# Главный игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if current_time - last_click_time > click_delay:
                if waiting_for_click:
                    current_scene = (current_scene + 1) % len(scenes)
                    current_char = 0
                    display_text = ""
                    waiting_for_click = False
                else:
                    display_text = scenes[current_scene]["text"]
                    waiting_for_click = True
                last_click_time = current_time

    # Анимация фона
    if current_time - last_frame_time > frame_delay:
        current_frame = (current_frame + 1) % len(frames)
        last_frame_time = current_time

    # Посимвольный вывод текста
    if not waiting_for_click and current_time - last_typing_time > typing_delay:
        if current_char < len(scenes[current_scene]["text"]):
            display_text += scenes[current_scene]["text"][current_char]
            current_char += 1
            last_typing_time = current_time
        else:
            waiting_for_click = True

    # Отрисовка
    # Анимированный фон
    screen.blit(frames[current_frame], (0, 0))

    # Полупрозрачное текстовое окно
    s = pygame.Surface((text_box.width, text_box.height), pygame.SRCALPHA)
    s.fill((*GRAY[:3], 200))  # Устанавливаем прозрачность
    screen.blit(s, text_box)
    pygame.draw.rect(screen, (70, 70, 70), text_box, 2, border_radius=10)

    # Имя персонажа
    if scenes[current_scene]["character"]:
        pygame.draw.rect(screen, (100, 100, 100, 200), character_box, border_radius=5)
        character_name = character_font.render(scenes[current_scene]["character"], True, WHITE)
        screen.blit(character_name, (character_box.x + 10, character_box.y + 5))

    # Текст с переносом (максимум 3 строки)
    wrapped_text = []
    words = display_text.split(' ')
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < text_box.width - 40:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word + ' '
    wrapped_text.append(line)

    # Ограничение до 3 строк с многоточием
    if len(wrapped_text) > 3:
        wrapped_text = wrapped_text[:3]
        wrapped_text[-1] = wrapped_text[-1].rstrip() + "..."  # Добавляем многоточие

    for i, line in enumerate(wrapped_text[:3]):  # Ограничение 3 строк
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (text_box.x + 20, text_box.y + 20 + i * (HEIGHT//20)))

    # Индикатор клика
    if waiting_for_click:
        click_indicator = font.render("▶", True, WHITE)
        screen.blit(click_indicator, (text_box.right - 40, text_box.bottom - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()