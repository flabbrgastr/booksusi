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
from datetime import datetime, timedelta
import wcwidth


def prune_items(path, test_mode=True):
    # Group files and folders by week
    files_by_week = defaultdict(lambda: defaultdict(list))
    folders_by_week = defaultdict(lambda: defaultdict(list))
    
    # Get current time
    now = datetime.now()
    
    # Counter for pruned items
    pruned_items = 0
    
    # Iterate over each item in the directory
    for item in os.listdir(path):
        # Full path of item
        item_path = os.path.join(path, item)
        
        # Get the date from the item name
        try:
            # Expected format YYYY-MM-DD_TTTTTT
            item_date = datetime.strptime(item[:10], '%Y-%m-%d')
        except ValueError:
            # Skip item if it doesn't match the expected format
            print(f"Skipping {item}, does not match expected format")
            continue
        
        # Get the number of weeks since the item's creation
        weeks_since_creation = (now - item_date).days // 7
        
        # Group items by weeks and type
        if os.path.isfile(item_path):
            files_by_week[weeks_since_creation][item_date].append(item_path)
        elif os.path.isdir(item_path):
            folders_by_week[weeks_since_creation][item_date].append(item_path)
    
    # Keep only the most recent item and one per week for files
    for week, files_by_date in files_by_week.items():
        for date, files in files_by_date.items():
            # Sort by creation time
            files.sort(key=lambda x: os.path.getctime(x), reverse=True)
            # If it's the current week, keep one item per day
            if week == 0:
                # Remove all but the most recent file for each day
                for file in files[1:]:
                    if test_mode:
                        print(f"Test mode: Would delete file {file}")
                    else:
                        os.remove(file)
                        pruned_items += 1
                        #print(f"Deleted file: {file}")
            else:
                # Remove all but the most recent file for each week
                for file in files[1:]:
                    if test_mode:
                        print(f"Test mode: Would delete file {file}")
                    else:
                        os.remove(file)
                        pruned_items += 1
                        #print(f"Deleted file: {file}")

    # Keep only the most recent item and one per week for folders
    for week, folders_by_date in folders_by_week.items():
        for date, folders in folders_by_date.items():
            # Sort by creation time
            folders.sort(key=lambda x: os.path.getctime(x), reverse=True)
            # If it's the current week, keep one item per day
            if week == 0:
                # Remove all but the most recent folder for each day
                for folder in folders[1:]:
                    if test_mode:
                        print(f"Test mode: Would delete folder {folder}")
                    else:
                        shutil.rmtree(folder)
                        pruned_items += 1
                        #print(f"Deleted folder: {folder}")
            else:
                # Remove all but the most recent folder for each week
                for folder in folders[1:]:
                    if test_mode:
                        print(f"Test mode: Would delete folder {folder}")
                    else:
                        shutil.rmtree(folder)
                        pruned_items += 1
                        #print(f"Deleted folder: {folder}")

    # Return the number of pruned items
    return pruned_items


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


def cat_files(dir_path, name, remove=True):
    concatenated_files = 0  # Counter for concatenated files
    concatenated_content = ""
    files = os.listdir(dir_path)
    num_items = len([f for f in files if f.startswith(name)])
    progress_bar = tqdm(total=num_items, desc='   ✓ '+name,
                        bar_format="{l_bar}", ncols=80)
    for filename in files:
        if filename.startswith(name):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                sgirls = soup(content, 'html.parser')
                girls = sgirls.find_all("div",
                              {"class": "girl-list-item",
                               "data-type": "listing"})
                progress_bar.update(1)
                for girl in girls:
                    concatenated_content += str(girl)
                if remove:
                    os.remove(file_path)
            concatenated_files += 1
    output_file_path = dir_path + '/' + f"{name}.html"
    with open(output_file_path, 'w') as output_file:
        output_file.write(concatenated_content)
        output_file.close()
    progress_bar.close()
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
            score_element = girl.find('div', class_='girl-score')
            score = score_element.text
        except:
            score = ''

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
        
        # Find the div element with the specified class
        #div = soup.find('div', class_='girl-list-item')
        try:
            # Extract the data-id and owner-id attributes
            sid = girl['data-id']
            gid = girl['class'][2].split('-')[1]
        except:
            sid = None
            gid = None

        tmp.append({'Girl': girl_name,
                    'Stadt': stadt,
                    'Bezirk': bezirk,
                    'Strasse': strasse,
                    'Fans': fancount,
                    'Score': score,
                    'Short': short,
                    'Tel': tel,
                    'Gurl': gurl,
                    'Purl': purl,
                    'a1': a1,
                    'a0': a0,
                    'cim': cim,
                    'cof': cof,
                    'sid': sid,
                    'gid': gid,
                    't':''
                    })
    progress_bar.close()
    return tmp


