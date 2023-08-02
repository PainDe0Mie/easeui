import tkinter as tk

class Window:
    def __init__(self, title="Window", size=(200, 200)):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.window_width = size[0]
        self.window_height = size[1]

    def center(self):
        x = (self.screen_width - self.window_width) // 2
        y = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"+{x}+{y}")

    def top_left(self):
        self.root.geometry(f"+0+0")

    def top_right(self):
        x = self.screen_width - self.window_width
        self.root.geometry(f"+{x}+0")

    def bottom_left(self):
        y = self.screen_height - self.window_height
        self.root.geometry(f"+0+{y}")

    def bottom_right(self):
        x = self.screen_width - self.window_width
        y = self.screen_height - self.window_height
        self.root.geometry(f"+{x}+{y}")
        
    def run(self):
        self.root.mainloop()