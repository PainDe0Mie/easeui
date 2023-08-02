![Logo](https://i.imgur.com/2eEdAkC.png)

## Installation

Install easeui with pip

```bash
  pip install easeui
```
## Features

- More widgets (PieChart, WebView, ColorPicker..)
- A app for make your app
- A Code Editor for button

## Code

Code your app yourself and enjoy more widgets than tkinter !

```python
import easeui

root = easeui.Window()
root.title("Your app")
root.geometry("909x474")

button_1 = easeui.Button(root, text="Nouveau Bouton")
button_1.place(x=128, y=175)

def abutton_1():
    print("hey !")

button_1.config(command=abutton_1)
easeui.Entry(root).place(x=158, y=287)
easeui.Image(root, image_path="C:/Users/axelr/Downloads/EaseUI__1_-removebg-preview.png").place(x=456, y=24)

root.run()
```

Otherwise you can use AppDesigner !

## Screenshots

#### AppDesigner:

![App Screenshot](https://i.imgur.com/Um9APRH.png)

#### Editor Code:

![App Screenshot2](https://i.imgur.com/ZjV4owx.png)

## Authors

- [PainDe0Mie](https://www.github.com/PainDe0Mie)
           
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
