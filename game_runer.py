import sys
import tkinter as tk
import pygame
from game_menu import GameMenu
from main_code.dania_game_1.danil_game import CatchTheErrorGame
from main_code.guk_game.guk_game import GukGame
from main_code.yana_game.yana_game import YanaGame
from main_code.юля.yula_game import YulaGame
from main_start.scene_1 import Scene_1
from main_start.scene_2 import Scene_2
from main_code.sasha_game.main import Level4

class Game():
    def __init__(self):
        self.game_menu = GameMenu()
        self.pre_run(self.game_menu)

    def pre_run(self, game_menu):
        if not self.game_menu.run():  # Если вернул False (нажали "Выход")
            pygame.quit()
            sys.exit()
        else:
            self.run()

    def run(self):
        scene = Scene_1()
        scene_completed = scene.run()
        if scene_completed:
            if(YulaGame().run()):
                scene = Scene_2()
                scene_completed = scene.run()
                if scene_completed:
                    game = YanaGame()
                    if game.run():
                        root = tk.Tk()
                        game = CatchTheErrorGame(root)
                        root.mainloop()

                        game_4 = Level4()
                        if game_4.run():
                            game = GukGame()
                            if game.run():
                                self.pre_run(GameMenu())





if __name__ == "__main__":
    game = Game()
    game.pre_run()