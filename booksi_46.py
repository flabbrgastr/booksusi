from IPython.display import clear_output
clear_output()
print("Installing Python Libraries")

%pip install validators --quiet
%pip install pandas --quiet
%pip install --upgrade beautifulsoup4 --quiet

import ipywidgets as widgets
import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
import os
import sys
import requests
import validators
import re
import pandas as pd
import warnings


def inf(msg, style, wdth): inf = widgets.Button(description=msg, disabled=True, button_style=style, layout=widgets.Layout(min_width=wdth));display(inf)

warnings.simplefilter(action='ignore', category=FutureWarning)

clear_output()
print("Python Libraries are set up")
inf('\u2714 Done','success', '50px')




def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

# default to latest directory


def is_file_or_url(name_or_url):
    #    name_or_url = './'+name_or_url
    #    print('name or url input is ' + name_or_url)
    url = formaturl(name_or_url)
    #print('url: '+url)

    if (os.path.isfile(name_or_url)):
        #        print('valid file\n')
        return 'valid_file'
    elif (validators.url(url) == True):
        try:
            requests.get(url).status_code == 200
            #            print('valid url\n')
            return('valid_url')
        except:
            return 'none'
    else:
        return 'none'

def getTimedDir(rootdir, time):
    dirs = [dI for dI in os.listdir(
        rootdir) if os.path.isdir(os.path.join(rootdir, dI))]
    dirs = [dir for dir in dirs if dir.startswith('2')]
    dirs.sort(reverse=True)
    return dirs[time]


def getNewestDir(rootdir):
    dirs = [dI for dI in os.listdir(
        rootdir) if os.path.isdir(os.path.join(rootdir, dI))]
    dirs = [dir for dir in dirs if dir.startswith('2')]
    dirs.sort(reverse=True)
    return dirs[0]
#    return max([os.path.join(rootdir, d) for d in os.listdir(rootdir)], key=os.path.getmtime)


def getLastDir(rootdir):
    dirs = [dI for dI in os.listdir(
        rootdir) if os.path.isdir(os.path.join(rootdir, dI))]
    dirs = [dir for dir in dirs if dir.startswith('2')]
    dirs.sort(reverse=True)
    if len(dirs) >= 1:
        return dirs[1]
    else:
        return None


def getAllFilesofType(dir, ftype):
    path = dir
    files = [f for f in os.listdir(path) if f.endswith(ftype)]
    files.sort()
    return files


def getGals(content, va1, va0, vcim, vcof):
    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    # only input is content
    tmp = []
    page_soup = soup(content, "html.parser")

    wrap_container = page_soup.find(
        "div", {"class": "container", "id": "wrap"})
    girls = page_soup.findAll(
        "div", {"class": "girl-list-item", "data-type": "listing"})

    # sys.exit()

    # print('**********************************************************')
#    print('*', len(girls), "g's")
    # print('**********************************************************')

    left = '</strong>'
    right = '<a'

    for girl in girls:
        # print(girl.div.a.text)  	    	    	# girl name
        girl_name = girl.select_one(
            "div a:nth-of-type(1)").text.strip()  	# girl name
        girl.div.a['href']      	    	    	# url

        # Adresse
        girl.div.div.text       	    	    	# addresse ganz
        node = girl.div.div.select_one("div a:nth-of-type(1)")
        if node is not None:
            stadt = node.text.strip()
        else:
            stadt = 'Wien'
#        stadt = girl.div.div.select_one(
#            "div a:nth-of-type(1)").text.strip()  	# stadt

        node = girl.div.div.select_one("div a:nth-of-type(2)")  	# bezirk
        if node is not None:
            bezirk = node.text.strip()
        else:
            bezirk = '1000'

#        bezirk = girl.div.div.select_one(
#            "div a:nth-of-type(2)").text.strip()  	# bezirk
        try:
            # strasse not every girl has it
            strasse = girl.div.div.select_one("div a:nth-of-type(3)").text
        except:
            strasse = ''
        try:
            # the fancount is not always there
            fancount = girl.select_one("span[id*=girl-fancount]").text
        except:
            fancount = 0
        try:
            # the notsoshort description
            short_str = str(girl.select("div .girl-subtitle"))
            short = short_str[short_str.index(
                left)+len(left):short_str.index(right)].strip()
        except:
            short = ''
            # the notsoshort description as string
        node = girl.find('a', {'class': 'pull-right'})
        if node is not None:
            tel = node['href']
        else:
            tel = 'None'
