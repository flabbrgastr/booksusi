import os
import gallib as gl
import pandas as pd

def newsidlist(old_folder, new_folder):
    # Get the paths to the old and new CSV files
    old_csv_file = old_folder + '/gen/all.csv'
    new_csv_file = new_folder + '/gen/all.csv'

    # Read the old and new CSV files into pandas dataframes
    old_df = pd.read_csv(old_csv_file)
    new_df = pd.read_csv(new_csv_file)

    # Identify the rows in the new CSV that have 'sid' not present in the old CSV
    new_sids = new_df[~new_df['sid'].isin(old_df['sid'])]['sid'].tolist()

    # Return the list of new sids
    return new_sids

# Specify the paths to the old and new folders
path = './data'
new_folder, delta0 = gl.matchdir('./data', 0)
old_folder, delta1 = gl.matchdir('./data', 1)
new_folder = path +'/'+new_folder
old_folder = path +'/'+old_folder

print("delta = 0:", new_folder)
print("delta = 1:", old_folder)

# Compare the CSV files and create the new CSV file
sidlist = newsidlist(old_folder, new_folder)
print (len(sidlist))
# Get the path to the all.csv file in the new folder
all_csv_file = new_folder + '/gen/all.csv'

# Read the all.csv file into a pandas dataframe
all_df = pd.read_csv(all_csv_file)

# Update the 't' column for matching sids
all_df.loc[all_df['sid'].isin(sidlist), 't'] = 'new'

# Write the updated dataframe back to the all.csv file
all_df.to_csv('./allnew.csv', index=False)

