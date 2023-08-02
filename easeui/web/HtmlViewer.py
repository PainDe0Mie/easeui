from tkinter import *
#from PIL import Image, ImageTk
#from bs4 import BeautifulSoup
#import requests, io
from tkhtmlview import HTMLLabel

class HtmlViewer:
    def __init__(self, root, html, url=None):
        self.html = html
        self.url = url
        self.root = root.root
        self.images = []  # List to hold the images

    def render(self):

        print("Using tkhtmlview for the moment.")
        html_label = HTMLLabel(self.root, html=self.html)
        html_label.pack(fill="both", expand=True)

        """
        # Create a BeautifulSoup object
        soup = BeautifulSoup(self.html, 'html.parser')

        # Create a main Frame
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=1)

        # Create a Canvas inside the main Frame
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add a Scrollbar to the Canvas
        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the Canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another Frame inside the Canvas
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Go through all elements of HTML
        for tag in ['h1', 'h2', 'p', 'a', 'img', 'ul', 'ol', 'input', 'button']:
            for element in soup.find_all(tag):
                widget = None
                font_size = 12
                style_kwargs = {}

                style = element.get('style')
                if style:
                    style_dict = dict(item.split(":") for item in style.split(";") if item)
                    if 'color' in style_dict:
                        style_kwargs['fg'] = style_dict['color'].strip()
                    if 'background-color' in style_dict:
                        style_kwargs['bg'] = style_dict['background-color'].strip()
                    if 'font-size' in style_dict:
                        font_size_str = style_dict['font-size'].strip()
                        if 'px' in font_size_str:
                         font_size = int(font_size_str.replace('px', ''))
                        elif 'pt' in font_size_str:
                            # 1 point is approximately 1.33 pixels
                            font_size = int(float(font_size_str.replace('pt', '')) * 1.33)
                        else:
                            # default font size if no valid unit found
                            font_size = 12
                        style_kwargs['font'] = ('Arial', font_size)

                # Create widgets based on HTML tags
                if element.name in ['h1', 'h2', 'p', 'a']:
                    widget = Label(frame, text=element.get_text(), **style_kwargs)
                    if element.name == 'a':
                        widget.config(fg="blue", cursor="hand2")
                        widget.bind("<Button-1>", lambda e, url=element.get('href'): self.open_link(url))
                elif element.name == 'img':
                    try:
                        try:
                            response = requests.get(self.url + element.get('src'))
                        except:
                            response = requests.get(element.get('src'))
                        image = Image.open(io.BytesIO(response.content))
                        photo = ImageTk.PhotoImage(image)
                        widget = Label(frame, image=photo, **style_kwargs)
                        widget.image = photo
                        self.images.append(photo)  # Add the photo to the list
                    except:
                        print("Failed to load image")
                        continue
                elif element.name in ['ul', 'ol']:
                    for li in element.find_all('li'):
                        widget = Label(frame, text=li.get_text(), **style_kwargs)
                        widget.pack()
                    continue
                elif element.name == 'input' and element.get('type') in ['search', 'text']:
                    label = Label(frame, text=f"Search Bar (name={element.get('name')}):", **style_kwargs)
                    label.pack()

                    # Create a Entry widget for the search bar
                    search_bar = Entry(frame)
                    search_bar.pack(pady=10)

                    # If the search bar has a placeholder, set it as the Entry widget's default text
                    if element.has_attr('placeholder'):
                        search_bar.insert(0, element['placeholder'])

                    continue
                elif element.name == 'button':
                    widget = Button(frame, text=element.get_text(), **style_kwargs)

                    continue

                if widget is not None:
                    widget.pack(pady=10)  # Adjust the spacing as needed

        """