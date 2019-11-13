#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

df=pd.DataFrame(columns=['title', 'intro', 'plot', 'music', 'score'])
s1= 0.5
s2=0.4
s3=0.3
s4=0.1
   
for index in range(len(document)):
    score=0
    #get id of documnets_is
    numberDocument=document[index][9:]
    #get wikipedia url
    url=lmovies2[int(numberDocument)]
    name="aritcle_"
    extension2=".tsv"
    index=int(numberDocument)
    file="{}{}{}".format(name,index,extension2)
    #get info about title and intro for evert film that corresponds to every documents_id
    with open("C:/Users/Ela/Desktop/HW3/tsv/"+file,"r",encoding="utf-8") as tsvfile:
                tsv_index = list(csv.reader(tsvfile, delimiter='\t'))
                title=tsv_index[1][3]
             
                intro=tsv_index[1][1]
           
                plot=tsv_index[1][2]
       
                music=tsv_index[1][8]

                if all(elem in title  for elem in dict4.keys())==True:
                        score+=s1
                elif all(elem in intro  for elem in dict4.keys())==True:
                        score+=s2
                elif all(elem in plot  for elem in dict4.keys())==True:
                        score+=s3
                elif all(elem in title  for elem in dict4.keys())==True:
                        score+=s4
                film=[title,intro,plot,music,score]
                df.loc[index] = film
       
   
   
ndf=df.sort_values('score', ascending=False)

print(dict4.keys())
ndf

