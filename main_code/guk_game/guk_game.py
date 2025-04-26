import pygame
import sys
from fighter import Fighter
from color import Color
from screen_size import Screen_size


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Screen_size.WIDTH.value, Screen_size.HEIGHT.value))
        pygame.display.set_caption("Лучший файтинг")
        self.clock = pygame.time.Clock()
        self.running = True

        # Загрузка ресурсов
        self.background = self.load_background()
        self.player1, self.player2 = self.create_players()

        # Настройки игры
        self.FPS = 60
        self.DAMAGE_PER_HIT = 1

    def load_background(self):
        """Загрузка фонового изображения"""
        try:
            bg = pygame.image.load(r"/Resources/guk_Images\City1.png").convert()
            return pygame.transform.scale(bg, (Screen_size.WIDTH.value, Screen_size.HEIGHT.value))
        except pygame.error as e:
            print(f"Не удалось загрузить фон: {e}. Используется чёрный фон")
            bg = pygame.Surface((Screen_size.WIDTH.value, Screen_size.HEIGHT.value))
            bg.fill(Color.BLACK.value)
            return bg

    def create_players(self):
        """Создание игроков"""
        player1 = Fighter(
            x=100,
            y=250,
            color=Color.BLUE.value,
            controls={
                "left": pygame.K_a,
                "right": pygame.K_d,
                "attack_up": pygame.K_w,
                "attack_down": pygame.K_s
            },
            image_path=r"/Resources/guk_Images\Персонаж.PNG"
        )

        player2 = Fighter(
            x=1200,
            y=250,
            color=Color.RED.value,
            controls={
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "attack_up": pygame.K_UP,
                "attack_down": pygame.K_DOWN
            },
            image_path=r"/Resources/guk_Images\Враг.png"
        )

        return player1, player2

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == self.player1.controls["attack_up"]:
                    self.player1.attack_up()
                if event.key == self.player2.controls["attack_up"]:
                    self.player2.attack_up()
                if event.key == self.player1.controls["attack_down"]:
                    self.player1.attack_down()
                if event.key == self.player2.controls["attack_down"]:
                    self.player2.attack_down()

    def update(self):
        """Обновление состояния игры"""
        keys = pygame.key.get_pressed()
        self.player1.move(keys, self.player2)
        self.player2.move(keys, self.player1)

        self.player1.update()
        self.player2.update()

    def check_collisions(self):
        """Проверка столкновений атак"""
        p1_attack = self.player1.draw(self.screen)
        p2_attack = self.player2.draw(self.screen)

        if p1_attack and p1_attack.colliderect(self.player2.rect):
            self.player2.health -= self.DAMAGE_PER_HIT

        if p2_attack and p2_attack.colliderect(self.player1.rect):
            self.player1.health -= self.DAMAGE_PER_HIT

    def check_game_over(self):
        """Проверка условий окончания игры"""
        if self.player1.health <= 0 or self.player2.health <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("ИГРА ОКОНЧЕНА", True, Color.WHITE.value)
            self.screen.blit(text, (Screen_size.WIDTH.value // 2 - 180, Screen_size.HEIGHT.value // 2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.running = False

    def render(self):
        """Отрисовка игры"""
        self.screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """Основной игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.check_collisions()
            self.check_game_over()
            self.render()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()