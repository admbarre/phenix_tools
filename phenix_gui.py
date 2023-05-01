from phenix_experiment import PhenixExperiment

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class PhenixGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.running = True
        self.wm_title("Phenix Experiment")
        self.container = ttk.Frame(self,height=480,width=640).grid()
        self.start = StartPage(self.container,self).grid()
        self.protocol("WM_DELETE_WINDOW",self.close)

    def close(self):
        self.running = False
        self.destroy()

    def load_exp(self):
        self.exp_dir = filedialog.askdirectory()
        self.exp = PhenixExperiment(exp_dir)
        exp_frame = ttk.Frame(master=root).grid()
        title_label = ttk.Label(master=exp_frame,text=exp.exp_title).grid()

class StartPage(ttk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.label = ttk.Label(self,text="Start Page").grid(sticky=(tk.N))
        self.dir_button = ttk.Button(self,text="Choose experiment dir...",command=lambda: print("yo")).grid(sticky=(tk.N))


if __name__ == "__main__":
    gui = PhenixGUI()
    while gui.running:
        gui.update_idletasks()
        gui.update()
