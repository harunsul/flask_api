import tkinter as tk
from main import *
from test import show_songs, increase_plays


def button_func(text_widget):
    return show_songs()

def button_func2(text_widget):
    return increase_plays(1)

class Songapi(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(1200, 300)
        Songframe().pack()

class Songframe(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        label = tk.Label(self, text="YT API", font=("Verdana", 10)).pack(pady=10, padx=10)
        text_widget = tk.Listbox(self, height=10, width=180)
       

        def pack_1():  
            get_data = button_func(text_widget)
            text_widget.insert(tk.END, str(get_data))
            text_widget.pack()

        def pack_2():  
            get_data = button_func2(text_widget)
            text_widget.insert(tk.END, str(get_data))
            text_widget.pack()

        button = tk.Button(self, text="Get 10 Songs", command= lambda: pack_1()).pack()
        button2 = tk.Button(self, text="Increase plays on Song 2", command= lambda: pack_2()).pack()

        
Songapi().mainloop()