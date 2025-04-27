import sys
import tkinter as tk
import pygame
from game_menu import GameMenu
from main_code.dania_game_1.danil_game import CatchTheErrorGame


class Game():
    def __init__(self):
        self.game_menu = GameMenu()

    def pre_run(self):
        if not self.game_menu.run():  # Если вернул False (нажали "Выход")
            pygame.quit()
            sys.exit()
        else:
            self.run()

    def run(self):
        root = tk.Tk()
        game = CatchTheErrorGame(root)
        root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.pre_run()