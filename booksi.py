import gallib
import pandas as pd
import os

# Specify the directory
dir_path = './data'  # replace with your directory

# leave only one, ie the newest, directory for each date
dfiles = gallib.clean_files(dir_path, test_mode=False)
if dfiles:
    print(str(dfiles) + 'files cleaned')

# get the last directory
lastdir = gallib.getlastdir(dir_path)

# get the names of categories in the last directory
# summarize each category into a single file
names = gallib.ex_names(lastdir)
if names:
    print('entering '+lastdir)
    for name in names:
        catted = gallib.cat_files(lastdir, name)
        print('    '+name + ' ... ' + str(catted))
else:
    print('no files found in ' + lastdir)

# extract gals out of each category file
# and save them in a separate csv file

print('⌵ '+lastdir[2:])

print('⌵ getgals')
html_files = gallib.findhtmls(lastdir)
#dataframes = []
pdall = pd.DataFrame()

for file in html_files:
    category = os.path.splitext(file)[0]

    arr = gallib.get_gals(lastdir, file)
    df = pd.DataFrame(arr)
    pdall = pd.concat([pdall, df], ignore_index=True)

pdall = gallib.dfComprehend(pdall)

# Create the directory if it doesn't exist
if not os.path.exists(lastdir+'/gen/'):
    os.makedirs(lastdir+'/gen/')

# Write DataFrame to CSV file (overwrite if exists)
csv_file = lastdir+'/gen/'+'all.csv'
pdall.to_csv(csv_file, index=False, mode='w')

'''    
    csv_file = lastdir+'/gen/'+category+'.csv'
    df.to_csv(csv_file, index=False, mode='w')
    # Write DataFrame to HTML table (overwrite if exists)
    html_table = df.to_html(index=False)
    html_file = lastdir+'/gen/'+category+'.html'
    with open(html_file, 'w') as hfile:
        hfile.write(html_table)
'''