def dfComprehend(dfnew):
  #sort dfnew
  # Combine the existing patterns with the new one
    pattern = r"(trans|tv|^ts |^Ts_|real.*doll|sex.*puppe|doll.*real)"
    pattern = re.compile(pattern, re.IGNORECASE)  # Makes the pattern case-insensitive

    oldnum=len(dfnew.index)
    print ('    ',+oldnum,'comprehended to ',end='', flush=True)
    dfnew = dfnew.sort_values(by=['Girl'], ascending=True)
    # remove ugly stuff
    dfnew = dfnew[~(dfnew["Girl"].str.contains(pattern, na=False) 
                  | dfnew["Short"].str.contains(pattern, na=False))]
#    dfnew = dfnew[dfnew["Girl"].str.contains(pattern)==False]
#    dfnew = dfnew[dfnew["Short"].str.contains(pattern)==False]
    dfnew = dfnew.groupby(['Girl', 'Tel'], as_index=False).max()
    newnum=len(dfnew.index)
    percentage = (oldnum - len(dfnew.index)) / oldnum * 100
    print(f"{newnum} -{percentage:.0f}%")
    return dfnew;


def fancy_print(message, level=1):
    if level == 1:
        header = f"=== {message} ==="
        line = "=" * sum(wcwidth.wcwidth(c) for c in header)
    elif level == 2:
        header = f"--- {message} ---"
        line = "-" * sum(wcwidth.wcwidth(c) for c in header)
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
    get_top_10_rows(rows_all_checkmarks,5,title="TOP Supergals              🍑🍑💦💦")
    get_top_10_rows(rows_both_a1_a0,5,title="TOP Ass                🍑🍑")
    get_top_10_rows(rows_both_cum,5,title="TOP Cum              💦💦")
    get_top_10_rows(rows_a0_only,5,title="TOP Ass0              0🍑")

    print('Tels:')
    dups(df,'Tel')


def dups(df, columnid=''):
    dups = 0
    total = len(df)
    counts = df[columnid].value_counts()
    duplicates = counts[counts > 1]
    duplicate_list = list(zip(duplicates.index, duplicates.values))
    for columnid, occurrences in duplicate_list:
        dups+=occurrences
    print(f"    Total: {total}, Uniques: {total-dups}")


def get_top_10_rows(top_10_rows, amount=10, Top=True, title="", print_top_10_rows=True):
    top_10_rows = top_10_rows.fillna('')  # Replace NaN values with empty string
    top_10_rows['Fans'] = top_10_rows['Fans'].astype(int)
    top_10_rows = top_10_rows[['Girl', 'Strasse','Fans','a1','a0','cim','cof']].sort_values('Fans', ascending = not Top).head(amount)
    top_10_rows = top_10_rows.reset_index(drop=True)  # Reset index and drop the original index column
    top_10_rows.index += 1  # Assign labels from 1 to 10
    top_10_rows.index.name = 'Rank'  # Add an index name
    if print_top_10_rows:
        fancy_print(title, level=2)
        print(top_10_rows)
    return top_10_rows


