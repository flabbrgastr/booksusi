# gallib.py
import re
import os
import glob
from collections import defaultdict
import pandas as pd
from bs4 import BeautifulSoup as soup  # HTML data structure
import shutil
from tqdm import tqdm
import time

def clean_files(dir_path, test_mode=False):
    # Get list of files in the directory
    files = glob.glob(os.path.join(dir_path, '*.tar.gz'))
    dfiles = 0
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
                dfiles += 1   	    # count deleted files
                os.remove(file)     # delete file

        if test_mode:
            print(f'Would keep: {files[0][1]}')
    return dfiles


def clean_dirs(dir_path, test_mode=False):
    # Get list of directories in the path
    directories = [os.path.join(dir_path, d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

    # Sort directories by date (ascending order)
    directories.sort()

    # Keep the last directory and delete the rest
    for directory in directories[:-1]:
        if test_mode:
            print(f'Would delete directory: {directory}')
        else:
            # Remove directory and all its contents recursively
            shutil.rmtree(directory)

    return len(directories[:-1])  # Return the number of deleted directories

def getlastdir(dir_path):
    # Get the directories in dir_path
    directories = [directory for directory in os.listdir(dir_path)
                   if os.path.isdir(os.path.join(dir_path, directory))]
    # Sort the directories based on their names
    sorted_directories = sorted(directories, reverse=True)

    if sorted_directories:
        # Get the latest directory
        latest_directory = sorted_directories[0]

        # Get the path to the latest directory
        latest_directory_path = os.path.join(dir_path, latest_directory)
    return latest_directory_path


def ex_names(dir_path):
    pattern = r'^(.*?)\d+\.html$'  # Regex pattern to match file
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


def cat_files2(dir_path, name, remove=True):
    concatenated_files = 0  # Counter for concatenated files
    concatenated_content = ""
    for filename in os.listdir(dir_path):
        if filename.startswith(name):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                concatenated_content += content
                if remove:
                    os.remove(file_path)
            concatenated_files += 1
    output_file_path = dir_path + '/' + f"{name}.html"
    with open(output_file_path, 'w') as output_file:
        output_file.write(concatenated_content)
        output_file.close()

    return concatenated_files


def cat_files(dir_path, name, remove=True):
    concatenated_files = 0  # Counter for concatenated files
    concatenated_content = ""
    for filename in os.listdir(dir_path):
        if filename.startswith(name):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                sgirls = soup(content, 'html.parser')
                girls = sgirls.find_all("div",
                              {"class": "girl-list-item",
                               "data-type": "listing"})
                for girl in girls:
                    concatenated_content += str(girl)
                if remove:
                    os.remove(file_path)
            concatenated_files += 1
    output_file_path = dir_path + '/' + f"{name}.html"
    with open(output_file_path, 'w') as output_file:
        output_file.write(concatenated_content)
        output_file.close()

    return concatenated_files

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
    for file in os.listdir(dir):
        if file.endswith(".html"):
            # Check if the file name contains no numbers
            if not any(char.isdigit() for char in file):
                htmls.append(file)
    return htmls


def count_occurrences(file, pattern):
    with open(file, 'r') as html_file:
        content = html_file.read()
        occurrences = len(re.findall(pattern, content))
        return occurrences


def get_gals(dir_path, category, test=False):
    left = '</strong>'
    right = '<a'

    f = category
    fh = check_file_exists(dir_path+'/'+f)
    if not fh:
        raise Exception('x', f)

    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    # only input is content
    a0, a1, cim, cof = '', '', '', ''
    if 'analsex' in category:
        a1 = '✓'
    if 'natur' in category:
        a0 = '✓'
    if 'cum_in_mouth' in category:
        cim = '✓'
    if 'cum_on_face' in category:
        cof = '✓'

    tmp = []
    page_soup = soup(fh, "html.parser")

    girls = page_soup.findAll("div",
                              {"class": "girl-list-item",
                               "data-type": "listing"})
    noofgals = len(girls)
    descstr = '   ✓ '+f+': '+str(noofgals)
    #print('   ✓ '+f+': '+str(noofgals))
    # Create a progress bar using tqdm
    progress_bar = tqdm(total=noofgals, desc=descstr, 
                        bar_format="{l_bar}", ncols=80)

    for girl in girls:
        progress_bar.update(1)
        girl_name = girl.find('h4').get_text(strip=True)

        location = girl.find("div", class_="g-location") # find the div element with class 'g-location'
        hrefs = location.find_all("a")
        stadt = hrefs[0].get_text() # get the text of the first element and assign it to stadt
        bezirk = hrefs[1].get_text() # get the text of the second element and assign it to bezirk
        try:
            strasse = hrefs[2].get_text() # get the text of the third element and assign it to 
        except:
            strasse = ''

        try:
            fancount = girl.select_one("span[id*=girl-fancount]").text
        except:
            fancount = 0

        try:
            short_str = girl.find('div', class_='girl-subtitle')
#            short = short_str[short_str.index(
#                              left)+len(left):short_str.index(right)].strip()
#            print(short_str)
#           short is the the part of the string after the first space
            short = short_str.get_text(strip=True, separator=' ')
            # remove the first word
            short = short[short.index(' ')+1:]

        except:
            short = ''
#        exit()

        node = girl.find('a', {'class': 'pull-right'})
        if node is not None:
            tel = node['href']
        else:
            tel = '-'

        #gurl = girl.find('a', href=True)['href']
        h4 = girl.find("h4") # find the h4 element
        gurl = h4.find("a")["href"] # find the a element inside the h4 element and get its 

        node = girl.find('source', srcset=True)
        if node is not None:
            purl = node['srcset']
        else:
            purl = None

        tmp.append({'Girl': girl_name,
                    'Stadt': stadt,
                    'Bezirk': bezirk,
                    'Strasse': strasse,
                    'Fans': fancount,
                    'Short': short,
                    'Tel': tel,
                    'Gurl': gurl,
                    'Purl': purl,
                    'a1': a1,
                    'a0': a0,
                    'cim': cim,
                    'cof': cof,                
                    't':''
                    })
    progress_bar.close()
    return tmp


def dfComprehend(dfnew):
  #sort dfnew
  oldnum=len(dfnew.index)
  print ('    ',+oldnum,'comprehended to ',end='', flush=True)
  dfnew = dfnew.sort_values(by=['Girl'], ascending=True)
  dfnew = dfnew[dfnew["Girl"].str.contains("Trans|trans|TRANS|^ts |TS |^Ts |^Ts_")==False]  # remove trans
  dfnew = dfnew[dfnew["Short"].str.contains("Trans|trans|TRANS|^ts |TS |^Ts |^Ts_")==False]  # remove trans
  dfnew = dfnew.groupby(['Girl', 'Tel'], as_index=False).max()
  newnum=len(dfnew.index)
  percentage = (oldnum - len(dfnew.index)) / oldnum * 100
  print(f"{newnum} -{percentage:.0f}%")
  return dfnew;


def fancy_print(message, level=1):
    if level == 1:
        header = f"=== {message} ==="
        line = "=" * len(header)
    elif level == 2:
        header = f"--- {message} ---"
        line = "-" * len(header)
    else:
        header = f"{message}"

    if level in [1, 2]: print(line)
    print(header)
    if level in [1, 2]: print(line)


def someStats(df):
    # Number of rows that have all four columns checkmarked
    rows_all_checkmarks = df[(df['a1'] == '✓') & (df['a0'] == '✓') & (df['cof'] == '✓') & (df['cim'] == '✓')]
    rows_both_a1_a0 = df[(df['a1'] == '✓') & (df['a0'] == '✓')]
    rows_both_cum = df[(df['cof'] == '✓') & (df['cim'] == '✓')]
    rows_a0_only = df[(df['a1'] != '✓') & (df['a0'] == '✓')]

    # Print the statistics
    fancy_print("TOP10 Supergals                            ✓✓✓✓",level=2)
    print(get_top_10_rows(rows_all_checkmarks,5))
    fancy_print("TOP10 Ass                                  ✓✓??",level=2)
    print(get_top_10_rows(rows_both_a1_a0,5))
    fancy_print("New Ass                                  ✓✓??",level=2)
    print(get_top_10_rows(rows_both_a1_a0,5, Top=False))
    fancy_print("TOP10 Cum                                  ??✓✓",level=2)
    print(get_top_10_rows(rows_both_cum,5))
    fancy_print("TOP10 A0Ass                                x✓??",level=2)
    print(get_top_10_rows(rows_a0_only,5))
    
def get_top_10_rows(top_10_rows, amount=10, Top=True):
    top_10_rows = top_10_rows.fillna('')  # Replace NaN values with empty string
    top_10_rows['Fans'] = top_10_rows['Fans'].astype(int)
    top_10_rows = top_10_rows[['Girl', 'Strasse','Gurl','Fans','a1','a0','cim','cof']].sort_values('Fans', ascending = not Top).head(amount)
    top_10_rows = top_10_rows.reset_index(drop=True)  # Reset index and drop the original index column
    top_10_rows.index += 1  # Assign labels from 1 to 10
    top_10_rows.index.name = 'Rank'  # Add an index name
    return top_10_rows


def convert_dataframe_to_html(df):
    # Sort the DataFrame by index
    df = df.sort_index()

    # Add Img column with image tags
    df.insert(0, 'Img', df['Purl'].apply(lambda x: f'<img src="{x}" style="max-width: 140px; max-height: 140px;">'))

    # Convert Purl column to clickable image URLs
    df['Purl'] = df['Purl'].apply(lambda x: f'<a href="{x}">img</a>')

    # Convert Gurl column to clickable URLs
    df['Gurl'] = df['Gurl'].apply(lambda x: f'<a href="{x}">url</a>')

    # Replace NaN values with empty string
    df = df.fillna("")

    # Convert DataFrame to HTML table
    table_html = df.to_html(escape=False, index=False, classes='sortable')

    # Create complete HTML page
    html = f'''
    <html>
    <head>
        <style>
            table {{
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
                border: none;
            }}
            
            th, td {{
                text-align: left;
                padding: 8px;
                border: none;
            }}
            
            th.sortable {{
                background-color: #007bff;
                color: white;
                cursor: pointer;
            }}
            
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            
            tr:hover {{
                background-color: #e6e6ff;
            }}
            
            img {{
                max-width: 140px;
                max-height: 140px;
                border: none;
            }}
        </style>
    </head>
    <body>
        {table_html}
        <link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.css" rel="stylesheet" />
        <script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>

    </body>
    </html>
    '''

    return html
