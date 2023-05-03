import sys
import os
import shutil

def get_leaves(tree):
    files = [f"{tree}/{f}" for f in os.listdir(tree) if not
             f.startswith(".")]
    leaves = []
    for f in files:
        if os.path.isdir(f):
            leaves = leaves + get_leaves(f)
        else:
            filename = f
            leaves.append(filename)
    return leaves

def flatten(top_level,dry_run=True):
    old_paths = get_leaves(top_level)
    for old in old_paths:
        filename = old.split("/")[-1]
        new = f"{top_level}/{filename}"
        if dry_run:
            print(f"Old: {old}")
            print(f"New: {new}")
        else:
            shutil.move(old,new)
#            cleanup(top_level)

# TODO: putting this on hold because I would have to traverse the tree again
# to make sure it's truly empty. Just going to delete them manually
def cleanup(top_level):
    files = [f"{top_level}/{f}" for f in os.listdir(top_level)]
    print(f"Cleaning up: {top_level}")
    for f in files:
        if os.path.isdir(f):
            dir_files = os.listdir(f)
            if len(dir_files) == 0:
                print(f"Empty dir")
            else:
                print(f"Nonempty dir")
                print(dir_files)
            print(f)
        else:
            pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        _, top_level = sys.argv
        print(f"Flattening {top_level}")
        cleanup(top_level)
        flatten(top_level,dry_run=False)