def convert_dataframe_to_html(df):
    # Get the current date, time, and day
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    day_of_week = current_datetime.strftime("%A")
    stringif = lambda column, ifstring, ifempty: column.apply(lambda x: ifstring if isinstance(x, str) and x.strip() != '' else ifempty)
    stringappend = lambda column, ifstring, ifempty: column.apply(lambda x: x + ifstring if isinstance(x, str) and x.strip() != '' else x + ifempty)

    # Sort the DataFrame by index
    df = df.sort_index()

    # Add Img column with image tags
    # Add a clickable URL to 'Girl' column with link from 'Gurl' and name from 'Girl', opening in a new tab
    df.insert(0, 'Img', df['Purl'].apply(lambda x: f'<img src="{x}" style="max-width: 140px; max-height: 140px;">'))
    df['Girl'] = df.apply(lambda row: f'<a href="{row["Gurl"]}" target="_blank" class="no-underline">{row["Girl"]}</a>', axis=1)

    # Replace NaN values with empty string
    df = df.fillna("")
    
    condition = ((df['a1'].str.len() > 0) | (df['a0'].str.len() > 0)) & (df['Strasse'].str.len() > 0)
    ahomecount = df[condition].shape[0]
    asscount = len(df[(df['a1'] == '✓') | (df['a0'] == '✓')])

    # emoji and string operations on cells
    df.loc[(df['t'].apply(lambda x: isinstance(x, str) and x.strip() != "")), 'Girl'] += '<span style="color: red;"><sup><b>' + df['t'] + '</b></sup></span>'
