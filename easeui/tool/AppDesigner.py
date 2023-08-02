import tkinter
from HighlightedText import HighlightedText
from ColorPicker import ColorPicker
from PIL import Image, ImageTk
from tkinter import filedialog

class CodeEditor:
    def __init__(self, root, button, initial_code, callback):
        self.root = root
        self.button = button
        self.initial_code = initial_code
        self.editable_code_v = ""
        self.callback = callback
        self.editor_window = tkinter.Toplevel(self.root)
        self.editor_window.title("Code Editor")
        self.editor_window.resizable(False, False)

        self.non_editable_code = tkinter.Text(self.editor_window, height=1)
        self.non_editable_code.insert("end", "def button_action():")
        self.non_editable_code.config(state="disabled")  # Rendre le widget non éditable
        self.non_editable_code.pack()

        self.editable_code = HighlightedText(self.editor_window)
        self.editable_code.insert("end", self.initial_code)
        self.editable_code.pack()
        self.editable_code.bind("<KeyRelease>", self.editable_code.highlight)

        apply_button = tkinter.Button(self.editor_window, text="Appliquer", command=self.apply_and_close)
        apply_button.pack(side="left")

        cancel_button = tkinter.Button(self.editor_window, text="Annuler", command=self.editor_window.destroy)
        cancel_button.pack(side="right")

    def apply_code(self):
        # Récupérer le code éditable

        editable_code = self.editable_code.get("1.0", "end").strip()
        self.editable_code_v = editable_code

        # Ajouter deux indentations (8 espaces) à chaque ligne du code éditable qui n'est pas vide
        indented_editable_code = "\n".join("    " + line if line.strip() else line for line in editable_code.split("\n"))

        # Concaténer le code non éditable et le code éditable
        self.code = self.non_editable_code.get("1.0", "end") + "\n" + indented_editable_code

        # Créer une fonction qui exécute le code
        exec_env = {}
        try:
            exec(self.code, exec_env)
        except SyntaxError as e:
            print(f"Erreur de syntaxe dans le code :\n{self.code}")
            raise e

        button_action = exec_env.get('button_action')
        if button_action is not None:
            # Assigner cette fonction comme commande pour le bouton
            self.button.config(command=button_action)
        else:
            print("Erreur : La fonction 'button_action' n'a pas été définie dans le code.")

    def get_code(self):
        return self.editable_code_v

    def apply_and_close(self):
        try:
            self.apply_code()
            self.editor_window.destroy()
            self.callback()
        except SyntaxError as e:
            tkinter.messagebox.showerror("Erreur de syntaxe", str(e))

