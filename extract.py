import os
import shutil
import sys

def extract(movies_dir,dry_run=True):
    cam_dirs = [f"{movies_dir}/{f}" for f in os.listdir(movies_dir)]
    new_csv_dir = f"{movies_dir}/csvs"
    new_roi_dir = f"{movies_dir}/rois"

    if not os.path.exists(new_csv_dir):
        os.mkdir(new_csv_dir)
    if not os.path.exists(new_roi_dir):
        os.mkdir(new_roi_dir)

    for cam_dir in cam_dirs:
        gfp_dirs = [f"{cam_dir}/{f}" for f in os.listdir(cam_dir)]
        for gfp_dir in gfp_dirs:
            csv_dir = f"{gfp_dir}/csvs"
            roi_dir = f"{gfp_dir}/rois"
            files = [f for f in os.listdir(gfp_dir) if not f in
                     ["rois","csvs"] and not f.startswith(".")]
            old_files = [f"{gfp_dir}/{f}" for f in files]
            new_files = [f"{cam_dir}/{f}" for f in files]

            csvs = [f for f in os.listdir(csv_dir)]
            new_csvs = [f"{new_csv_dir}/{c}" for c in csvs]
            old_csvs = [f"{csv_dir}/{c}" for c in csvs]

            rois = [f for f in os.listdir(roi_dir)]
            new_rois = [f"{new_roi_dir}/{r}"  for r in rois]
            old_rois = [f"{roi_dir}/{r}"  for r in rois]

            zipped = [zip(old_csvs,new_csvs),zip(old_rois,new_rois),zip(old_files,new_files)]
            names = ["csvs","rois","files"]
            for i,z in enumerate(zipped):
                print(names[i])
                for old,new in z:
                    if(dry_run):
                        print(old)
                        print(new)
                    else:
                        shutil.move(old,new)
    


if __name__ == "__main__":
    if len(sys.argv) ==2:
        _,movies_dir = sys.argv
        extract(movies_dir,dry_run=False)

