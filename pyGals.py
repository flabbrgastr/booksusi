import os
import shutil
import subprocess
import sys

# Function to display help information
def show_help():
    print("Usage: getGals [options]")
    print("Options:")
    print("  -h        Display this help information")
    print("  -i        Include images")
    print("  -a        a only")
    print("  -l        local tar storage")
    print("  -f        local folder storage")
    # Add more options and their descriptions as needed

# Check for the --help or -h argument
if "-h" in sys.argv or "--h" in sys.argv:
    show_help()
    sys.exit(0)

# Read options from config file into a dictionary
variables = {}
variables_section = False
with open("gals.conf", "r") as config_file:
    for line in config_file:
        line = line.strip()
        if line == "[variables]":
            variables_section = True
            continue
        if variables_section:
            if line.startswith("#") or not line:
                continue
            key, value = map(str.strip, line.split("=", 1))
            variables[key] = value

# Testmode
if "-t" in sys.argv:
    print("Testmode")
    Testing = 10
    # Print the variables
    for key, value in variables.items():
        print(f"{key}={value}")
else:
    Testing = 0

user = os.getlogin()

# wget args
arg1 = "-e robots=off"
arg2 = "-q -k -K --adjust-extension"
arg3 = "-U mozilla"
if "-i" in sys.argv:
    arg4 = f"-nH -nd -p -H {variables.get('arg4i', '')}"
    print("include images")
else:
    arg4 = "-nH -nd"
arg5 = "--convert-links --random-wait"
args = f"{arg1} {arg2} {arg3} {arg4} {arg5}"

# Check for the -a argument
if "-a" in sys.argv:
    # anal only
    keyword = "an"
    filtered_arr = [option for option in html1arr if keyword in option]
    # Update html1arr with filtered_arr values
    html1arr = filtered_arr

GalsinPage = int(variables.get("GalsinPage", "0"))
html0 = variables.get("html0", "")
html2 = variables.get("html2", "")
datum = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
out_dir = f"./data/{datum}"
arg_out = f"-P{out_dir}"

print(f"Getting Gals on {datum}")
print(html1arr)
print("")

for i in html1arr:
    print(i, end=" ")
    x = 1
    sumGals = 0
    Gals = GalsinPage
    while Gals >= GalsinPage:
        subprocess.run(["wget", args, arg_out, f"{html0}{i}{html2}{x}"])
        file = f"{out_dir}/{i}{x}.html"
        shutil.move(f"{out_dir}/index*{x}.html", file)
        with open(file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if "<body>" in line:
                    f.write(line)
                elif "</body>" in line:
                    f.write(line)
                    break
            f.truncate()
        Gals = sum(1 for _ in re.finditer(r"\blisting\b", open(file).read()))
        Gals -= Testing
        sumGals += Gals
        print(".", end="")
        x += 1

    print(sumGals)

print("cleaning up")
os.chdir(out_dir)
subprocess.run(["rm", "*.orig", "*.svg", "*.css", "*.css?*", "*.js?*", "*.jpg", "*.png", "*.[0-9]", "*.[0-9][0-9]"], stderr=subprocess.DEVNULL)
os.chdir("../..")

# Delete all directories and files older than N days
N = int(variables.get("N", "0"))
for root, dirs, files in os.walk("./data/"):
    for name in dirs:
        path = os.path.join(root, name)
        ctime = os.path.getctime(path)
        if (time.time() - ctime) // (24 * 3600) > N:
            shutil.rmtree(path)

# python booksi_a_42.py d

# Renaming images
subprocess.run(["./renamejpgs.sh", out_dir])
os.chdir("./data/")
print(f"tar {datum}/ to {datum}.tar.gz")
subprocess.run(["tar", "-zcf", f"{datum}.tar.gz", datum])

if "-f" not in sys.argv:  # if not local storage
    shutil.rmtree(datum)  # delete folder to save space on local storage

if Testing != 0:
    print("testmode")
else:
    if "-l" not in sys.argv:
        print("rcloning to gdrive")
        subprocess.run(["rclone", "copy", f"{datum}.tar.gz", "fgdrive:/"])
        os.chdir("..")

print("finished, enjoy!")
sys.exit(0)