#        tel = girl.find('a', {'class': 'pull-right'})['href']

        gurl = girl.find('a', href=True)['href']

        node = girl.find('source', srcset=True)
        if node is not None:
            purl = node['srcset']
        else:
            purl = None
        #purl = girl.find('source', srcset=True)['srcset']

        # append the Girl in every loop
        tmp.append({'Girl': girl_name, 'Tel': tel, 'Short': short,
                    'Bezirk': bezirk, 'Stadt': stadt, 'Strasse': strasse, 'Fans': fancount,
                    'Gurl': gurl, 'Purl': purl,
                    'a1': va1, 'a0': va0, 'cim': vcim, 'cof': vcof,
                    't':''
                    })
    #print (tmp)
    return tmp


def getFolderGals(folder):
  dftmp = pd.DataFrame(columns=['Girl', 'Tel', 'Short',
                               'Bezirk', 'Stadt', 'Strasse', 'Fans',
                               'Gurl', 'Purl', 'a1', 'a0', 'cim', 'cof','t'])
  allFiles = getAllFilesofType(folder, '.html')
  for f in allFiles:
    with open(folder+'/'+f, 'r') as file:
      #print(f,end='.', flush=True)
      tmp = getGals(file.read(),  # file
        str_a1 in f,            # service args
        str_a0 in f,
        str_cim in f,
        str_cof in f)
      dftmp = dftmp.append(tmp)
      if (len(tmp)<25):
        print (len(tmp),end='', flush=True)
      else:
        print ('.',end='', flush=True)
  print('')
  return dftmp;

def dfComprehend(dfnew):
  #sort dfnew
  print (len(dfnew.index),'Gals comprehended to ',end='', flush=True)
  dfnew = dfnew.sort_values(by=['Girl'], ascending=True)
  dfnew = dfnew[dfnew["Girl"].str.contains("Trans|trans|TRANS|^ts |^TS |^Ts |^Ts_")==False]  # remove trans
  dfnew = dfnew.groupby(['Girl', 'Tel'], as_index=False).max()
  print (len(dfnew.index))
  return dfnew;



clear_output()
# default url
default_url = "https://booksusi.com/service/analsex/?&city=wien&service=2&page="
default_csv = "b.csv"
datadir = '/content/drive/MyDrive/rclone'

str_a0 = 'anal_natur_no_condom'
str_a1 = 'analsex'
str_cof = 'cum_on_face'
str_cim = 'cum_in_mouth'
tarfiles=[]

def xtracttarimages(datadir):
  tarfiles = []  # List to store tar file names
  for x in os.listdir(datadir):
    if x.endswith(".tar.gz"):
      tarfiles.append(x)  # Append tar file names to the list
  if len(tarfiles) > 0:
    print (tarfiles)
    for tar in tarfiles:
#      print('untaring', tar)
      !tar -xzf $datadir/$tar -C $datadir --overwrite  # Extract the tar file
      tarfolder = tar.replace('.tar.gz', '')  # Get the folder name after extraction
      imagecount = 0  # Variable to count the number of images
      for y in os.listdir(datadir+'/'+tarfolder):
        if y.endswith(".jpg"):
          imagecount += 1  # Increment the image count
      #print('untaring', imagecount, 'images')
      #!mv $datadir/$tarfolder/*.jpg $datadir/GalImages/ -f  # Move extracted images to a different directory
      #print('deleting tar')
      !rm $datadir/$tar  # Remove the tar file after extraction
  else: 
    print('no tar')
    return 0  # Return 0 if no tar files found
  return imagecount  # Return the total count of extracted images

def numberoffiles(dir, ending, r=False):
    count = 0  # Variable to store the count of files
    if r:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(ending):
                    count += 1  # Increment the count for each file with the specified ending
    else:
        for file in os.listdir(dir):
            if file.endswith(ending):
                count += 1  # Increment the count for each file with the specified ending
    return count

imagesBefore=numberoffiles(datadir+'/GalImages','.jpg')
#print('new images '+ str(xtracttarimages(datadir)));
imagesNow=imagesBefore + xtracttarimages(datadir);

print('Images New/Total:',imagesNow-imagesBefore,'.', imagesNow-imagesBefore)
inf('\u2714 Done','success', '50px')


from pandas.tseries.offsets import Hour
from numpy import size
# Find the newest data directory

latest_backwards=1

newestDir = getTimedDir(datadir, 0)
newest_csv = datadir+'/'+newestDir+'/'+'c.csv'
lastDir = getTimedDir(datadir,latest_backwards)
last_csv = datadir+'/'+lastDir+'/'+'c.csv'
allFiles = getAllFilesofType(datadir+'/'+newestDir, '.html')
#print('new ', newest_csv,'\nlast', last_csv )

def insert_colon(string, index):
    return string[:index] + ':' + string[index:]

def reformatTime(fnewestDir):
  fnewestDir = insert_colon(fnewestDir,13)
  fnewestDir = insert_colon(fnewestDir,16)
  fnewestDir = fnewestDir.replace('_',' ')
  return fnewestDir;

