import customtkinter as ctk

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def get_exp_dir():
    exp_dir = filedialog.askdirectory(title="test..?")

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("640x480")

    dir_button = ctk.CTkButton(master=root, text = "Choose experiment", command = get_exp_dir)
    dir_button.pack()
    root.mainloop()
