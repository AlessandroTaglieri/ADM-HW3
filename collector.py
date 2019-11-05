#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import time
import random
f = open("/Users/digitalfirst/Desktop/HW3 ADM/movies3.html")

soup = BeautifulSoup(f)
listUrl_Movies3=[]
for link in soup.select('a'):
    listUrl_Movies3.append(link.text)


# In[ ]:


def downloadFile(index):

    for index in range(len(listUrl_Movies3)):
        
        t2=1200
        try:
            t1 = random.randint(1,5)
            time.sleep(t1)
            url=listUrl_Movies3[index]
            response = requests.get(url)
            name="aritcle_"
            extension=".html"
            file="{}{}{}".format(name,index,extension)
            with open(file,'wb') as f: 
                f.write(response.content)  

        except response.status_code as e:
            print("exception")
            if e==492:
                time.sleep(t2)
                downloadFile(index+1)
            elif e==200:
                soup = BeautifulSoup(listUrl_Movies3[1])
                
                with open(file,'w') as f: 
                    f.write(soup.text)
                downloadFile(index+1)
            else:
                continue


# In[ ]:


downloadFile(0)

