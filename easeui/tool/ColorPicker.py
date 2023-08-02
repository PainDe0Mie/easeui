import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import colorsys

class ColorPicker(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Dimensions du rectangle
        self.resizable(False, False)
        self.title("Palette de couleur")
        self.width, self.height = 200, 200
        self.custom_color_selected_label = None
        self.basic_colors = {
            'red': '#ff0000',
            'green': '#00ff00',
            'blue': '#0000ff',
            'cyan': '#00ffff',
            'magenta': '#ff00ff',
            'yellow': '#ffff00',
            'black': '#000000',
            'white': '#ffffff'
        }
        self.custom_colors_count = 9

        # Créer l'image et la convertir en PhotoImage pour Tkinter
        self.color_rectangle_image = self.draw_color_rectangle(self.width, self.height)
        self.color_rectangle_photoimage = ImageTk.PhotoImage(self.color_rectangle_image)

        # Créer le canvas et afficher l'image
        self.color_rectangle_canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.color_rectangle_canvas.create_image(0, 0, image=self.color_rectangle_photoimage, anchor='nw')
        self.color_rectangle_canvas.bind('<Button-1>', self.color_selected)

        # Créer les couleurs de base
        self.basic_colors_frame = tk.Frame(self)

        for color in self.basic_colors.values():
            swatch = tk.Label(self.basic_colors_frame, bg=color, width=2, height=1, relief="solid", bd=1)
            swatch.pack(side=tk.LEFT, padx=5)  # Ajoute de l'espace entre les carrés
            swatch.bind('<Button-1>', self.basic_color_selected)

        # Créer les carrés de couleurs personnalisables
        self.custom_colors_frame = tk.Frame(self)

        for _ in range(self.custom_colors_count):
            swatch = tk.Label(self.custom_colors_frame, bg='#ffffff', width=2, height=1, relief="solid", bd=1)
            swatch.pack(side=tk.LEFT, padx=5)  # Ajoute de l'espace entre les carrés
            swatch.bind('<Button-1>', self.custom_color_selected)

        self.color_display = tk.Label(self, text='Color Display', width=20)
        self.color_display.pack(side=tk.TOP)

        self.rgb_display = tk.Label(self, text='R:0, G:0, B:0', width=20)
        self.rgb_display.pack(side=tk.TOP)

        self.r_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, command=self.r_scale_changed)
        self.r_scale.pack(side=tk.TOP, fill=tk.X)
        self.g_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, command=self.g_scale_changed)
        self.g_scale.pack(side=tk.TOP, fill=tk.X)
        self.b_scale = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL, command=self.b_scale_changed)
        self.b_scale.pack(side=tk.TOP, fill=tk.X)

        self.color_rectangle_canvas.pack(side=tk.LEFT)

        self.basic_colors_frame.pack(side=tk.TOP, pady=10)  # Ajoute de l'espace entre les carrés de couleur personnalisables et les carrés de couleur de base
        self.custom_colors_frame.pack(side=tk.TOP, pady=10)  # Ajoute de l'espace entre la palette de couleurs et les carrés de couleur personnalisables

        self.button_frame = tk.Frame(self)
        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.ok_clicked)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_clicked)
        self.ok_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        self.button_frame.pack(side=tk.TOP, pady=10)

        self.selected_color = None

        self.transient()

    def open(self):
        self.wait_visibility()
        self.grab_set() 
        self.wait_window()

    def get_color(self):
        return self.selected_color

    def draw_color_rectangle(self, width, height):
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        for i in range(width):
            for j in range(height):
                h = (i / width) * 0.5
                s = 1
                v = 1 - j / height
                color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))
                draw.point((i, j), fill=color)
        return image

    def set_rgb_display(self, r, g, b):
        self.rgb_display.config(text="R: {}, G: {}, B: {}".format(r,g,b))

    def set_color_display(self, r, g, b):
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.color_display.config(bg=color)

    def r_scale_changed(self, value):
        r = int(value)
        g = self.g_scale.get()
        b = self.b_scale.get()
        self.set_rgb_display(r, g, b)
        self.set_color_display(r, g, b)

    def g_scale_changed(self, value):
        r = self.r_scale.get()
        g = int(value)
        b = self.b_scale.get()
        self.set_rgb_display(r, g, b)
        self.set_color_display(r, g, b)

    def b_scale_changed(self, value):
        r = self.r_scale.get()
        g = self.g_scale.get()
        b = int(value)
        self.set_rgb_display(r, g, b)
        self.set_color_display(r, g, b)

    def color_selected(self, event):
        r, g, b = self.color_rectangle_image.getpixel((event.x, event.y))
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.color_display.config(bg=color)
        self.rgb_display.config(text="R: {}, G: {}, B: {}".format(r,g,b))
        self.r_scale.set(r)
        self.g_scale.set(g)
        self.b_scale.set(b)
        self.selected_color = f'#{r:02x}{g:02x}{b:02x}'
        if self.custom_color_selected_label is not None:
            self.custom_color_selected_label.config(bg=color)

    def basic_color_selected(self, event):
        color = event.widget.cget('bg')
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        self.color_display.config(bg=color)
        self.rgb_display.config(text="R: {}, G: {}, B: {}".format(r,g,b))
        self.r_scale.set(r)
        self.g_scale.set(g)
        self.b_scale.set(b)
        self.selected_color = color
        if self.custom_color_selected_label is not None:
            self.custom_color_selected_label.config(bg=color)

    def custom_color_selected(self, event):
        self.custom_color_selected_label = event.widget

    def ok_clicked(self):
        self.destroy()

    def cancel_clicked(self):
        self.destroy()
        self.selected_color = None