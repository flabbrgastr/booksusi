import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
import os
import sys
import requests
import validators
import re
import pandas as pd

# default url
default_url = "https://booksusi.com/service/analsex/?&city=wien&service=2&page="
default_csv = "b.csv"
datadir = './data'

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

def getNewestDir(rootdir):
    return max([os.path.join(rootdir,d) for d in os.listdir(rootdir)], key=os.path.getmtime)
   
def getAllFilesofType(dir, ftype):
    path = dir
    files = [f for f in os.listdir(path) if f.endswith(ftype)]
    files.sort()
    return files

    
#newestDir
#allFiles
#print(allFiles)

#sys.exit()


# test if command line arguments are available
if len(sys.argv) > 1:

    # check command line args
    file_or_url = is_file_or_url(sys.argv[1])

    if (sys.argv[1] == 'd'):  # Option d for default dir
        newestDir = getNewestDir(datadir)
        allFiles = getAllFilesofType(newestDir, '.html')
        print('d:', newestDir)
        with open(newestDir+'/'+allFiles[0], 'r') as file:
            content = file.read()
    elif (file_or_url == 'valid_file'):
    # its a valid file
        print('valid file: '+sys.argv[1])
        with open(sys.argv[1], 'r') as file:
            content = file.read()

    elif (file_or_url == 'valid_url'):
    # its a valid URL
        url = formaturl(sys.argv[1])
        print('valid url: '+url)
        # opens the connection and downloads html page from url
        # uClient = uReq(page_url)
        page = requests.get(url)

        if page.status_code == 200:
            content = page.content

# no command line argument
else:
    # defaulting to default url if nothing is given
    url = default_url
    print("defaulting to url: "+url)
    page = requests.get(url)
    if page.status_code == 200:
        content = page.content
    file_or_url = is_file_or_url(url)

# check if csv exists, put into pandas structure df
default_csv = newestDir+'/'+default_csv
#print(default_csv)
#sys.exit()

if (os.path.isfile(default_csv)):
    df = pd.read_csv(default_csv, index_col = False)
    print('Read csv: ',+len(df.index))
#    print(df)
else:
# create a new csv and pandas
    print('Create new csv...')
    df = pd.DataFrame(columns=['Girl', 'Tel', 'Short',
                  'Bezirk', 'Stadt', 'Strasse', 'Fans',
                  'Gurl', 'Purl'])


# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(content, "html.parser")

wrap_container = page_soup.find("div", {"class": "container", "id": "wrap"})
girls = page_soup.findAll(
    "div", {"class": "girl-list-item", "data-type": "listing"})

#sys.exit()

#print('**********************************************************')
print('*', len(girls), "g's")
#print('**********************************************************')

left = '</strong>'
right = '<a'

for girl in girls:
    # print(girl.div.a.text)  	    	    	# girl name
    girl_name = girl.select_one(
        "div a:nth-of-type(1)").text.strip()  	# girl name
    girl.div.a['href']      	    	    	# url

    # Adresse
    girl.div.div.text       	    	    	# addresse ganz
    stadt = girl.div.div.select_one(
        "div a:nth-of-type(1)").text.strip()  	# stadt
    bezirk = girl.div.div.select_one(
        "div a:nth-of-type(2)").text.strip()  	# bezirk
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
    tel = girl.find('a', {'class': 'pull-right'})['href']
    
    
    gurl = girl.find('a', href=True)['href']
    purl = girl.find('source', srcset=True)['srcset']
    
    # append the Girl in every loop
    df = df.append({'Girl': girl_name, 'Tel': tel, 'Short': short,
                    'Bezirk': bezirk, 'Stadt': stadt, 'Strasse': strasse, 'Fans': fancount,
		    'Gurl': gurl, 'Purl': purl
                    }, ignore_index=True)

# drop duplicates, based on Column
df=df.drop_duplicates(subset='Tel', keep="last")
print('Writing ', +len(df.index))
#print('Writing ', +len(df.index) + ' lines in ',+default_csv)
#df.to_csv('a.csv', index = False)
df.to_csv(default_csv, index = False)
print(df)
