from phenix_experiment import PhenixExperiment

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

def load_exp():
    exp_dir = filedialog.askdirectory()
    exp = PhenixExperiment(exp_dir)
    exp_frame = ttk.Frame(master=root).grid()
    title_label = ttk.Label(master=exp_frame,text=exp.exp_title).grid()

if __name__ == "__main__":
    running = True
    root = Tk()
    frame = ttk.Frame(master=root).grid()
    dir_button = ttk.Button(master=root,text="Choose experiment dir...",command=load_exp).grid()


    while running:
        root.update_idletasks()
        root.update()
