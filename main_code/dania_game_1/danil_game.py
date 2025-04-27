import tkinter as tk
from tkinter import messagebox
import os
from main_code.dania_game_1.background import Background
from main_code.dania_game_1.custom_cursor import CustomCursor
from main_code.dania_game_1.error_window import ErrorWindow
from main_code.dania_game_1.game_UI import GameUI


class CatchTheErrorGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Catch The Error!")
        self.master.attributes('-fullscreen', True)

        # Получаем размеры экрана
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # Настройки игры
        self.score = 0
        self.time_left = 30
        self.game_active = False

        # Пути к ресурсам
        self.resources_dir = r"C:\Users\alex_\РАБ. СТОЛ\python\Igraton\Resources\dania_images"
        self.bg_path = os.path.join(self.resources_dir, "Виндоус ХР.jpg")

        # Инициализация компонентов
        self.background = Background(self.master, self.bg_path, self.screen_width, self.screen_height)
        self.cursor = CustomCursor(self.master, self.resources_dir)
        self.ui = GameUI(self.master)
        self.error_window = ErrorWindow(self.master, self.screen_width, self.screen_height)

        # Настройка кнопки
        self.ui.play_button.config(command=self.start_game)

        # Привязка событий
        self.master.bind('<Escape>', lambda e: self.exit_game())
        self.master.bind('<Motion>', lambda e: self.cursor.move(e.x, e.y))
        self.master.bind('<ButtonPress>', lambda e: self.cursor.change_cursor("clicked"))
        self.master.bind('<ButtonRelease>', lambda e: self.cursor.change_cursor("normal"))

        # Скрываем стандартный курсор
        self.master.config(cursor='none')

    def start_game(self):
        self.game_active = True
        self.score = 0
        self.time_left = 30
        self.ui.play_button.config(state=tk.DISABLED)
        self.ui.update_score(self.score, self.time_left)
        self.spawn_error_window()
        self.update_timer()

    def spawn_error_window(self):
        window = self.error_window.create()
        tk.Button(
            window,
            text="FIX",
            command=self.fix_error,
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            activebackground="darkred"
        ).pack(pady=10)

        width = min(400, self.screen_width // 3)
        height = min(200, self.screen_height // 4)
        self.error_window.move(width, height)

        if self.time_left > 0:
            window.after(1000, lambda: self.move_error_window(width, height))

    def move_error_window(self, width, height):
        if self.game_active:
            self.error_window.move(width, height)
            if self.time_left > 0:
                self.error_window.window.after(1000, lambda: self.move_error_window(width, height))

    def fix_error(self):
        if self.game_active:
            self.score += 1
            self.ui.update_score(self.score, self.time_left)
            self.error_window.window.config(bg="green")
            self.error_window.window.update()
            self.master.after(100, lambda: self.error_window.window.destroy())
            self.master.after(300, self.spawn_error_window)

    def update_timer(self):
        if self.time_left > 0 and self.game_active:
            self.time_left -= 1
            self.ui.update_score(self.score, self.time_left)
            self.master.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        self.game_active = False
        if hasattr(self.error_window, 'window') and self.error_window.window.winfo_exists():
            self.error_window.window.destroy()
        self.ui.play_button.config(state=tk.NORMAL)
        messagebox.showinfo(
            "Игра окончена!",
            f"Вы исправили {self.score} ошибок!\nПопробуйте ещё раз!"
        )

    def exit_game(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.master.destroy()