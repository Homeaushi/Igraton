import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageDraw
import os

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
        self.error_window = None

        # Пути к ресурсам
        self.resources_dir = r"C:\Users\danil\PycharmProjects\Igraton\Resources\данич имагес"
        self.bg_path = os.path.join(self.resources_dir, "Виндоус ХР.jpg")
        self.cursor_normal_path = os.path.join(self.resources_dir, "Default_hand.png")
        self.cursor_clicked_path = os.path.join(self.resources_dir, "Click_hand.png")

        # Загрузка фона
        self.load_background()

        # Создаем Canvas для курсора
        self.cursor_canvas = tk.Canvas(
            self.master,
            width=32,
            height=32,
            bg='black',
            highlightthickness=0,
            bd=0
        )
        self.cursor_canvas.place(x=0, y=0)

        # Загрузка курсоров
        self.load_custom_cursors()

        # Интерфейс
        self.setup_ui()

        # Привязка событий
        self.master.bind('<Escape>', lambda e: self.exit_game())
        self.master.bind('<Motion>', self.move_cursor)
        self.master.bind('<ButtonPress>', lambda e: self.change_cursor("clicked"))
        self.master.bind('<ButtonRelease>', lambda e: self.change_cursor("normal"))

        # Скрываем стандартный курсор
        # self.master.config(cursor='none')  # Закомментируйте для тестирования

    def load_background(self):
        """Загружает фоновое изображение"""
        try:
            if os.path.exists(self.bg_path):
                bg_image = Image.open(self.bg_path)
                bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                self.bg_label = tk.Label(self.master, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bg_label.lower()
            else:
                raise FileNotFoundError("Фоновое изображение не найдено")
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
            self.master.configure(bg='black')

    def load_custom_cursors(self):
        """Загружает кастомные курсоры"""
        try:
            if not os.path.exists(self.cursor_normal_path):
                raise FileNotFoundError("Файл курсора не найден")
            if not os.path.exists(self.cursor_clicked_path):
                raise FileNotFoundError("Файл курсора (нажатие) не найден")
            normal_img = Image.open(self.cursor_normal_path)
            clicked_img = Image.open(self.cursor_clicked_path)
            # Проверяем размеры изображений
            if normal_img.size != (32, 32) or clicked_img.size != (32, 32):
                raise ValueError("Размер изображений курсора должен быть 32x32 пикселя")
            normal_img = normal_img.resize((32, 32), Image.LANCZOS)
            clicked_img = clicked_img.resize((32, 32), Image.LANCZOS)
            self.cursor_normal = ImageTk.PhotoImage(normal_img)
            self.cursor_clicked = ImageTk.PhotoImage(clicked_img)
            self.current_cursor = "normal"
            self.cursor_id = self.cursor_canvas.create_image(
                16, 16,
                image=self.cursor_normal,
                anchor='center'
            )
        except Exception as e:
            print(f"Ошибка загрузки курсоров: {e}")
            self.create_fallback_cursors()

    def create_fallback_cursors(self):
        """Создает простые курсоры"""
        try:
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
            self.current_cursor = "normal"
        except Exception as e:
            print(f"Ошибка создания резервных курсоров: {e}")
            self.master.config(cursor='arrow')

    def change_cursor(self, state):
        """Меняет вид курсора"""
        if hasattr(self, 'cursor_id'):
            print(f"Состояние курсора: {state}")  # Отладочный вывод
            if state == "clicked" and self.current_cursor != "clicked":
                self.cursor_canvas.itemconfig(self.cursor_id, image=self.cursor_clicked)
                self.current_cursor = "clicked"
            elif state == "normal" and self.current_cursor != "normal":
                self.cursor_canvas.itemconfig(self.cursor_id, image=self.cursor_normal)
                self.current_cursor = "normal"

    def move_cursor(self, event):
        """Перемещает курсор"""
        if hasattr(self, 'cursor_canvas') and self.cursor_canvas.winfo_exists():
            print(f"Позиция курсора: x={event.x}, y={event.y}")  # Отладочный вывод
            self.cursor_canvas.place(x=event.x - 16, y=event.y - 16)

    def setup_ui(self):
        """Создает интерфейс игры"""
        self.ui_frame = tk.Frame(self.master, bg='SystemButtonFace')
        self.ui_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.title_label = tk.Label(
            self.ui_frame,
            text="CATCH THE ERROR!",
            font=("Arial", 40, "bold"),
            fg="red",
            bg='SystemButtonFace',
            highlightthickness=0
        )
        self.title_label.pack(pady=40)

        self.score_label = tk.Label(
            self.ui_frame,
            text=f"Очки: {self.score} | Время: {self.time_left}",
            font=("Arial", 24),
            fg="white",
            bg='SystemButtonFace',
            highlightthickness=0
        )
        self.score_label.pack()

        self.play_button = tk.Button(
            self.ui_frame,
            text="НАЧАТЬ ИГРУ",
            command=self.start_game,
            font=("Arial", 24),
            width=20,
            bg="red",
            fg="white",
            activebackground="darkred",
            highlightthickness=0,
            bd=0
        )
        self.play_button.pack(pady=60)

    def start_game(self):
        """Начинает игру"""
        try:
            print("Игра начата!")  # Отладочный вывод
            self.game_active = True
            self.score = 0
            self.time_left = 30
            self.play_button.config(state=tk.DISABLED)
            self.update_score_display()
            self.spawn_error_window()
            self.update_timer()
        except Exception as e:
            print(f"Ошибка при старте игры: {e}")

    def spawn_error_window(self):
        """Создаёт новое окно с ошибкой"""
        try:
            if self.error_window and self.error_window.winfo_exists():
                self.error_window.destroy()
            self.error_window = tk.Toplevel(self.master)
            self.error_window.overrideredirect(True)
            self.error_window.attributes('-topmost', True)
            self.error_window.configure(bg='white')
            error_width = min(400, self.screen_width // 3)
            error_height = min(200, self.screen_height // 4)
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
                self.error_window,
                text=error_text,
                font=("Arial", 12, "bold"),
                fg="black",
                bg="white"
            ).pack(pady=10)
            tk.Button(
                self.error_window,
                text="FIX",
                command=self.fix_error,
                bg="red",
                fg="white",
                font=("Arial", 10, "bold"),
                width=10,
                activebackground="darkred"
            ).pack(pady=10)
            self.move_error_window(error_width, error_height)
        except Exception as e:
            print(f"Ошибка при создании окна с ошибкой: {e}")

    def move_error_window(self, width, height):
        """Перемещает окно с ошибкой"""
        if not self.game_active:
            return
        new_x = random.randint(0, self.screen_width - width)
        new_y = random.randint(0, self.screen_height - height)
        self.error_window.geometry(f"{width}x{height}+{new_x}+{new_y}")
        if self.time_left > 0:
            self.error_window.after(1000, lambda: self.move_error_window(width, height))

    def fix_error(self):
        """Игрок устранил ошибку"""
        if self.game_active:
            self.score += 1
            self.update_score_display()
            self.error_window.config(bg="green")
            self.error_window.update()
            self.master.after(100, lambda: self.error_window.destroy())
            self.master.after(300, self.spawn_error_window)

    def update_timer(self):
        """Обновляет таймер"""
        if self.time_left > 0 and self.game_active:
            self.time_left -= 1
            self.update_score_display()
            self.master.after(1000, self.update_timer)
        else:
            self.end_game()

    def update_score_display(self):
        """Обновляет счётчик очков и времени"""
        self.score_label.config(text=f"Очки: {self.score} | Время: {self.time_left}")

    def end_game(self):
        """Завершает игру"""
        self.game_active = False
        if self.error_window and self.error_window.winfo_exists():
            self.error_window.destroy()
        self.play_button.config(state=tk.NORMAL)
        messagebox.showinfo(
            "Игра окончена!",
            f"Вы исправили {self.score} ошибок!\nПопробуйте ещё раз!"
        )

    def exit_game(self):
        """Выход из игры"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = CatchTheErrorGame(root)
    root.mainloop()