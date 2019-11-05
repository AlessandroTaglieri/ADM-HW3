#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os.path
#define column of our dataframe
df=pd.DataFrame(columns=['title', 'intro', 'plot'])


for index in range(len(listUrl_Movies3)):
    
    title=''
    plot=''
    intro=''
    movie=[]
    
    #define name of the file that we want to find (in my case: in the same directory)
    name="aritcle_"
    extension=".html"
    file="{}{}{}".format(name,index,extension)
    
    #check if this file exists
    if not os.path.isfile(file):
        continue
        
    #open file   
    response2 = open(file)
    soup = BeautifulSoup(response2)
    #take title.
    title=soup.title.text.rsplit(' ', 2)[0]
    
    #take all p in intro(firt section)
    if soup.find('span', attrs={'class': 'mw-headline'}):
        heading = soup.find('span', attrs={'class': 'mw-headline'})
        paragraphs = heading.find_all_previous('p')
        for p in paragraphs: 
            intro = p.text + intro
            
     
        #take all p in 'plot'(second section)
        b=True
        if soup.find('span', attrs={'class': 'mw-headline'}):   
            heading = soup.find('span', attrs={'class': 'mw-headline'})
            if heading.find_all_next('p'):
            
                paragraphs = heading.find_all_next('p')
                for p in paragraphs: 
                    # print (team.text)
                    plot=plot+p.text
                    if p.next_sibiling:
                    
                        if not p.next_sibling.name=='p':
                            b=False
                        if not b:
                            continue
                    else:
                        continue
            else:
                plot="NAN"
        else:
            plot="NAN"
    
    
    
    
    else:
        intro="NAN"
        plot="NAN"
    
    #here: code to get info about infobox from every page        
            
    
    #put all infos in movie list
    movie=[title,intro,plot]
    #update dataframe with this list
    df.loc[index] = movie
