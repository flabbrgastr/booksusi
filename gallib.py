# gallib.py
import re
import os
import glob
from collections import defaultdict
import pandas as pd
from bs4 import BeautifulSoup as soup  # HTML data structure

def clean_files(dir_path, test_mode=False):
    # Get list of files in the directory
    files = glob.glob(os.path.join(dir_path, '*.tar.gz'))
    dfiles=0
    # Group files by date
    files_by_date = defaultdict(list)
    for file in files:
        date, time = os.path.basename(file).split('_')
        time = time.split('.')[0]  # remove .tar.gz
        files_by_date[date].append((time, file))

    # For each date, keep only the file with the latest time
    for date, files in files_by_date.items():
        # Sort files by time
        files.sort(reverse=True)
        # Keep only the file with the latest time
        for time, file in files[1:]:
            if test_mode:
                print(f'Would delete: {file}')
            else:
                dfiles+=1   # count deleted files
                os.remove(file)  # delete file

        if test_mode:
            print(f'Would keep: {files[0][1]}')
    return dfiles



def getlastdir(dir_path):
    # Get the directories in dir_path
    directories = [directory for directory in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, directory))]
    # Compile the regular expression pattern
    pattern = re.compile(r'.*\d+\.html')
    # Sort the directories based on their names
    sorted_directories = sorted(directories, reverse=True)

    if sorted_directories:
        # Get the latest directory
        latest_directory = sorted_directories[0]

        # Get the path to the latest directory
        latest_directory_path = os.path.join(dir_path, latest_directory)
    return latest_directory_path



def ex_names(dir_path):

    pattern = r'^(.*?)\d+\.html$'  # Regular expression pattern to match NAME NUMBER.html format

    filenames = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            match = re.match(pattern, filename)
            if match:
                filenames.append(match.group(1))
    # Sort the filenames alphabetically
    filenames.sort()

    # Remove duplicates while preserving the order
    filenames = list(dict.fromkeys(filenames))

#    print(filenames)
    return filenames

def cat_files(dir_path, name, remove=True):
    concatenated_files = 0  # Counter for concatenated files
    concatenated_content = ""
    for filename in os.listdir(dir_path):
        if filename.startswith(name):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                concatenated_content += content
                if remove:
                    #print('remove ' + file_path)
                    os.remove(file_path)

            concatenated_files += 1

    output_file_path = dir_path + '/' + f"{name}.html"
    with open(output_file_path, 'w') as output_file:
        output_file.write(concatenated_content)
        output_file.close()

    return concatenated_files

def get_gals(dir_path, category, test=False):
    dftmp = pd.DataFrame(columns=['Girl', 'Tel', 'Short',
                               'Bezirk', 'Stadt', 'Strasse', 'Fans',
                               'Gurl', 'Purl', 'a1', 'a0', 'cim', 'cof','t'])
    f = category + '.html'
    fh = check_file_exists(dir_path+'/'+f)
    if fh: 
        print('   ✓ '+f)
    else: 
        print('   x '+f)

"""
    with open(dir_path+'/'+f, 'r') as file:
      #print(f,end='.', flush=True)
      tmp = getGals(file.read(),  # file
        True,            # service args
        True,
        True,
        True)
"""

def getGals(content, a1=True, a0=True, cim=True, cof=True):
    #pri
    print('getGals')
    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    # only input is content
    tmp = []
    page_soup = soup(content, "html.parser")

    wrap_container = page_soup.find(
        "div", {"class": "container", "id": "wrap"})
    girls = page_soup.findAll(
        "div", {"class": "girl-list-item", "data-type": "listing"})


def check_file_exists(filename):
    try:
        # Try to open the file
        file_handle = open(filename, 'r')
        # File exists, return the file handle
        return file_handle

    except FileNotFoundError:
        # File doesn't exist, handle the case
        print(f"The file {filename} does not exist!")
        return None

def findhtmls(dir):
    htmls = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".html"):
                # Check if the file name contains no numbers
                if not any(char.isdigit() for char in file):
                    htmls.append(file)
    return htmls
