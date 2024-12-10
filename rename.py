import os
import sys

def rename_jpgs(out_dir):
    files = [f for f in os.listdir(out_dir) if f.endswith(".jpg") or f.endswith(".jpg?")]
    for file in files:
        new_file = file.replace(".jpg?", "_")
        os.rename(os.path.join(out_dir, file), os.path.join(out_dir, new_file))
    # print("done")  # Uncomment this line if you want to print "done" at the end

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the output directory.")
        sys.exit(1)

    out_dir = sys.argv[1]
    rename_jpgs(out_dir)
