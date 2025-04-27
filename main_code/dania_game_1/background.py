import tkinter as tk
from PIL import Image, ImageTk

class Background:
    def __init__(self, master, bg_path, screen_width, screen_height):
        self.master = master
        self.bg_path = bg_path
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.load()

    def load(self):
        try:
            bg_image = Image.open(self.bg_path)
            bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.bg_label = tk.Label(self.master, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.master.configure(bg='black')
