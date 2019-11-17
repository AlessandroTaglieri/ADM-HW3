#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import time
import random

#we saved url about every wikipedia page from movies1/movies2/movies3 in three different files: listUrl_Movies1, listUrl_Movies2, listUrl_Movies3
f1 = open("HW3 ADM/movies3.html")
f3 = open("HW3 ADM/movies1.html")
f2 = open("HW3 ADM/movies2.html")
soup = BeautifulSoup(f1)
soup1 = BeautifulSoup(f3)
soup2 = BeautifulSoup(f2)
listUrl_Movies1=[]
listUrl_Movies2=[]
listUrl_Movies3=[]
for link in soup.select('a'):
    listUrl_Movies3.append(link.text)
for link in soup2.select('a'):
    listUrl_Movies2.append(link.text)
for link in soup1.select('a'):
    listUrl_Movies1.append(link.text)
#we put in totalMovies the number of urls of movies1/movies2/movies3
totalMovies=len(listUrl_Movies1)+len(listUrl_Movies2)+len(listUrl_Movies3)    

#function that allows to download html file from url list. Every person of the tema download html files from listUrl_Movies1/listUrl_Movies2/listUrl_Movies3
def downloadFile():

    for index in range(listUrl_Movies1):
        
        t2=1200
        try:
            #wait n seconds (from 1 to 5) between every request
            t1 = random.randint(1,5)
            time.sleep(t1)
            url=listUrl_Movies3[index]
            response = requests.get(url)
            name="article_"
            extension=".html"
            file="{}{}{}".format(name,index,extension)
            with open(file,'wb') as f: 
                f.write(response.content)  

        except response.status_code as e:
            print("exception")
            #error=492 is error that occurs when we have done a limit of request
            if e==492:
                #wait 20 minutes
                time.sleep(t2)
                downloadFile(index+1)
            elif e==200:
                soup = BeautifulSoup(listUrl_Movies3[1])
                with open(file,'w') as f: 
                    f.write(soup.text)
                downloadFile(index+1)
            else:
                continue

#call previous function tht creates html files
downloadFile()

