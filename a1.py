import requests
import pandas
from itertools import zip_longest
from bs4 import BeautifulSoup

base_url = "https://nh.craigslist.org/search/apa"
big_lis=[]
for num in range(0,3000,120):
    if num == 0:
        r=requests.get(base_url)
    else:
        r=requests.get(base_url+"?s="+str(num))

    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("li",{"class":"result-row"})

    for items in all:
        d={}
        d["Title"]=items.find("a",{"class":"result-title hdrlnk"}).text
        try:
            d["City"]=items.find("span",{"class":"result-hood"}).text.replace(" ","").replace("(","").replace(")","")
        except:
            print(None)
        try:
            det = items.find("span",{"class":"housing"}).text.replace("\n","").replace(" ","").split("-")
            d["bedroom"]=det[0]
            d["ft"]=det[1]
            #d["Detail"] = detail
        except:
            print(None)
        try:
            d["Price"]=items.find("span",{"class":"result-price"}).text
        except:
            print(None)
        big_lis.append(d)

df=pandas.DataFrame(big_lis)
df.to_csv("houses.csv")
