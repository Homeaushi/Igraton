import pygame
from PIL import Image, ImageSequence
import os
from pathlib import Path

from main_code.config import ScreenSize


class Scene_1:
    def __init__(self):
        self.screen = pygame.display.set_mode((ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
        self.WIDTH, self.HEIGHT = (ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value)
        self.setup_colors()
        self.setup_fonts()
        self.load_gif()
        self.setup_scenes()
        self.setup_text_boxes()
        self.reset_scene_state()
        self.running = True

    def setup_colors(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50, 200)

    def setup_fonts(self):
        try:
            font_size = self.HEIGHT // 20
            self.font = pygame.font.Font(None, font_size)
            self.character_font = pygame.font.Font(None, int(font_size * 0.9))
        except:
            self.font = pygame.font.SysFont('arial', self.HEIGHT // 20)
            self.character_font = pygame.font.SysFont('arial', int(self.HEIGHT // 20 * 0.9))

    def load_gif(self):
        # Получаем путь относительно расположения скрипта
        script_dir = Path(__file__).parent.parent.parent
        gif_path = script_dir / "main_code" / "main_start" / "frames" / "gge30af3a644.gif"

        if not os.path.exists(gif_path):
            print(f"Файл GIF не найден: {gif_path}")
            self.frames = [pygame.Surface((self.WIDTH, self.HEIGHT))]
            self.frames[0].fill(self.BLACK)
        else:
            self.frames = self.load_gif_frames(gif_path)

        self.FPS = 10
        self.frame_delay = 1000 // self.FPS
        self.last_frame_time = 0
        self.current_frame = 0

    def load_gif_frames(self, gif_path):
        frames = []
        try:
            with Image.open(gif_path) as gif:
                for frame in ImageSequence.Iterator(gif):
                    frame = frame.convert("RGBA")
                    frame_data = frame.tobytes()
                    size = frame.size
                    pygame_frame = pygame.image.fromstring(frame_data, size, "RGBA")
                    pygame_frame = pygame.transform.scale(pygame_frame, (self.WIDTH, self.HEIGHT))
                    frames.append(pygame_frame)
        except Exception as e:
            print(f"Ошибка загрузки GIF: {e}")
            placeholder = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            placeholder.fill(self.BLACK)
            frames.append(placeholder)
        return frames

    def setup_scenes(self):
        self.scenes = [
            {"character": "...",
             "text": "Привет! Меня зовут Акакий. Я программист фермер и на мою ферму нападают Жуки-Баги!"},
            {"character": "Акакий", "text": "Помоги мне спасти мой ПК и сад от вредоносных вирусов!"},
            {"character": "ЖУКИ-БАГИ", "text": "БЖЖЖЖЖЖЖЖЖЖ!"},
            {"character": "", "text": "Нажмите, чтобы продолжить >:)"}
        ]

    def setup_text_boxes(self):
        self.text_box_height = self.HEIGHT // 4
        self.text_box = pygame.Rect(
            self.WIDTH // 20, self.HEIGHT - self.text_box_height - self.HEIGHT // 20,
            self.WIDTH - self.WIDTH // 10, self.text_box_height
        )
        self.character_box = pygame.Rect(
            self.WIDTH // 20 + 10, self.HEIGHT - self.text_box_height - self.HEIGHT // 20 - 10,
            self.WIDTH // 4, self.HEIGHT // 20
        )

    def reset_scene_state(self):
        self.current_scene = 0
        self.current_char = 0
        self.display_text = ""
        self.typing_speed = 30
        self.typing_delay = 1000 // self.typing_speed
        self.last_typing_time = 0
        self.waiting_for_click = False
        self.last_click_time = 0
        self.click_delay = 300

    def handle_events(self):
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if current_time - self.last_click_time > self.click_delay:
                    if self.waiting_for_click:
                        if self.current_scene + 1 >= len(self.scenes):
                            self.running = False
                            return False
                        self.current_scene += 1
                        self.current_char = 0
                        self.display_text = ""
                        self.waiting_for_click = False
                    else:
                        self.display_text = self.scenes[self.current_scene]["text"]
                        self.waiting_for_click = True
                    self.last_click_time = current_time

        return True

    def update(self):
        current_time = pygame.time.get_ticks()

        # Анимация фона
        if current_time - self.last_frame_time > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_time = current_time

        # Посимвольный вывод текста
        if not self.waiting_for_click and current_time - self.last_typing_time > self.typing_delay:
            if self.current_char < len(self.scenes[self.current_scene]["text"]):
                self.display_text += self.scenes[self.current_scene]["text"][self.current_char]
                self.current_char += 1
                self.last_typing_time = current_time
            else:
                self.waiting_for_click = True

    def render(self):
        # Анимированный фон
        self.screen.blit(self.frames[self.current_frame], (0, 0))

        # Полупрозрачное текстовое окно
        s = pygame.Surface((self.text_box.width, self.text_box.height), pygame.SRCALPHA)
        s.fill((*self.GRAY[:3], 200))
        self.screen.blit(s, self.text_box)
        pygame.draw.rect(self.screen, (70, 70, 70), self.text_box, 2, border_radius=10)

        # Имя персонажа
        if self.scenes[self.current_scene]["character"]:
            pygame.draw.rect(self.screen, (100, 100, 100, 200), self.character_box, border_radius=5)
            character_name = self.character_font.render(
                self.scenes[self.current_scene]["character"], True, self.WHITE
            )
            self.screen.blit(character_name, (self.character_box.x + 10, self.character_box.y + 5))

        # Текст с переносом
        wrapped_text = self.wrap_text()
        for i, line in enumerate(wrapped_text[:3]):
            text_surface = self.font.render(line, True, self.WHITE)
            self.screen.blit(text_surface, (self.text_box.x + 20, self.text_box.y + 20 + i * (self.HEIGHT // 20)))

        # Индикатор клика
        if self.waiting_for_click:
            click_indicator = self.font.render("▶", True, self.WHITE)
            self.screen.blit(click_indicator, (self.text_box.right - 40, self.text_box.bottom - 40))

    def wrap_text(self):
        wrapped_text = []
        words = self.display_text.split(' ')
        line = ''
        for word in words:
            test_line = line + word + ' '
            if self.font.size(test_line)[0] < self.text_box.width - 40:
                line = test_line
            else:
                wrapped_text.append(line)
                line = word + ' '
        wrapped_text.append(line)

        if len(wrapped_text) > 3:
            wrapped_text = wrapped_text[:3]
            wrapped_text[-1] = wrapped_text[-1].rstrip() + "..."

        return wrapped_text

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            if not self.handle_events():
                break

            self.update()
            self.render()

            pygame.display.flip()
            clock.tick(60)

        return True  # Возвращает True, если сцена завершена полностью