#    df['Loc'] = stringif(df['Strasse'], '&#8962;', '&#9243;')
    df['Loc'] = stringif(df['Strasse'], '🛌', '🚗')
    df['a0'] = stringif(df['a0'], '🍑', '·')
    df['a1'] = stringif(df['a1'], '🍑', '·')
    df['cim'] = stringif(df['cim'], '💦', '·')
    df['cof'] = stringif(df['cof'], '💦', '·')

    # combine columns Stadt, Bezirk and Strasse into one column 'Location'
    df['Bezirk'] = df['Bezirk'].apply(lambda x: f'{x}<br>')
    df['Strasse'] = df['Strasse'].apply(lambda x: f'{x}<br>')
    df['Location'] = df['Bezirk'] + df['Strasse']
    # Remove Stadt, Bezirk and Strasse columns
    df = df.drop(columns=['Stadt', 'Bezirk', 'Strasse'])
    
    # Specify the desired order of columns
    new_column_order = ['Img', 'Girl', 'Loc', 'Score', 'Fans', 'a1', 'a0', 'cof', 'cim', 'Short', 'Location', 'Tel', 't']
    df = df[new_column_order]

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

            thead th {{
                position: sticky;
                top: 0;
                background-color: #f1f1f1;
            }}
            .no-underline {{
                text-decoration: none;
            }}

        </style>
    </head>
    <body>
        <p>Date: {formatted_datetime}, Time: {day_of_week}, Day: {day_of_week}, Gals: {len(df)}, As{asscount}, Ah{ahomecount}</p>
        {table_html}
        <script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>

    </body>
    </html>
    '''

    return html


def matchdir(path, delta):
    # Get the current date
    current_date = datetime.now().date()

    # Initialize a list to store directory-delta pairs
    dir_delta_pairs = []

    # Get the directories in path
    directories = [directory for directory in os.listdir(path)
                   if os.path.isdir(os.path.join(path, directory))]

    # Iterate over the directories
    for directory in directories:
        # Calculate the delta based on the directory name
        date_str = directory.split("_")[0]
        directory_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        dir_delta = (current_date - directory_date).days

        # Add the directory-delta pair to the list
        dir_delta_pairs.append((directory, dir_delta))

    # Print the list of directory-delta pairs
#    print("List of directory-delta pairs:")
#    for pair in dir_delta_pairs:
#        print(pair)

    if dir_delta_pairs:
        # Find the closest matching delta
        closest_delta = min(dir_delta_pairs, key=lambda x: abs(delta - x[1]))[1]

        # Find the directory with the closest matching delta
        closest_directory = next((pair[0] for pair in dir_delta_pairs if pair[1] == closest_delta), None)

        # Return the closest matching directory-delta pair
        return closest_directory, closest_delta

    return None, None


def newsidlist(old_folder, new_folder, column='sid', dir_path='./data', verbose=False):
    if isinstance(old_folder, int):
        # Calculate folder names based on the provided delta values
        getold_folder, deltaold = matchdir(dir_path, old_folder)
        old_csv_file = dir_path +'/'+getold_folder + '/gen/all.csv'
    else:
        # Get the paths to the old and new CSV files
        old_csv_file = dir_path +'/'+ old_folder + '/gen/all.csv'

    if isinstance(new_folder, int):
        # Calculate folder names based on the provided delta values
        getnew_folder, deltanew = matchdir(dir_path, new_folder)
        new_csv_file = dir_path +'/'+getnew_folder + '/gen/all.csv'
    else:
        # Get the paths to the old and new CSV files
        new_csv_file = dir_path +'/'+ new_folder + '/gen/all.csv'

    # Get the paths to the old and new CSV files
#    new_csv_file = os.path.join(new_folder, 'gen/all.csv')

    # Read the old and new CSV files into pandas dataframes
    old_df = pd.read_csv(old_csv_file)
    new_df = pd.read_csv(new_csv_file)

    # Identify the rows in the new CSV that have the specified column value not present in the old CSV
    new_values = new_df[~new_df[column].isin(old_df[column])][column].tolist()

    if verbose:
        matched_rows = new_df[new_df[column].isin(new_values)]
        print(f"{len(matched_rows)} New {deltanew} since-{deltaold} ")
        print(matched_rows)
        print(f"Old folder delta: {deltaold}")
        print(f"New folder delta: {deltanew}")

    return new_values


def update_dataframe(old_folder, new_folder, dir_path='./data', verbose=False):
    if isinstance(old_folder, int):
        # Calculate folder names based on the provided delta values
        getold_folder, deltaold = matchdir(dir_path, old_folder)
        old_csv_file = dir_path +'/'+getold_folder + '/gen/all.csv'
    else:
        # Get the paths to the old and new CSV files
        old_csv_file = dir_path +'/'+ old_folder + '/gen/all.csv'

    if isinstance(new_folder, int):
        # Calculate folder names based on the provided delta values
        getnew_folder, deltanew = matchdir(dir_path, new_folder)
        new_csv_file = dir_path +'/'+getnew_folder + '/gen/all.csv'
    else:
        # Get the paths to the old and new CSV files
        new_csv_file = dir_path +'/'+ new_folder + '/gen/all.csv'

    # Read the old and new CSV files into pandas dataframes
    old_df = pd.read_csv(old_csv_file)
    old_df = old_df.fillna("")
    # Replace NaN values with empty string

    new_df = pd.read_csv(new_csv_file)
    new_df = new_df.fillna("")

    # Merge the old and new dataframes on 'sid'
    merged_df = pd.merge(old_df, new_df, on='sid', suffixes=('_old', '_new'))

    # Identify the rows where 'Tel' or 'Strasse' has changed
    changed_rows = merged_df[
                             (merged_df['Tel_old'] != merged_df['Tel_new']) 
                           | (merged_df['Strasse_old'] != merged_df['Strasse_new'])
                           | (merged_df['Girl_old'] != merged_df['Girl_new'])
                           ]

    # Get the 'sid' values for the changed rows
    changed_sids = changed_rows['sid'].tolist()

    if verbose:
        # Print the differences in 'Tel' and 'Strasse' columns
        if not changed_rows.empty:
            print("Differences in 'Tel' and 'Strasse' columns:")
            print(changed_rows[['sid', 'Girl_old' ,'Girl_new' ,'Tel_old', 'Tel_new', 'Strasse_old', 'Strasse_new']])
        else:
            print("No differences found.")

    # Return the list of changed 'sid' values
    return changed_sids
