import gallib as gl
import pandas as pd
import os
import sys


if "-h" in sys.argv:
    print('''
    Usage:
        python booksi.py [options]
        -h  help
        -ci csv import instead of html analysis. Faster for testing.
        -s show stats''')
    sys.exit()

# Specify the directory
dir_path = './data'  # replace with your directory

# leave only one, ie the newest, zip file for each date
dfiles = gl.clean_files(dir_path, test_mode=False)
ddirs = gl.clean_dirs(dir_path, test_mode=False)
if dfiles or ddirs:
    print(str(dfiles) +' / '+str(dfiles) + '   dirs / files cleaned')

# get the last directory
lastdir = gl.getlastdir(dir_path)

# get the names of categories in the last directory
# summarize each category into a single file
names = gl.ex_names(lastdir)
if names:
    print('html preprocessing '+lastdir)
    for name in names:
        catted = gl.cat_files(lastdir, name, remove=True)
#        print('    '+name + ' ... ' + str(catted))
else:
    print('no files found in ' + lastdir)

if "-ci" not in sys.argv:
    # extract gals out of each category file
    # and save them in a separate csv file
    print('⌵ getgals '+lastdir[2:])
    html_files = gl.findhtmls(lastdir)
    #dataframes = []
    pdall = pd.DataFrame()

    for file in html_files:
        category = os.path.splitext(file)[0]

        arr = gl.get_gals(lastdir, file)
        df = pd.DataFrame(arr)
    #   print(df.head(3))
        pdall = pd.concat([pdall, df], ignore_index=True)

    pdall = gl.dfComprehend(pdall)
    
    if "-s" in sys.argv:
        gl.someStats(pdall)

    # Create the directory if it doesn't exist
    if not os.path.exists(lastdir+'/gen/'):
        os.makedirs(lastdir+'/gen/')
    # Write DataFrame to CSV file (overwrite if exists)
    csv_file = lastdir+'/gen/'+'all.csv'
    pdall.to_csv(csv_file, index=False, mode='w')
else:
    # ingest existing csv file
    pdall = pd.read_csv(lastdir+'/gen/all.csv')
    if "-s" in sys.argv:
        gl.someStats(pdall)

print('⌵ write csv and html')
html_table = gl.convert_dataframe_to_html(pdall)
#html_table = gallib.df_to_html2(pdall)
html_file = lastdir+'/gen/'+'all.html'
with open(html_file, 'w') as hfile:
    hfile.write(html_table)
