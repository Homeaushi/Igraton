import pygame
from player import Player
from level_design import Level
from camera import Camera

class Level4:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Уровень 4: Полный экран")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        """Полностью сбрасывает состояние игры"""
        self.level = Level("level4_map.json")
        self.player = Player(100, 200)
        self.camera = Camera(
            self.screen_width, 
            self.screen_height,
            self.level.level_width,
            self.level.level_height,
            
        )
        self.all_sprites = pygame.sprite.Group(self.player)
        self.all_sprites.add(*self.level.platforms, *self.level.buffs)
        self.game_over = False
        self.death_timer = 0  # Таймер перед перезапуском
        self.level_complete = False  # Уровень не завершен изначально

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Дельта времени в секундах
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over and not self.level_complete:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN and self.level_complete:
                        running = False  # выход при нажатии Enter после завершения уровня
            
            # Логика игры
            if not self.game_over and not self.level_complete:
                self.player.update(self.level.platforms, self.level.hazards)
                self.camera.update(self.player)
                self.check_buff_collisions()

                if getattr(self.player, "is_dead", False):
                    self.game_over = True
                    self.death_timer = 2.0

                # Проверка выхода за правую границу экрана
                if self.player.rect.x > self.level.level_width - 0.01:
                    self.level_complete = True

            elif self.game_over:
                self.death_timer -= dt
                if self.death_timer <= 0:
                    self.reset_game()

            # Отрисовка
            self.screen.fill((30, 30, 50))
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

            # Отрисовываем шипы
            for hazard in self.level.hazards:
                self.screen.blit(hazard.image, self.camera.apply(hazard))

            self.draw_health_bar()

            # Показываем сообщение о завершении уровня
            if self.level_complete:
                self.show_level_complete()

            if self.game_over:
                self.show_game_over(self.death_timer)

            pygame.display.flip()

    def check_buff_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.level.buffs, True)
        for buff in hits:
            self.player.apply_buff(buff.type)

    def draw_health_bar(self):
        # Ваша текущая реализация
        pass

    def show_game_over(self, time_left):
        font = pygame.font.SysFont(None, 80)
        text = font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.screen.blit(text, text_rect)

        # Показываем обратный отсчет
        countdown_text = pygame.font.SysFont(None, 50).render(
            f"Перезапуск через: {max(0, int(time_left))} сек", 
            True, (255, 255, 255)
        )
        countdown_rect = countdown_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 20))
        self.screen.blit(countdown_text, countdown_rect)

    def show_level_complete(self):
        font = pygame.font.SysFont(None, 80)
        text = font.render("УРОВЕНЬ ПРОЙДЕН!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.screen.blit(text, text_rect)

        enter_text = pygame.font.SysFont(None, 50).render(
            "Нажмите Enter для выхода", True, (255, 255, 255)
        )
        enter_rect = enter_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 20))
        self.screen.blit(enter_text, enter_rect)

if __name__ == "__main__":
    game = Level4()
    game.run()
