import os
import random
import shutil
import json

class BlindExp():
    ignore_dirs = ["rois","annotations","csvs","exp_info"]
    def __init__(self,exp_dir):
        # Directories
        self.exp_dir = exp_dir
        self.movies_dir = f"{exp_dir}/movies"
        self.rois_dir = f"{self.movies_dir}/rois"
        self.save_dir = f"{self.movies_dir}/exp_info"
        
        self.random_names = self.init_word_list()
        self.cams = [f for f in os.listdir(self.movies_dir) if f not in self.ignore_dirs]
        # TODO: this needs to be provided, not hardcoded
        self.gfp_names = ["gfp100","gfp300","gfp900","gfp2700","gfp8100","gfp24300","nogfp"]
        self.exp_info = {
            "blinded": False
        }
        
        # Check if this experiment has been initialized before
        if os.path.exists(self.save_dir):
            # Translate dictionary loading
            translate_path = f"{self.save_dir}/translate.json"
            if os.path.exists(translate_path):
                print("Opening existing translation dict...")
                # Opening JSON file
                with open(translate_path) as json_file:
                    self.translate_dict = json.load(json_file)
                    self.scramble_dict = {v:k for k,v in self.translate_dict.items()}

            # Experiment info dictionary loading
            info_path = f"{self.save_dir}/info.json"
            # Opening experiment info
            if os.path.exists(info_path):
                print("Opening existing experiment info dict...")
                with open(info_path) as info:
                    self.exp_info = json.load(info)

        else:
            # Create save dir
            os.mkdir(self.save_dir) 
            
            # Generate and save translation dicts
            self.scramble_dict = self.generate_scramble_dict()
            self.translate_dict = {v:k for k,v in self.scramble_dict.items()}
                        # Save the translated dict to disk
            self.save_dict(self.translate_dict,"translate")
            
            # Generate and save experiment info
            # TODO: expand this to save more info
            self.save_dict(self.exp_info,"info")


    def init_word_list(self):
        with open("neg.txt") as f:
            random_names = [f.strip() for f in f.readlines()]
            #random_names = [f for f in random_names if not f.contains(["-","_"])]
            random.shuffle(random_names)
            return random_names 
        
    def generate_scramble_dict(self):
        num_cams = len(self.cams)
        num_gfp = len(self.gfp_names)

        cam_scramble = self.random_names[:num_cams]
        self.random_names = self.random_names[num_cams:] # shorten the list and remove the used names
        
        gfp_scramble = self.random_names[:num_gfp]
        self.random_names = self.random_names[num_gfp:] # shorten the list and remove the used names
        
        cam_dict = {cam:rand for cam,rand in zip(self.cams,cam_scramble)}
        gfp_dict = {gfp:rand for gfp,rand in zip(self.gfp_names,gfp_scramble)}
        scramble_dict = {}
        scramble_dict.update(cam_dict)
        scramble_dict.update(gfp_dict)
        return scramble_dict
    
    def save_dict(self,dictionary,name): 
        print(f"Saving {name} dictionary to...")
        save_path = f"{self.save_dir}/{name}.json"
        print(save_path)
        # create json object from dictionary
        json_dict = json.dumps(dictionary)
        with open(save_path,"w") as f:
            f.write(json_dict)
            f.close()
            
    def translate_dir(self,directory,command,dry_run=True):
        if command == "blind":
            dictionary = self.scramble_dict
        elif command == "unblind":
            dictionary = self.translate_dict
        else:
            # Not entirely sure how to handle this type of error
            return False
        
        print(f"*** Running {command} on {directory}...")
        for file in os.listdir(directory):
            name,ext = file.split(".")
            #print(name)
            
            cam,gfp,well,field = name.split("_")
            new_cam = dictionary[cam]
            new_gfp = dictionary[gfp]
            new_file = f"{new_cam}_{new_gfp}_{well}_{field}.{ext}"
            old_path = f"{directory}/{file}"
            new_path = f"{directory}/{new_file}"

            if dry_run:
                print(file)
                print(new_file)
            else:
                os.rename(old_path,new_path)
                
    def translate_exp(self,command,dry_run=True):
        # Need to update cams names every translation
        self.cams = [f for f in os.listdir(self.movies_dir) if f not in self.ignore_dirs]
        blinded = self.exp_info["blinded"]
        if command == "blind":
            if blinded == True:
                print("Experiment already blinded")
                return False
            else:
                dictionary = self.scramble_dict
                if not dry_run:
                    self.exp_info["blinded"] = True
        elif command == "unblind":
            if blinded == False:
                print("Experiment is not blinded")
                return False
            else:
                dictionary = self.translate_dict
                if not dry_run:
                    self.exp_info["blinded"] = False
        else:
            # probably a better way of handling this type of error
            return False
            
        # Scramble ROIs
        self.translate_dir(self.rois_dir,command,dry_run)
            
        # Scramble files
        for cam in self.cams:
            cam_dir = f"{self.movies_dir}/{cam}"
            
            # scramble files inside cam folder
            self.translate_dir(cam_dir,command,dry_run)
            
            # scramble cam folder names
            print(f"*** Running {command} on folder names...")
            new_cam = dictionary[cam]
            new_cam_dir = f"{self.movies_dir}/{new_cam}"
            if dry_run:
                print(cam)
                print(new_cam)
            else:
                os.rename(cam_dir,new_cam_dir)
        self.save_dict(self.exp_info,"info")
