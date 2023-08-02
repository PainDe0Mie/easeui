from tkinter import Label
from .Windows import Window
from PIL import Image as IMG
from PIL import ImageTk

class Image:
    def __init__(self, root: Window, image_path):
        self.root = root.root
        self.image_path = image_path

        # Open the image file
        img = IMG.open(self.image_path)
        # Convert the image to PhotoImage format
        photo = ImageTk.PhotoImage(img)

        # Create a label and add the image to it
        self.label_image = Label(self.root, image=photo)
        self.label_image.image = photo  # keep a reference to the image

    def place(self, x, y):
        self.label_image.place(x=x, y=y)

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