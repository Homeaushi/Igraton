import tkinter as tk
import random

class ErrorWindow:
    def __init__(self, master, screen_width, screen_height):
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = None

    def create(self):
        if self.window and self.window.winfo_exists():
            self.window.destroy()

        self.window = tk.Toplevel(self.master)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='white')

        error_text = random.choice([
            "Ошибка СИСТЕМНЫЙ СБОЙ!",
            "ДОСТУП ЗАПРЕЩЁН!",
            "ОШИБКА 0xDEADBEEF!",
            "НЕФИГ БЫЛО ЗАХОДИТЬ НА ПОРНО САЙТЫ!",
            "ТЫ МЕНЯ НЕ ПОЙМАЕШЬ!!",
            "ПОПРОБУЙ ОСТАНОВИТЬ МЕНЯ!))))",
            "AXAXAXAXAXAXX",
            "МЕШОК ПЛОТИ, ЧТО ТЫ МНЕ СДЕЛАЕШЬ?))",
            "ДЫШИ, ДЫШИ, ДЫШИ"
        ])

        tk.Label(
            self.window,
            text=error_text,
            font=("Arial", 12, "bold"),
            fg="black",
            bg="white"
        ).pack(pady=10)

        return self.window

    def move(self, width, height):
        new_x = random.randint(0, self.screen_width - width)
        new_y = random.randint(0, self.screen_height - height)
        self.window.geometry(f"{width}x{height}+{new_x}+{new_y}")

