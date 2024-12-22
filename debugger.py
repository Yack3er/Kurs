import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import traceback
import sys
import os
import trace
from io import StringIO
import linecache

class SimpleDebugger:
    def __init__(self, root):
        self.root = root
        self.root.title("Debugger")

        self.file_path = tk.StringVar()
        self.output_text = tk.StringVar()
        self.start_line = tk.IntVar(value=1)
        self.end_line = tk.IntVar()

        self.create_widgets()
        self.set_theme('light')

    def create_widgets(self):
        self.theme_var = tk.StringVar(value='light')

        tk.Label(self.root, text="Выберите Python файл для отладки:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.file_path, width=50).pack(pady=5)
        tk.Button(self.root, text="Обзор", command=self.browse_file).pack(pady=5)

        line_frame = tk.Frame(self.root)
        line_frame.pack(pady=10)

        tk.Label(line_frame, text="Начальная строка:").pack(side=tk.LEFT, padx=5)
        self.start_line_entry = tk.Entry(line_frame, textvariable=self.start_line, width=10)
        self.start_line_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(line_frame, text="Конечная строка:").pack(side=tk.LEFT, padx=5)
        self.end_line_entry = tk.Entry(line_frame, textvariable=self.end_line, width=10)
        self.end_line_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Отладка", command=self.debug_file).pack(pady=10)

        self.code_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.code_text.pack(pady=10)

        tk.Button(self.root, text="Показать Код", command=self.show_code).pack(pady=5)
        tk.Button(self.root, text="Сохранить Код", command=self.save_code).pack(pady=5)
    def change_theme(self):
        theme = self.theme_var.get()
        self.set_theme(theme)

    def set_theme(self, theme):
        if theme == 'light':
            bg_color = '#FFFFFF'
            fg_color = '#000000'
            text_bg_color = '#FFFFFF'
            text_fg_color = '#000000'
            button_bg_color = '#EEEEEE'
            button_fg_color = '#000000'
            radio_bg_color = '#EEEEEE'
            radio_fg_color = '#000000'
            radio_select_color = '#000000'
            entry_bg_color = '#FFFFFF'
            entry_fg_color = '#000000'

        self.root.config(bg=bg_color)
        self.code_text.config(bg=text_bg_color, fg=text_fg_color)

        style = ttk.Style()
        style.configure('TRadiobutton', background=radio_bg_color, foreground=radio_fg_color,
                        selectbackground=radio_select_color, selectforeground=radio_fg_color)


        for widget in self.root.winfo_children():
            widget_type = widget.winfo_class()
            if widget_type == 'Label':
                widget.config(bg=bg_color, fg=fg_color)
            elif widget_type == 'Button':
                widget.config(bg=button_bg_color, fg=button_fg_color)
            elif widget_type == 'Entry':
                widget.config(bg=entry_bg_color, fg=entry_fg_color)
            elif widget_type == 'Frame':
                widget.config(bg=bg_color)

        self.start_line_entry.config(bg=entry_bg_color, fg=entry_fg_color)
        self.end_line_entry.config(bg=entry_bg_color, fg=entry_fg_color)
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python файлы", "*.py")])
        if file_path:
            self.file_path.set(file_path)
            self.show_code()

    def show_code(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл для отладки.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            self.code_text.delete(1.0, tk.END)
            for i, line in enumerate(lines, start=1):
                self.code_text.insert(tk.END, f"{i:4}  {line}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")