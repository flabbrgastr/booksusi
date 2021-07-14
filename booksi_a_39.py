import requests
from bs4 import BeautifulSoup as soup  # HTML data structure
import os
import sys
import requests
import validators
import re


def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url


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


# default url
default_url = "https://booksusi.com/service/analsex/?&city=wien&service=2&page="


# test if command line arguments are available
if len(sys.argv) > 1:

    # check command line args
    file_or_url = is_file_or_url(sys.argv[1])

    if (file_or_url == 'valid_file'):
        print('valid file: '+sys.argv[1])
        with open(sys.argv[1],'r') as file:
           content = file.read();

    elif (file_or_url == 'valid_url'):
        url = formaturl(sys.argv[1])
        print('valid url: '+url)
        # opens the connection and downloads html page from url
        # uClient = uReq(page_url)
        page = requests.get(url)

        if page.status_code == 200:
            content = page.content

else:
    # defaulting to default url
    url = default_url
    print("defaulting to url: "+url)
    page = requests.get(url)
    if page.status_code == 200:
       content = page.content
    file_or_url = is_file_or_url(url)


#sys.exit()

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com


# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(content, "html.parser")

wrap_container = page_soup.find("div", {"class": "container", "id": "wrap"})
# girl_list = page_soup.find("div", {"class": "girl-list", "id": "girls"})
girls = page_soup.findAll(
    "div", {"class": "girl-list-item", "data-type": "listing"})

print('**********************************************************')
print('***', len(girls), " Analgirls gefunden")
print('**********************************************************')


left = '</strong>'
right = '<a'

for girl in girls:
    # print(girl.div.a.text)  # girl name
    girl_name = girl.select_one(
        "div a:nth-of-type(1)").text.strip()  # girl name
    girl.div.a['href']      # url

    # Adresse
    girl.div.div.text  # addresse ganz
    stadt = girl.div.div.select_one(
        "div a:nth-of-type(1)").text.strip()  # stadt
    bezirk = girl.div.div.select_one(
        "div a:nth-of-type(2)").text.strip()  # bezirk
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
        # short_in = girls.select("div .girl-subtitle")  # the notsoshort description
        short_str = str(girl.select("div .girl-subtitle"))
        short = short_str[short_str.index(
            left)+len(left):short_str.index(right)].strip()
    except:
        short = ''
    # the notsoshort description as string
    tel = girl.find('a', {'class': 'pull-right'})['href']

    # print girlname and short description
    print(girl_name, tel, '<', short, '>', 'aus', bezirk, stadt,
          strasse, 'hat', fancount, 'fans')
    # Tel
