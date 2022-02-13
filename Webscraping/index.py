import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import datetime
import re

def extractInformation(URL):
    print("--------Extraction started-----------")

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    description = soup.find("p", itemprop="description")
    label = soup.find_all("div", {"class": "spaceit_pad"})
    if(soup.find("p",{"class":"title-english title-inherit"})):
        name=soup.find("p",{"class":"title-english title-inherit"}).text
    else:
        name=soup.find("h1",{"class":"title-name h1_bold_none"}).text
    information = []
    for info in label:
        information.append(info.text.strip().split(':\n'))
    data = {}
    data['Name']=name.strip()
    data['Description']=description.text.replace("\n","").replace('[Written by MAL Rewrite]',"")
    for pair in information:
        if(len(pair)>1):
            data[pair[0].strip()]=pair[1].strip().replace("\n","").replace("  ","")

    print("--------Extraction of ",name," over-----------")
    return data

def extractURLs(URL):
    print("******---------File opened---------********")
    data = []
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,'html5lib')
    urls = soup.find_all("a",{"class":"hoverinfo_trigger fl-l ml12 mr8"},href=True)
    for url in urls:
        data.append(extractInformation(str(url['href'])))
        if(str(url['href'])=="https://myanimelist.net/anime/38524/Shingeki_no_Kyojin_Season_3_Part_2"):
            break
    with open("first50.json", "w") as outfile:
        json.dump(data, outfile)
    print("******---------File written---------********")

def transformDate(date):
    listOfDate = date.split(' to ')
    dates = {'AiredFrom':'','AiredTo':''}
    datesList = []
    for i in range(len(listOfDate)):
        a=''
        try:
            a=datetime.strptime(listOfDate[i], '%b %d, %Y').strftime('%d/%m/%Y')
        except ValueError:
            try:
                a=datetime.strptime(listOfDate[i], '%b, %Y').strftime('%m/%Y')
            except ValueError:
                try:
                    a=datetime.strptime(listOfDate[i], '%Y').strftime('%Y')
                except ValueError:
                    a=''
        finally:
            datesList.append(a)
    dates['AiredFrom']=datesList[0]
    dates['AiredTo'] = datesList[1] if len(datesList)>1 else ''
    return dates

def transformNumbers(value):
    return re.sub("[^\d\.]", "", value)
# transformNumbers('8.811 (scored by 247419247,419 users)1indicates a weighted score.')

a=extractInformation("https://myanimelist.net/anime/39900/Haru_Natsu")
print(a)