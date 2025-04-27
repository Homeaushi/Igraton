import pygame
import sys
from main_code.config import Color,ScreenSize
from main_code.guk_game.enemy import Enemy
from main_code.guk_game.player import Player



class GukGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
        pygame.display.set_caption("Лучший файтинг")
        self.clock = pygame.time.Clock()
        self.running = True

        # Загрузка ресурсов
        self.background = self._load_background()
        self.player1, self.player2 = self._create_players()

        # Настройки игры
        self.FPS = 60
        self.DAMAGE_PER_HIT = 0.4

        # Сообщение о повреждении
        self.show_damage_message = False
        self.message_timer = 0
        self.message_duration = 2000  # 2 секунды
        self.font = pygame.font.Font(None, 60 )

    def _load_background(self):
        try:
            bg = pygame.image.load(r"C:\Users\danil\PycharmProjects\Igraton\Resources\guk_Images\City1.png").convert()
            return pygame.transform.scale(bg, (ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
        except:
            bg = pygame.Surface((ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
            bg.fill(Color.BLACK.value)
            return bg

    def _create_players(self):
        player1 = Player(
            x=100, y=250,
            color=Color.BLUE.value,
            controls={
                "left": pygame.K_a,
                "right": pygame.K_d,
                "attack_up": pygame.K_w,
                "attack_down": pygame.K_s
            },
            image_path=r"C:\Users\danil\PycharmProjects\Igraton\Resources\guk_Images\Персонаж.PNG"
        )

        player2 = Enemy(
            x=1200, y=250,
            color=Color.RED.value,
            image_path=r"C:\Users\danil\PycharmProjects\Igraton\Resources\guk_Images\Враг.png"
        )
        return player1, player2

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == self.player1.controls["attack_up"]:
                    self.player1.attack_up()
                if event.key == self.player1.controls["attack_down"]:
                    self.player1.attack_down()

    def _update(self):
        keys = pygame.key.get_pressed()
        self.player1.move(keys, self.player2)
        self.player1.update()
        self.player2.update(self.player1)


    def check_collisions(self):
        # Проверка обычных атак
        p1_attack = self.player1.draw(self.screen)
        p2_attack = self.player2.draw(self.screen)

        if p1_attack and p1_attack.colliderect(self.player2.rect):
            self.player2.health -= self.DAMAGE_PER_HIT

        # Проверка снарядов игрока 2 (врага)
        for proj in self.player2.projectiles[:]:
            # Столкновение с игроком 1
            if proj.rect.colliderect(self.player1.rect):
                self.player2.projectiles.remove(proj)
                self.show_damage_message = True
                self.message_timer = pygame.time.get_ticks()
            # Столкновение с атакой игрока 1
            elif p1_attack and proj.rect.colliderect(p1_attack):
                self.player2.projectiles.remove(proj)

    def check_game_over(self):
        if self.player1.health <= 0 or self.player2.health <= 0:
            font = pygame.font.Font(None, 74)
            text = font.render("ИГРА ОКОНЧЕНА", True, Color.WHITE.value)
            self.screen.blit(text, (ScreenSize.WIDTH.value // 2 - 180, ScreenSize.HEIGHT.value // 2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.running = False

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        # Проверяем, нужно ли показывать сообщение о повреждении
        current_time = pygame.time.get_ticks()
        if self.show_damage_message and current_time - self.message_timer < self.message_duration:
            text = self.font.render("Вам нанесён моральный урон", True, (255, 0, 0))  # Красный цвет
            text_rect = text.get_rect(center=(ScreenSize.WIDTH.value // 2, 50))
            self.screen.blit(text, text_rect)
        else:
            self.show_damage_message = False

        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self.check_collisions()
            self.check_game_over()
            self.render()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GukGame()
    game.run()
