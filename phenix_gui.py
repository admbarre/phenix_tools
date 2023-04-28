from phenix_experiment import PhenixExperiment

from tkinter import *
from tkinter import filedialog
from tkinter import ttk

class PhenixGui:
    def __init__(self):
        # Initialize the variable to none and assign later, is this best practice?
        self.experiment = None
        self.root = Tk()
        self.frame = ttk.Frame(master=self.root)
        self.frame.grid(column=0,row=0,sticky=(N,W,E,S))

        self.dir_button = ttk.Button(master=self.frame, text = "Choose experiment...", command = self.load_experiment)
        self.dir_button.grid()

        # Main loop
        self.root.mainloop()


    def load_experiment(self):
        exp_dir = filedialog.askdirectory(title="test..?")
        self.experiment = PhenixExperiment(exp_dir)
        print(self.experiment)

if __name__ == "__main__":
    gui = PhenixGui()
