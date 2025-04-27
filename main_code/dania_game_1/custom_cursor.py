import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

class CustomCursor:
    def __init__(self, master, resources_dir):
        self.master = master
        self.resources_dir = resources_dir
        self.cursor_normal_path = os.path.join(self.resources_dir, r"cursor_normal.png")
        self.cursor_clicked_path = os.path.join(self.resources_dir, r"cursor_clicked.png")

        self.cursor_canvas = tk.Canvas(
            self.master,
            width=32,
            height=32,
            bg='black',
            highlightthickness=0,
            bd=0
        )
        self.cursor_canvas.place(x=0, y=0)

        self.current_cursor = "normal"
        self.cursor_id = None
        self.load_cursors()

    def load_cursors(self):
        try:
            normal_img = Image.open(self.cursor_normal_path).resize((32, 32), Image.LANCZOS)
            clicked_img = Image.open(self.cursor_clicked_path).resize((32, 32), Image.LANCZOS)
            self.cursor_normal = ImageTk.PhotoImage(normal_img)
            self.cursor_clicked = ImageTk.PhotoImage(clicked_img)

            self.cursor_id = self.cursor_canvas.create_image(
                16, 16,
                image=self.cursor_normal,
                anchor='center'
            )
        except Exception as e:
            print(f"Ошибка загрузки курсоров: {e}")
            self.create_fallback_cursors()

    def create_fallback_cursors(self):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((4, 4, 28, 28), outline='red', width=2)
        self.cursor_normal = ImageTk.PhotoImage(img)

        img_clicked = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_clicked)
        draw.ellipse((4, 4, 28, 28), fill='red')
        self.cursor_clicked = ImageTk.PhotoImage(img_clicked)

        self.cursor_id = self.cursor_canvas.create_image(
            16, 16,
            image=self.cursor_normal,
            anchor='center'
        )

    def change_cursor(self, state):
        if state == "clicked" and self.current_cursor != "clicked":
            self.cursor_canvas.itemconfig(self.cursor_id, image=self.cursor_clicked)
            self.current_cursor = "clicked"
        elif state == "normal" and self.current_cursor != "normal":
            self.cursor_canvas.itemconfig(self.cursor_id, image=self.cursor_normal)
            self.current_cursor = "normal"

    def move(self, x, y):
        self.cursor_canvas.place(x=x - 16, y=y - 16)
