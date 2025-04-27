import pygame
import random
import sys
from PIL import Image, ImageSequence
from main_code.config import ScreenSize, Color


class Player:
    def __init__(self):
        self.size = int(ScreenSize.HEIGHT.value * 0.2)
        self.x = ScreenSize.WIDTH.value // 2 - self.size // 2
        self.y = ScreenSize.HEIGHT.value - self.size * 2
        self.speed = 10
        self.lanes = [
            ScreenSize.WIDTH.value // 4 - self.size // 2,
            ScreenSize.WIDTH.value // 2 - self.size // 2,
            ScreenSize.WIDTH.value * 3 // 4 - self.size // 2
        ]
        self.current_lane = 1
        self.frames = self.load_gif_frames(
            r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images\animation_person.gif",
            (self.size, self.size)
        )
        self.current_frame = 0

    def load_gif_frames(self, gif_path, size):
        gif = Image.open(gif_path)
        frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            pygame_frame = pygame.transform.scale(pygame_frame, size)
            frames.append(pygame_frame)
        return frames

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.current_lane > 0:
            self.current_lane -= 1
        elif keys[pygame.K_RIGHT] and self.current_lane < 2:
            self.current_lane += 1
        self.x = self.lanes[self.current_lane]
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class Enemy:
    def __init__(self, x, y, size, image):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = image
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 7
        self.size = size

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, Color.GREEN.value, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))
        pygame.display.set_caption("Pixel Tanks")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.player = Player()
        self.enemy_images = self.load_enemy_images()
        self.enemies = []
        self.bullets = []
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.score = 0
        self.kill_count = 0

        self.states = {
            "MENU": 0,
            "PLAYING": 1,
            "GAME_OVER": 2
        }
        self.current_state = self.states["MENU"]

        self.font = pygame.font.Font(None, int(ScreenSize.HEIGHT.value * 0.05))

    def load_enemy_images(self):
        paths = [
            r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images\vrag1.PNG",
            r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images\vrag2.PNG",
            r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images\vrag3.PNG",
            r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images\vrag4.PNG",
            r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images\vrag5.PNG",
        ]
        images = []
        for path in paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (self.player.size, self.player.size))
            images.append(image)
        return images

    def draw_background(self):
        pygame.draw.rect(self.screen, Color.SKY_BLUE.value, (0, 0, ScreenSize.WIDTH.value, ScreenSize.HEIGHT.value))

        pygame.draw.rect(self.screen, Color.GREEN.value,
                         (0, 0, ScreenSize.WIDTH.value // 4 - self.player.size // 2, ScreenSize.HEIGHT.value))
        pygame.draw.rect(self.screen, Color.GREEN.value,
                         (ScreenSize.WIDTH.value * 3 // 4 + self.player.size // 2, 0, ScreenSize.WIDTH.value,
                          ScreenSize.HEIGHT.value))

        for i in range(3):
            lane_x = self.player.lanes[i]
            pygame.draw.rect(self.screen, Color.WHITE.value, (lane_x, 0, self.player.size, ScreenSize.HEIGHT.value))

        for i in range(3):
            lane_x = self.player.lanes[i]
            for _ in range(10):
                x = lane_x + random.randint(-self.player.size // 2, self.player.size // 2)
                y = random.randint(0, ScreenSize.HEIGHT.value)
                size = random.randint(5, 15)
                pygame.draw.circle(self.screen, Color.RED.value, (x, y), size)

    def draw_button(self, text, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, Color.BLACK.value)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def check_collision(self, rect, targets):
        for target in targets:
            if rect.colliderect(target.rect):
                return True, target
        return False, None

    def spawn_enemy(self):
        lane = random.randint(0, 2)
        enemy_x = self.player.lanes[lane]
        enemy_y = -self.player.size
        enemy_image = random.choice(self.enemy_images)
        self.enemies.append(Enemy(enemy_x, enemy_y, self.player.size, enemy_image))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.current_state == self.states["MENU"]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (ScreenSize.WIDTH.value // 2 - 100 <= mouse_x <= ScreenSize.WIDTH.value // 2 + 100 and
                            ScreenSize.HEIGHT.value // 2 - 50 <= mouse_y <= ScreenSize.HEIGHT.value // 2):
                        self.current_state = self.states["PLAYING"]
                    elif (ScreenSize.WIDTH.value // 2 - 100 <= mouse_x <= ScreenSize.WIDTH.value // 2 + 100 and
                          ScreenSize.HEIGHT.value // 2 + 20 <= mouse_y <= ScreenSize.HEIGHT.value // 2 + 70):
                        return False

            elif self.current_state == self.states["PLAYING"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullet_x = self.player.x + self.player.size // 2 - self.player.size // 3 // 2
                    bullet_y = self.player.y
                    self.bullets.append(Bullet(bullet_x, bullet_y, self.player.size // 3))

            elif self.current_state == self.states["GAME_OVER"]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (ScreenSize.WIDTH.value // 2 - 100 <= mouse_x <= ScreenSize.WIDTH.value // 2 + 100 and
                            ScreenSize.HEIGHT.value // 2 + 70 <= mouse_y <= ScreenSize.HEIGHT.value // 2 + 120):
                        self.reset_game()
                    elif (ScreenSize.WIDTH.value // 2 - 100 <= mouse_x <= ScreenSize.WIDTH.value // 2 + 100 and
                          ScreenSize.HEIGHT.value // 2 + 140 <= mouse_y <= ScreenSize.HEIGHT.value // 2 + 190):
                        return False

        return True

    def reset_game(self):
        self.current_state = self.states["PLAYING"]
        self.score = 0
        self.kill_count = 0
        self.enemies = []
        self.bullets = []
        self.spawn_timer = 0
        self.player.current_lane = 1
        self.player.x = self.player.lanes[self.player.current_lane]

    def update(self):
        if self.current_state == self.states["PLAYING"]:
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_enemy()
                self.spawn_timer = 0

            for enemy in self.enemies:
                enemy.update()
            self.enemies = [enemy for enemy in self.enemies if enemy.rect.y < ScreenSize.HEIGHT.value]

            for bullet in self.bullets:
                bullet.update()
            self.bullets = [bullet for bullet in self.bullets if bullet.rect.y > -bullet.size]

            for bullet in self.bullets[:]:
                hit, enemy = self.check_collision(bullet.rect, self.enemies)
                if hit:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    self.score *= 12
                    self.kill_count += 1

            if self.check_collision(self.player.get_rect(), self.enemies)[0]:
                self.current_state = self.states["GAME_OVER"]

    def draw(self):
        if self.current_state == self.states["MENU"]:
            self.screen.fill(Color.SKY_BLUE.value)
            self.draw_button("Начать игру", ScreenSize.WIDTH.value // 2 - 100,
                             ScreenSize.HEIGHT.value // 2 - 50, 200, 50, Color.WHITE.value)
            self.draw_button("Выйти", ScreenSize.WIDTH.value // 2 - 100,
                             ScreenSize.HEIGHT.value // 2 + 20, 200, 50, Color.WHITE.value)

        elif self.current_state == self.states["PLAYING"]:
            self.draw_background()
            self.player.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            for bullet in self.bullets:
                bullet.draw(self.screen)

            score_text = self.font.render(f"Score: {self.score}", True, Color.BLACK.value)
            kill_count_text = self.font.render(f"Истребленные вирусы: {self.kill_count}", True, Color.BLACK.value)
            self.screen.blit(score_text, (40, 60))
            self.screen.blit(kill_count_text, (40, 30))

        elif self.current_state == self.states["GAME_OVER"]:
            self.screen.fill(Color.SKY_BLUE.value)
            game_over_text = self.font.render("Game Over", True, Color.RED.value)
            score_text = self.font.render(f"Score: {self.score}", True, Color.BLACK.value)
            kill_count_text = self.font.render(f"Истребленные вирусы: {self.kill_count}", True, Color.BLACK.value)

            self.screen.blit(game_over_text, (ScreenSize.WIDTH.value // 2 - game_over_text.get_width() // 2,
                                              ScreenSize.HEIGHT.value // 2 - 100))
            self.screen.blit(score_text, (ScreenSize.WIDTH.value // 2 - score_text.get_width() // 2,
                                          ScreenSize.HEIGHT.value // 2 - 50))
            self.screen.blit(kill_count_text, (ScreenSize.WIDTH.value // 2 - kill_count_text.get_width() // 2,
                                               ScreenSize.HEIGHT.value // 2))

            self.draw_button("Рестарт", ScreenSize.WIDTH.value // 2 - 100,
                             ScreenSize.HEIGHT.value // 2 + 70, 200, 50, Color.WHITE.value)
            self.draw_button("Выйти", ScreenSize.WIDTH.value // 2 - 100,
                             ScreenSize.HEIGHT.value // 2 + 140, 200, 50, Color.WHITE.value)

        pygame.display.flip()
        self.clock.tick(self.FPS)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()