class AppDesigner:
    def __init__(self, master=None):
        self.root = tkinter.Tk() if master is None else master
        self.root.title("AppDesigner - Your app")
        self.root.geometry("909x474")
        self.widgets = []
        self.Menus = []
        self.buttons = []
        self.codes_edit = {}

        self.root.bind("<Button-3>", self.show_add_widget_menu)

        menu = tkinter.Menu(self.root)
        menu_root = tkinter.Menu(menu, tearoff=0)
        menu_gen = tkinter.Menu(menu, tearoff=0)
        self.root.config(menu=menu)

        menu.add_cascade(label="Générer le code", menu=menu_gen)
        menu.add_cascade(label="Modifier la fenetre", menu=menu_root)
        menu.add_command(label=" | ")
        menu.add_command(label="Nouveau Menu", command=self.create_menu)

        menu_gen.add_command(label="avec tkinter & pillow", command=lambda: self.generate_code("tkinter & pillow"))
        menu_gen.add_command(label="avec easeui", command=lambda: self.generate_code("easeui"))

        menu_root.add_command(label="Renommer l'app", command=self.renamme_app)
        menu_root.add_command(label="Redimensionner", command=self.open_resize_window)
        menu_root.add_command(label="Changer le fond", command=self.change_background)

        try:
            menu_root.delete("Enlever le fond")
        except tkinter.TclError:
            pass

        if hasattr(self, 'background_label'):
            menu_root.add_command(label="Enlever le fond", state='normal', command=self.remove_background)
        else:
            menu_root.add_command(label="Enlever le fond", state='disabled', command=self.remove_background)

    def show_add_widget_menu(self, event):
        self.add_widget_menu = tkinter.Menu(self.root, tearoff=0)
        create_menu = tkinter.Menu(self.add_widget_menu, tearoff=0)
        move = tkinter.Menu(self.add_widget_menu, tearoff=0)
        change_bg = tkinter.Menu(self.add_widget_menu, tearoff=0)

        try:
            self.add_widget_menu.delete("Enlever le fond")
        except tkinter.TclError:
            pass

        self.menu_x = event.x_root - self.root.winfo_rootx()
        self.menu_y = event.y_root - self.root.winfo_rooty()

        self.add_widget_menu.add_cascade(label="Créer..", menu=create_menu)
        self.add_widget_menu.add_cascade(label="Déplacer..", menu=move)
        self.add_widget_menu.add_separator()
        self.add_widget_menu.add_command(label="Redimensionner", command=self.open_resize_window)
        self.add_widget_menu.add_cascade(label="Changer le fond", menu=change_bg)

        change_bg.add_command(label="choisir une couleur", command=self.change_background_color)
        change_bg.add_command(label="choisir une image", command=self.change_background)

        if hasattr(self, 'background_label'):
            self.add_widget_menu.add_command(label="Enlever le fond", state='normal', command=self.remove_background)
        else:
            self.add_widget_menu.add_command(label="Enlever le fond", state='disabled', command=self.remove_background)

        create_menu.add_command(label="Label", command=lambda e=event: self.add_label(e))
        create_menu.add_command(label="Button", command=lambda e=event: self.add_button(e))
        create_menu.add_command(label="Image", command=lambda e=event: self.add_image(e))
        create_menu.add_command(label="CheckButton", command=lambda e=event: self.add_checkbutton(e))
        create_menu.add_command(label="Entry", command=lambda e=event: self.add_entry(e))
        for widget_type, text, widget in self.widgets:
            move.add_command(label=text, command=lambda: self.move_widget(widget))
        self.add_widget_menu.tk_popup(event.x_root, event.y_root)

    def show_widget_options_menu(self, event):
        self.widget_options_menu = tkinter.Menu(self.root, tearoff=0)
        self.widget_options_menu.add_command(label="Renommer", command=lambda: self.change_label(event.widget))

        if event.widget.winfo_class() == 'Button':
            self.widget_options_menu.add_command(label="Definir une action", command=lambda: self.add_action(event.widget))
            self.widget_options_menu.add_command(label="Changer le skin", command=lambda: self.change_skin(event.widget))
        
        self.widget_options_menu.add_command(label="Redimensionner", command=lambda: self.open_resize_widget(event.widget))

        self.widget_options_menu.add_command(label="Supprimer", command=lambda: self.delete_widget(event.widget))
        self.widget_options_menu.tk_popup(event.x_root, event.y_root)

    def create_menu(self):
        pass

    def select_file(self, title):
        return filedialog.askopenfilename(title=title, filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])

    def create_image(self, image_path):
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image)

    def create_widget(self, widget_type, text):
        widget = widget_type(self.root, text=text)
        widget.place(x=self.menu_x, y=self.menu_y)
        widget.bind("<Button-3>", self.show_widget_options_menu)
        self.widgets.append((widget_type.__name__, text, widget))
        if widget_type.__name__ == "Button":
            self.buttons.append(widget)
            self.codes_edit[widget] = ""
        return widget

    def move_widget(self, widget):
        widget.place_forget()
        widget.place(x=self.menu_x, y=self.menu_y)

    def change_skin(self, widget):
        image_path = self.select_file("Changer le skin")
        if image_path:
            photo = self.create_image(image_path)
            for i in range(len(self.widgets)):
                if self.widgets[i][2] == widget:
                    self.widgets[i] = (self.widgets[i][0], "Button: " + str(image_path), widget)
            widget.config(image=photo, bd=0)
            widget.image = photo

    def remove_background(self):
        if hasattr(self, 'background_label'):
            self.background_label.destroy()
            del self.background_label

    def change_background(self):
        image_path = self.select_file("Changer le fond")
        if image_path:
            self.remove_background()
            photo = self.create_image(image_path)
            self.background_label = tkinter.Label(self.root, image=photo)
            self.background_label.image = photo
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.lower()

    def change_background_color(self):
        colorpicker = ColorPicker()
        colorpicker.open()
        self.root.config(bg=colorpicker.get_color())

    def add_label(self, event):
        self.create_widget(tkinter.Label, 'Nouveau Label')

    def add_button(self, event):
        self.create_widget(tkinter.Button, 'Nouveau Bouton')

    def add_image(self, event):
        image_path = self.select_file("Ajouter une image")
        if image_path:
            photo = self.create_image(image_path)
            image_label = tkinter.Label(self.root, image=photo)
            image_label.image = photo
            image_label.place(x=event.x, y=event.y, relwidth=1, relheight=1)
            image_label.bind("<Button-3>", self.show_widget_options_menu)
            self.widgets.append(('Image', 'Image: ' + str(image_path), image_label))

    def add_checkbutton(self, event):
        self.create_widget(tkinter.Checkbutton, 'Nouveau CheckButton')

    def add_entry(self, event):
        self.create_widget(tkinter.Entry, 'Nouveau Entry')

    def delete_widget(self, widget):
        self.widgets = [(type, text, w) for (type, text, w) in self.widgets if w != widget]
        if widget.winfo_class() == 'Button':
            self.buttons.remove(self.buttons[self.buttons.index(widget)])
        widget.destroy()

    def open_resize_dialog(self, title, target, widget=None, width=None, height=None):
        self.resize_window = tkinter.Toplevel(self.root)
        self.resize_window.resizable(False, False)
        self.resize_window.title(title)

        if target == "window" or target == "widget":
            self.new_width_var = tkinter.StringVar(value=width)
            self.new_height_var = tkinter.StringVar(value=height)

            tkinter.Label(self.resize_window, text="Nouvelle largeur :").pack()
            tkinter.Entry(self.resize_window, textvariable=self.new_width_var).pack()

            tkinter.Label(self.resize_window, text="Nouvelle hauteur :").pack()
            tkinter.Entry(self.resize_window, textvariable=self.new_height_var).pack()

        elif target == "appname":
            self.new_appname_var = tkinter.StringVar(value=(self.root.title())[14:])

            tkinter.Label(self.resize_window, text="Nouveau nom de l'application :").pack()
            tkinter.Entry(self.resize_window, textvariable=self.new_appname_var).pack()

        elif target == "widgetname":
            self.new_widgetname_var = tkinter.StringVar(value=widget["text"])

            tkinter.Label(self.resize_window, text="Nouveau nom du widget :").pack()
            tkinter.Entry(self.resize_window, textvariable=self.new_widgetname_var).pack()

        apply_button = tkinter.Button(self.resize_window, text="Appliquer")
        apply_button.pack(side="left")
        cancel_button = tkinter.Button(self.resize_window, text="Annuler", command=self.resize_window.destroy)
        cancel_button.pack(side="right")

        if target == "window":
            apply_button.config(command=self.apply_new_size)
        elif target == "widget":
            apply_button.config(command=lambda: self.apply_new_size_w(target))
        elif target == "appname":
            apply_button.config(command=self.apply_new_appname)
        elif target == "widgetname":
            apply_button.config(command=lambda: self.apply_new_widgetname(widget))

    def apply_new_widgetname(self, widget):
        new_widgetname = self.new_widgetname_var.get()
        widget.config(text=new_widgetname)
        for i in range(len(self.widgets)):
            if self.widgets[i][2] == widget:
                self.widgets[i] = (self.widgets[i][0], new_widgetname, widget)
        self.resize_window.destroy()

    def apply_new_appname(self):
        new_appname = self.new_appname_var.get()
        self.root.title("AppDesigner - " + str(new_appname))
        self.resize_window.destroy()

    def open_resize_window(self):
        self.open_resize_dialog("Changer la taille de la fenêtre", "window", self.root.winfo_width(), self.root.winfo_height())

    def open_resize_widget(self, widget):
        self.open_resize_dialog("Changer la taille du widget", "widget", widget, widget.winfo_width(), widget.winfo_height())

    def renamme_app(self):
        self.open_resize_dialog("Changer le nom de l'application","appname")

    def change_label(self, widget):
        self.open_resize_dialog("Changer le nom du widget","widgetname", widget)

    def validate_dimensions(self, width_str, height_str):
        if not width_str or not height_str:
            print("Error: Width and height must not be empty")
            return None, None

        try:
            width = int(width_str)
            height = int(height_str)
        except ValueError:
            print("Error: Width and height must be integers")
            return None, None

        return width, height

    def apply_new_size(self):
        new_width, new_height = self.validate_dimensions(self.new_width_var.get(), self.new_height_var.get())

        if new_width is not None and new_height is not None:
            self.root.geometry(f"{new_width}x{new_height}")
            self.root.resizable(False, False)
            self.resize_window.destroy()

    def apply_new_size_w(self, widget):
        new_width, new_height = self.validate_dimensions(self.new_width_var.get(), self.new_height_var.get())

        if new_width is not None and new_height is not None:
            widget.place(width=new_width, height=new_height)
            self.resize_window.destroy()

    def add_action(self, widget):
        self.editor = CodeEditor(self.root, widget, self.codes_edit[widget], lambda: self.save_code(widget))

    def save_code(self, widget):
        self.codes_edit[widget] = self.editor.get_code()

    def generate_code_logic(self, module):
        code = []

        if module == "tkinter & pillow":
            code.append('import tkinter')
            code.append(f'\nroot = tkinter.Tk()\nroot.title("{(self.root.title())[14:]}")\nroot.geometry("{self.root.winfo_width()}x{self.root.winfo_height()}")\n')

            image_c = 0
            for widget_type, text, widget in self.widgets:
                if widget_type == 'Label':
                    code.append(f'tkinter.Label(root, text="{text}").place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                elif widget_type == 'Button':
                    code.append(f'tkinter.Button(root, text="{text}").place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                elif widget_type == 'Image':
                    image_c += 1
                    code.append(f'photo = ImageTk.PhotoImage(Image.open("{text}"))')
                    code.append('image_label = tkinter.Label(self.root, image=photo)')
                    code.append('image_label.image = photo')
                    code.append(f'image_label.place(x={widget.winfo_x()}, y={widget.winfo_y()})')

                    if image_c == 1:
                        code.insert(1, 'from PIL import Image, ImageTK')

            code.append('\nroot.mainloop()')
            return '\n'.join(code)
        else:
            code.append(f'import easeui\n\nroot = easeui.Window()\nroot.title("{(self.root.title())[14:]}")\nroot.geometry("{self.root.winfo_width()}x{self.root.winfo_height()}")\n')

            button_count = 0
            for widget_type, text, widget in self.widgets:
                if widget_type == 'Label':
                    code.append(f'easeui.Label(root, text="{text}").place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                elif widget_type == 'Button':
                    button_count += 1
                    code.append(f'button_{button_count} = easeui.Button(root, text="{text}")\nbutton_{button_count}.place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                    code_button = self.codes_edit[widget]
                    code_button = "\n".join("    " + line if line.strip() else line for line in code_button.split("\n"))
                    code.append(f'\ndef abutton_{button_count}():\n{code_button}\n\nbutton_{button_count}.config(command=abutton_{button_count})')
                elif widget_type == 'Image':
                    code.append(f'easeui.Image(root, "{text}").place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                elif widget_type == 'Entry':
                    code.append(f'easeui.Entry(root).place(x={widget.winfo_x()}, y={widget.winfo_y()})')
                elif widget_type == 'CheckButton':
                    code.append(f'easeui.CheckButton(root, text="{text}").place(x={widget.winfo_x()}, y={widget.winfo_y()})')

            code.append('\nroot.run()')
            return '\n'.join(code)

    def generate_code(self, module):
        code = self.generate_code_logic(module)  # Suppose this method returns the generated code

        # Create a new window
        new_window = tkinter.Toplevel(self.root)
        new_window.resizable(False, False)
        new_window.grid_columnconfigure(0, weight=1)  # Allow column to stretch with window
        new_window.grid_rowconfigure(0, weight=1)  # Allow row to stretch with window

        # Create a Text widget and set its value to the generated code
        text = tkinter.Text(new_window)
        text.insert(tkinter.END, code)
        text.grid(row=0, column=0, sticky="nsew")  # Make text widget stretch with window

        # Create a Scrollbar and associate it with the Text widget
        scrollbar = tkinter.Scrollbar(new_window, command=text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        text['yscrollcommand'] = scrollbar.set

        # Create a button that copies the code to the clipboard when clicked
        copy_button = tkinter.Button(new_window, text="Copy to clipboard", command=lambda: self.copy_to_clipboard(text.get("1.0", tkinter.END)))
        copy_button.grid(row=1, column=0)

    def copy_to_clipboard(self, text):
        # Clear the clipboard
        self.root.clipboard_clear()
        # Copy text to clipboard
        self.root.clipboard_append(text)

def start():
    designer = AppDesigner()
    designer.root.mainloop()

start()