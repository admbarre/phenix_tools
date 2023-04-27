import os
import shutil
import sys

def tidy(tidy_dir,dry_run=True):
    files = [f for f in os.listdir(tidy_dir) if f.endswith(".avi") and not f.startswith(".")]
    for f in files:
        filename,ext = f.split(".")
        cell,gfp,well,field = filename.split("_")

        # TODO: maybe add an argument to decide what level of directories?
        new_dir = f"{tidy_dir}/{cell}"
        new_path = f"{new_dir}/{f}"
        old_path = f"{tidy_dir}/{f}"
        if dry_run:
            print(old_path)
            print(new_path)
        else:
            os.makedirs(os.path.dirname(new_path),exist_ok=True)
            shutil.move(old_path,new_path)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        _,tidy_dir = sys.argv
        dry_run = False if input("Dry run? [y/n]").lower() in ["n","no"] else True
        tidy(tidy_dir,dry_run)
    else:
        print("Usage: python tidy.py <directory path>")


