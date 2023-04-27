import re
import os
import shutil

import string

import pandas as pd
import numpy as np

class PhenixExperiment():
    # Regex used to extract the metadata from file names
    phenix_regex = r"r([0-9]+)c([0-9]+)f([0-9]+)p([0-9]+)-ch([0-9]+)sk([0-9]+)fk1fl1.tiff"

    def __init__(self,experiment_directory):
        self.experiment_directory = experiment_directory

        # Get the last folder, and then trim off the Phenix annotated portion of the name
        self.exp_title = self.experiment_directory.split("/")[-1].split("__")[0]

        self.layout_directory = f"{self.experiment_directory}/AssayLayout"
        self.images_directory = f"{self.experiment_directory}/Images"
        self.grouped_directory = f"{self.experiment_directory}/grouped"

        # TODO: Order is critical here, maybe find a way to decouple?
        self.metadata = self.get_experiment_metadata()
        self.experiment_description = self.describe_exp()
        self.plate_layout = self.get_layout()

    def __str__(self):
        return self.experiment_description

    def get_experiment_metadata(self):
        """ Extracts metadata from filenames of image list"""
        imgs = self.load_phenix_imgs()

        # TODO: is this necessary to make a named column?
        filenames =  pd.DataFrame(imgs,columns=["filename"])

        # Metadata columns to extract into
        metadata_cols = ["row","col","field","zpos","ch","time"]

        # Use extract for the capture groups NOT split!
        metadata = filenames["filename"].str.extract(self.phenix_regex,expand=True).astype(int)
        metadata.columns = metadata_cols

        metadata["filename"] = filenames
        metadata["well"] = metadata.apply(lambda x: self.rc_to_well(x["row"],x["col"]),axis=1)
        metadata["row_letter"] = metadata["well"].str[0]

        # Experiment Info initialized to zero, probably better way of doing this
        metadata["cell"] = None
        metadata["media"] = None
        metadata["coating"] = None

        return metadata

    def get_layout(self):
        '''Returns a text visual of the plate layout. '''
        # Eventually we want svg/html interactive graphics, REQUIRES metadata to be generated

        # TODO: generalize
        wells = 384 # based on plate type, need to make generalizable
        rows = 16
        cols = 24

        # To allow for printing and visualizing of full plate
        pd.set_option('display.max_columns', cols)
        pd.set_option('display.max_rows', rows)

        column_names = list(range(1,cols+1))
        row_names = list(string.ascii_uppercase)[:rows]

        # Generate an empty array of the plate size
        zero_plate = np.zeros(shape=(rows,cols))
        # Give row names
        layout = pd.DataFrame(zero_plate,index=row_names,columns=column_names).replace(0,"-")

        # TODO: make generalizable
        # Fill in dead rows with X, not every plate has dead rows
        dead_rows = layout.index.isin(["A","B","O","P"])
        layout[dead_rows] = " "

        # Fill in dead cols with X
        layout[[1,2,23,24]] = " "
        for name,data in self.metadata.groupby(["row_letter","col"]):
            row,col = name

            # If row,col exists in experiment, fill in the blank plate
            layout.loc[row,col] = "O"

        return layout

    # TODO: this feels off, generalize this (?), maybe refactor somewhere...
    def rc_to_well(self,row,col):
        '''Translates row,col coordinates to well'''
        rows = 16
        cols = 24
        row_letters = [s for s in string.ascii_uppercase[0:rows]]
        letter = row_letters[row-1]
        well = f"{letter}{col}"
        return well

    def describe_exp(self):
        self.channels = self.metadata["ch"].max()
        self.timepoints = self.metadata["time"].max()
        self.wells = len(self.metadata["well"].unique())
        self.fields = self.metadata["field"].max()
        self.slices = self.metadata["zpos"].max()
        self.total_imgs = len(self.metadata)

        description = (f"Experiment: {self.exp_title}\n"
                        f"Channels: {self.channels}\n"
                        f"Fields: {self.fields}\n"
                        f"Timepoints: {self.timepoints}\n"
                        f"Wells: {self.wells}\n"
                        f"Z slices: {self.slices}\n"
                        f"Total Images: {self.total_imgs} 🙃")
        return description

    def load_phenix_imgs(self):
        """ Reads in an experiment directory and loads image names into memory"""
        top_level = [f for f in os.listdir(self.experiment_directory)]
        imgs = [i for i in os.listdir(self.images_directory) if not i.startswith(".") and i.endswith(".tiff")]
        return imgs

def test():
    test_dir = "/Volumes/the_box/phenix/04-05 crawling__2023-04-05T11_32_49-Measurement 1"
    test_exp = PhenixExperiment(test_dir)
    print(test_exp)

if __name__ == "__main__":

    test()

