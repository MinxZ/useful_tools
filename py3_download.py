from bs4 import BeautifulSoup
import requests
import re
import urllib
import os
import json
import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

def get_soup(url,header):
    import urllib.request    #urllib library for Extracting web pages

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    resp = opener.open(req)
    #respData = str(resp.read())
    return BeautifulSoup(resp,'html.parser')



query = input("query image")# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
#url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
url = 'https://www.google.co.jp/search?q=' + query+ '=acti'

print(url)
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)
ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print("there are total" , len(ActualImages),"images")

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
fn = 'logo'
ii = 0
for i , (img , Type) in enumerate( ActualImages):
    #if int(i) < 20:
        i = str(i)
        filename = fn + i
        lec = opener.open(img)
        with open(filename+'.'+Type,'wb') as output:
            output.write(lec.read())
