import tkinter as tk
from .Windows import Window
import subprocess

class Button:
    def __init__(self, root: Window, text="Button", image_path=None, **kwargs):

        self.image = None
        if image_path is not None:
            self.image = tk.PhotoImage(file=image_path)
            self.button = tk.Button(root.root, text=text, image=self.image, compound='center', bd=0, **kwargs)
        else:
            self.button = tk.Button(root.root, text=text, image=self.image, compound='center', **kwargs)

    def place(self, x, y):
        self.button.place(x=x, y=y)

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

    def set_action(self, action):
        self.button.config(command=action)

    def execute_file(self, filepath):
        try:
            subprocess.run(filepath, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute file: {e}")

    def execute(self, file):
        self.set_action(lambda: self.execute_file(file))