import tkinter as tk

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
