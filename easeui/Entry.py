import tkinter as tk
from .Windows import Window

class Entry:
    def __init__(self, root: Window, **kwargs):
        self.root = root.root

        self.text_var = tk.StringVar(self.root)

        self.entry = tk.Entry(self.root, textvariable=self.text_var, **kwargs)

    def place(self, x, y):
        self.entry.place(x=x, y=y)

    def align(self, horizontal='left', vertical='top'):
        x, y = 0, 0
    
        if isinstance(horizontal, float):
            x = int(self.window.window_width * horizontal) - self.button.winfo_width() // 2
        else:
            if horizontal == 'center':
                x = (self.window.window_width - self.button.winfo_width()) // 2
            elif horizontal == 'right':
                x = self.window.window_width - self.button.winfo_width()

        if isinstance(vertical, float):
            y = int(self.window.window_height * vertical) - self.button.winfo_height() // 2
        else:
            if vertical == 'center':
                y = (self.window.window_height - self.button.winfo_height()) // 2
            elif vertical == 'bottom':
                y = self.window.window_height - self.button.winfo_height()

        self.place(x, y)

    def get_text(self):
        return self.text_var.get()

    def set_text(self, text):
        self.text_var.set(text)