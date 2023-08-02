# debug_window.py
import tkinter, sys, logging
from tkinter import scrolledtext

class DebugWindow:
    def __init__(self, master=None, show_window=True):
        # Vérifier si master est une instance de tkinter.Tk ou tkinter.Toplevel
        if master and not isinstance(master, (tkinter.Tk, tkinter.Toplevel)):
            # Si ce n'est pas le cas, on essaie d'accéder à l'attribut 'root'
            master = getattr(master, 'root', None)
        
        if master:
            self.root = tkinter.Toplevel(master)
        else:
            self.root = tkinter.Tk()

        if not show_window:
            self.root.withdraw()

        self.root.title("Debug Window")
        self.text = scrolledtext.ScrolledText(self.root)
        self.text.pack()

        sys.stderr = self

        self.write(f"Welcome to the debug console.\nAdd logs: easeui.DebugWindow(master).setup_logging()\n\n{'- '*30}")

    def write(self, text):
        self.text.configure(state='normal')
        self.text.insert(tkinter.END, text)
        self.text.configure(state='disabled')

    def flush(self):
        pass

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    def setup_logging(self):
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                msg = self.format(record)
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tkinter.END, msg + '\n')
                self.text_widget.configure(state='disabled')

        handler = TextHandler(self.text)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

    def start(self):
        self.root.mainloop()