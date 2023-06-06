import gallib

"""

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

"""

# extract gals out of each category file
# and save them in a separate csv file
testpath = './data/2023-06-06_202336'
print('⌵ '+testpath[2:])
gallib.findhtmls(testpath)
#gallib.get_gals(testpath, 'analsex')

