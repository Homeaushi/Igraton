import pygame
import sys

from config import ScreenSize


class GameMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
        screen_width, screen_height = (ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value)
        pygame.display.set_caption("Меню игры")
        self.clock = pygame.time.Clock()

        # Загрузка фона
        try:
            self.background = pygame.image.load(
                r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\Menu\lobby.png").convert()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except:
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill((50, 50, 50))  # Серый фон, если картинка не загрузилась

        # Шрифт
        self.font = pygame.font.Font(None, 48)

        # Кнопки
        self.run_button_width = 620
        self.run_button_height = 120
        self.run_button_color = (70, 130, 180)  # SteelBlue
        self.run_button_hover_color = (100, 150, 200)

        self.exit_button_width = 450
        self.exit_button_height = 100
        self.exit_button_color = (70, 130, 180)  # SteelBlue
        self.exit_button_hover_color = (100, 150, 200)

        # Кнопка "Запуск игры"
        self.start_button = pygame.Rect(
            480,
            335,
            self.run_button_width,
            self.run_button_height
        )

        # Кнопка "Выход"
        self.exit_button = pygame.Rect(
            480,
            650,
            self.exit_button_width,
            self.exit_button_height
        )

        self.running = True
        self.game_started = False

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        start_hover = self.start_button.collidepoint(mouse_pos)
        exit_hover = self.exit_button.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_hover:
                    self.game_started = True
                    self.running = False
                elif exit_hover:
                    self.running = False

        return start_hover, exit_hover

    def run(self):
        while self.running:
            start_hover, exit_hover = self.handle_events()

            # Отрисовка
            self.screen.blit(self.background, (0, 0))

            # Заголовок меню
            title = self.font.render("Главное меню", True, (255, 255, 255))
            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

            pygame.display.flip()
            self.clock.tick(60)

        return self.game_started


# # Пример использования
# if __name__ == "__main__":
#     menu = GameMenu()
#     game_started = menu.run()
#
#     if game_started:
#         print("Игра запускается...")
#         # Здесь можно запустить основной игровой цикл
#     else:
#         print("Выход из игры")
#         pygame.quit()
#         sys.exit()
