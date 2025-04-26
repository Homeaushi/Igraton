import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageDraw
import os


class CustomCursor:
    def __init__(self, master, resources_dir):
        self.master = master
        self.resources_dir = resources_dir
        self.cursor_normal_path = os.path.join(self.resources_dir, "Default_hand.png")
        self.cursor_clicked_path = os.path.join(self.resources_dir, "Click_hand.png")

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


class GameUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg='SystemButtonFace')
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.title_label = tk.Label(
            self.frame,
            text="CATCH THE ERROR!",
            font=("Arial", 40, "bold"),
            fg="red",
            bg='SystemButtonFace',
            highlightthickness=0
        )
        self.title_label.pack(pady=40)

        self.score_label = tk.Label(
            self.frame,
            text="Очки: 0 | Время: 30",
            font=("Arial", 24),
            fg="white",
            bg='SystemButtonFace',
            highlightthickness=0
        )
        self.score_label.pack()

        self.play_button = tk.Button(
            self.frame,
            text="НАЧАТЬ ИГРУ",
            font=("Arial", 24),
            width=20,
            bg="red",
            fg="white",
            activebackground="darkred",
            highlightthickness=0,
            bd=0
        )
        self.play_button.pack(pady=60)

    def update_score(self, score, time_left):
        self.score_label.config(text=f"Очки: {score} | Время: {time_left}")


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
        self.resources_dir = r"C:\Users\danil\PycharmProjects\Igraton\Resources\dania_images"
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


if __name__ == "__main__":
    root = tk.Tk()
    game = CatchTheErrorGame(root)
    root.mainloop()