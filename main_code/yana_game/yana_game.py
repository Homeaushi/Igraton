import pygame
import random
from pathlib import Path
from main_code.config import ScreenSize


class YanaGame:
    def __init__(self):
        pygame.init()
        self.setup_screen()
        self.load_assets()
        self.setup_game()

    def setup_screen(self):
        """Настройка экрана игры"""
        self.WIDTH, self.HEIGHT = (ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WIDTH -= 100
        self.HEIGHT -= 100
        pygame.display.set_caption("Беги от ошибок!")

    def load_assets(self):
        """Загрузка изображений и шрифтов"""
        # Получаем путь к ресурсам относительно расположения скрипта
        script_dir = Path(__file__).parent.parent.parent
        resources_dir = script_dir / "Resources" / "yana_images"

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        try:
            # Загрузка изображений
            self.idle_img = pygame.image.load(str(resources_dir / "character.png"))
            self.jump_img = pygame.image.load(str(resources_dir / "characterjump.png"))
            self.run_left_img = pygame.image.load(str(resources_dir / "characterleft.jpg"))
            self.run_right_img = pygame.image.load(str(resources_dir / "character.png"))
            self.portal_img = pygame.image.load(str(resources_dir / "portal.png"))

            # Масштабирование изображений
            self.idle_img = pygame.transform.scale(self.idle_img, (70, 70))
            self.jump_img = pygame.transform.scale(self.jump_img, (70, 70))
            self.run_left_img = pygame.transform.scale(self.run_left_img, (70, 70))
            self.run_right_img = pygame.transform.scale(self.run_right_img, (70, 70))
            self.portal_img = pygame.transform.scale(self.portal_img, (50, 100))
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            self.create_placeholder_images()

    def create_placeholder_images(self):
        """Создание изображений-заглушек при ошибке загрузки"""
        self.idle_img = pygame.Surface((70, 70))
        self.idle_img.fill(self.BLUE)
        self.jump_img = pygame.Surface((70, 70))
        self.jump_img.fill(self.RED)
        self.run_left_img = pygame.Surface((70, 70))
        self.run_left_img.fill(self.GREEN)
        self.run_right_img = pygame.Surface((70, 70))
        self.run_right_img.fill(self.BLUE)
        self.portal_img = pygame.Surface((50, 100))
        self.portal_img.fill((255, 0, 255))  # Фиолетовый

    def setup_game(self):
        """Настройка игровых параметров"""
        self.FPS = 60
        self.gravity = 0.3
        self.player_speed = 5
        self.platform_speed = 5
        self.level_duration = 30000  # 40 секунд
        self.platform_spawn_delay = 500  # 1 секунда задержки
        self.last_platform_spawn_time = 0

        self.reset_game()

    def reset_game(self):
        """Сброс состояния игры"""
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()

        self.player = Player(
            self.idle_img, self.jump_img,
            self.run_left_img, self.run_right_img,
            (200, self.HEIGHT - 200)
        )
        self.all_sprites.add(self.player)

        self.create_initial_platforms()

        self.start_time = pygame.time.get_ticks()
        self.portal_spawned = False
        self.game_over = False
        self.game_won = False

    def create_initial_platforms(self):
        """Создание начальных платформ"""
        platforms = [
            Platform(0, self.HEIGHT - 100, self.WIDTH, 20, self.GREEN),  # Нижняя платформа
            Platform(200, random.randint(self.HEIGHT - 300, self.HEIGHT - 50),
                     random.randint(100, 200), 20, self.GREEN),
            Platform(400, random.randint(self.HEIGHT - 300, self.HEIGHT - 50),
                     random.randint(100, 200), 20, self.GREEN),
            Platform(600, random.randint(self.HEIGHT - 300, self.HEIGHT - 50),
                     random.randint(100, 200), 20, self.GREEN),
        ]

        for platform in platforms:
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def handle_events(self):
        """Обработка событий игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if self.game_over or self.game_won:
                    if event.key == pygame.K_r:  # Перезапуск
                        self.reset_game()
                    if event.key == pygame.K_q:  # Выход
                        return False
        return True

    def update_game_state(self):
        """Обновление состояния игры"""
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.velocity_x = -self.player_speed
        elif keys[pygame.K_RIGHT]:
            self.player.velocity_x = self.player_speed
        else:
            self.player.velocity_x = 0

        # Обновление игрока
        player_fell = self.player.update(self.platforms)
        if player_fell:
            self.game_over = True

        # Движение платформ
        for platform in self.platforms:
            platform.rect.x -= self.platform_speed
            if platform.rect.right < 0:
                platform.kill()

        # Создание новых платформ с задержкой
        if (len(self.platforms) < 9 and
                current_time - self.last_platform_spawn_time > self.platform_spawn_delay):
            self.create_new_platform()
            self.last_platform_spawn_time = current_time

        # Проверка завершения уровня
        if not self.portal_spawned and elapsed_time >= self.level_duration:
            self.spawn_portal()

        # Проверка столкновения с порталом
        if self.portal_spawned and pygame.sprite.spritecollide(self.player, self.portal_group, False):
            self.game_won = True

    def create_new_platform(self):
        """Создание новой платформы"""
        new_platform = Platform(
            self.WIDTH,
            random.randint(self.HEIGHT - 400, self.HEIGHT - 20),
            random.randint(100, 200),
            20,
            self.GREEN
        )
        self.platforms.add(new_platform)
        self.all_sprites.add(new_platform)

    def spawn_portal(self):
        """Создание портала"""
        portal = Portal(
            self.WIDTH - 50,
            random.randint(self.HEIGHT - 300, self.HEIGHT - 150),
            self.portal_img
        )
        self.portal_group.add(portal)
        self.all_sprites.add(portal)
        self.portal_spawned = True
        print("Портал появился!")

    def render(self):
        """Отрисовка игры"""
        self.screen.fill(self.WHITE)
        self.all_sprites.draw(self.screen)

        # Отображение таймера
        remaining_time = max(0, self.level_duration - (pygame.time.get_ticks() - self.start_time))
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {remaining_time // 1000}", True, self.BLACK)
        self.screen.blit(time_text, (self.WIDTH - 100, 50))

        # Отображение экрана завершения
        if self.game_over:
            self.show_end_screen("Провал, попробуй ещё")
        elif self.game_won:
            self.show_end_screen("YOU WIN!")
            return True

        pygame.display.flip()

    def show_end_screen(self, message):
        """Показать экран завершения игры"""
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Полупрозрачный черный
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 74)
        message_text = font.render(message, True, self.WHITE)
        restart_text = font.render("Press R to Restart", True, self.WHITE)
        quit_text = font.render("Press Q to Quit", True, self.WHITE)

        self.screen.blit(message_text, (self.WIDTH // 2 - message_text.get_width() // 2, self.HEIGHT // 3))
        self.screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, self.HEIGHT // 2))
        self.screen.blit(quit_text, (self.WIDTH // 2 - quit_text.get_width() // 2, self.HEIGHT // 2 + 50))

    def run(self):
        """Запуск основного цикла игры"""
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(self.FPS)

            running = self.handle_events()

            if not (self.game_over or self.game_won):
                self.update_game_state()

            if self.render():
                return self.game_won

        pygame.quit()
        return self.game_won


class Player(pygame.sprite.Sprite):
    def __init__(self, idle_img, jump_img, run_left_img, run_right_img, pos):
        super().__init__()
        self.idle_img = idle_img
        self.jump_img = jump_img
        self.run_left_img = run_left_img
        self.run_right_img = run_right_img

        self.image = self.idle_img
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False

    def update(self, platforms):
        """Обновление состояния игрока"""
        self.rect.x += self.velocity_x

        # Гравитация
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Проверка столкновений с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                if self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Проверка на падение
        if self.rect.top > ScreenSize.HEIGHT.value:  # Падение ниже нижней платформы
            return True

        # Анимация
        if self.velocity_y < 0:
            self.image = self.jump_img
        elif self.velocity_x < 0:
            self.image = self.run_left_img
        elif self.velocity_x > 0:
            self.image = self.run_right_img
        else:
            self.image = self.idle_img

        return False

    def jump(self):
        """Прыжок игрока"""
        if self.on_ground:
            self.velocity_y = -15


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