#print('Time Delta:',pd.Timedelta( 
#    pd.to_datetime(reformatTime(newestDir)) -
#    pd.to_datetime(reformatTime(lastDir))
#  )
#)

print(newestDir, '   Delta:',pd.Timedelta( 
    pd.to_datetime(reformatTime(newestDir)) -
    pd.to_datetime(reformatTime(lastDir))
  )
)



# Setup panda frames

if (os.path.isfile(newest_csv)):
    dfnew = pd.read_csv(newest_csv, index_col=False)
    print('newest_csv file esists with', len(dfnew.index),'Gals')
else:
    # create a new csv and pandas
    print('Creating',newest_csv)
    dfnew=getFolderGals(datadir+'/'+newestDir);
    dfnew=dfComprehend(dfnew);
    dfnew.to_csv(datadir+'/'+newestDir+'/'+'c.csv', index=False)
if (os.path.isfile(last_csv)):
    dflast = pd.read_csv(last_csv, index_col=False)
    print('last_csv file esists with', len(dflast.index),'Gals')
else:
    print('last_csv does not esists')
    dflast=getFolderGals(datadir+'/'+lastDir);
    dflast=dfComprehend(dflast);
    dflast.to_csv(datadir+'/'+lastDir+'/'+'c.csv', index=False)




# check differences between new and last
df=dfnew


########### Stabil ################
dfstabil = pd.merge(df, dflast, on=['Girl','Tel'], how='inner')
# remove columns with _y's
dfstabil = dfstabil.loc[:, ~dfstabil.columns.str.endswith('_y')]
dfstabil = dfstabil[dfstabil.columns[~dfstabil.columns.str.endswith('_y')]]
# remove _x string
dfstabil = dfstabil.rename(columns = lambda x: x.strip('_x'))
#dfstabil.head(10)

########### OUT ################
dfout = pd.merge(df, dflast, on=['Girl','Tel'], how='right', indicator=True)
dfout=dfout.query('_merge == "right_only"').drop('_merge', 1)
# remove columns with _x's
dfout = dfout.loc[:, ~dfout.columns.str.endswith('_x')]
dfout = dfout[dfout.columns[~dfout.columns.str.endswith('_x')]]
# remove _y string
dfout = dfout.rename(columns = lambda x: x.strip('_y'))
dfout = dfout.assign(t='out')

###################################################
# Get Incoming Gals
###################################################

# get all incomin gals
dfin = pd.merge(df, dflast, on=['Girl','Tel'], how='left', indicator=True)
dfin = dfin.query('_merge == "left_only"').drop('_merge', 1)
# remove columns with _y's
dfin = dfin.loc[:, ~dfin.columns.str.endswith('_y')]
dfin = dfin[dfin.columns[~dfin.columns.str.endswith('_y')]]
# remove _x string
dfin = dfin.rename(columns = lambda x: x.strip('_x'))
dfin = dfin.assign(t='new')

# dfinass tests
dfall = pd.concat([dfstabil, dfin], ignore_index=True, sort=False)
dfall = dfall.sort_values(by=['Girl'], ascending=True)
#dfall.head()
#dfall.to_csv(datadir+'/'+newestDir+'/'+'dfall.csv', index=False)

# get all  ass
dfass = dfall.query('a0 == True | a1 == True')

# get all incoming ass
dfinass = dfin.query('a0 == True | a1 == True')
dfinass = dfinass.assign(t='new')


dfin = dfin.replace({True: 'X', False: '.'})
dfstabil = dfstabil.replace({True: 'X', False: '.'})
dfout = dfout.replace({True: 'X', False: '.'})
dfall = dfall.replace({True: 'X', False: '.'})
dfinass = dfinass.replace({True: 'X', False: '.'})
dfass = dfass.replace({True: 'X', False: '.'})


#print('Newest / Last: ', len(df.index),'/',len(dflast.index),'Gals in', newestDir)
print('Gals\tNew\t Ass\tNewAss\tStabil\tOut')
print(len(df.index),'\t',len(dfin.index),'\t',len(dfass.index),'\t',len(dfinass.index),'\t',len(dfstabil.index),'\t',len(dfout.index))


# Store da csv's
#df.to_csv(datadir+'/'+newestDir+'/'+'c.csv', index=False)
dfall.to_csv(datadir+'/'+newestDir+'/'+'all.csv', index=False)
dfin.to_csv(datadir+'/'+newestDir+'/'+'in.csv', index=False)
dfass.to_csv(datadir+'/'+newestDir+'/'+'ass.csv', index=False)
dfinass.to_csv(datadir+'/'+newestDir+'/'+'inass.csv', index=False)
dfout.to_csv(datadir+'/'+newestDir+'/'+'out.csv', index=False)
print('Write CSVs in',datadir+'/'+newestDir)

