import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PieChart(tk.Frame):
    def __init__(self, root, sizes, show_sizes=False, labels=None, title=None):
        super().__init__(root.root)
        self.root = root.root
        self.labels = labels
        self.sizes = sizes
        self.title = title
        self.show_sizes = show_sizes

        # Créer un label avec une image transparente
        self.label = tk.Label(self.root)
        self.label.pack(expand=True)

        # Afficher le camembert sur le label
        self.display_pie_chart()

    def display_pie_chart(self):
        # Créer un camembert
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('none')  # rend le fond de la figure transparent
        ax.axis('off')  # masque les axes

        if self.show_sizes:
            ax.pie(self.sizes, labels=self.labels, autopct='%1.1f%%', startangle=90)
        else:
            ax.pie(self.sizes, labels=self.labels, autopct='', startangle=90)

        if self.title:
            ax.set_title(self.title)

        # Afficher le camembert sur le label
        canvas = FigureCanvasTkAgg(fig, master=self.label)
        canvas.draw()
        canvas.get_tk_widget().pack()