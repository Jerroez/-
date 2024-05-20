import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AttendanceApp:
    def __init__(self, root):  # Исправлено: __init__ вместо init
        self.root = root
        self.root.title("Учет пропусков занятий")

        # Создание бд
        self.conn = sqlite3.connect('attendance.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                student_name TEXT,
                date TEXT,
                reason TEXT,
                hours_missed INTEGER
            )
        ''')
        self.conn.commit()

        # Интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода данных о пропусках
        input_frame = ttk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Label(input_frame, text="Имя студента:").grid(row=0, column=0, sticky='w')
        self.student_name_entry = ttk.Entry(input_frame)
        self.student_name_entry.grid(row=0, column=1, sticky='w')

        ttk.Label(input_frame, text="Дата пропуска (гггг-мм-дд):").grid(row=1, column=0, sticky='w')
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=1, column=1, sticky='w')

        ttk.Label(input_frame, text="Причина пропуска:").grid(row=2, column=0, sticky='w')
        self.reason_entry = ttk.Entry(input_frame)
        self.reason_entry.grid(row=2, column=1, sticky='w')

        ttk.Label(input_frame, text="Часы пропущенных занятий:").grid(row=3, column=0, sticky='w')
        self.hours_entry = ttk.Entry(input_frame)
        self.hours_entry.grid(row=3, column=1, sticky='w')

        ttk.Button(input_frame, text="Добавить пропуск", command=self.add_attendance).grid(row=4, column=0,
                                                                                           columnspan=2)

        # Фрейм для отображения статистики
        stats_frame = ttk.Frame(self.root)
        stats_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Button(stats_frame, text="Показать статистику", command=self.show_stats).grid(row=0, column=0, columnspan=2)

    def add_attendance(self):
        student_name = self.student_name_entry.get()
        date = self.date_entry.get()
        reason = self.reason_entry.get()
        hours_missed = self.hours_entry.get()

        if student_name and date and hours_missed:
            self.cursor.execute('INSERT INTO attendance (student_name, date, reason, hours_missed) VALUES (?, ?, ?, ?)',
                                (student_name, date, reason, hours_missed))
            self.conn.commit()
            messagebox.showinfo("Готово", "Данные о пропуске добавлены")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")


    def show_stats(self):
        # Отображения статистики пропусков
        pass



if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
