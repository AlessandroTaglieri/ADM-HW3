#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import sys
import ast
import pandas as pd

#define function that allows us to calculate a list that is an intersection from two list
def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

#INPUT QUERY
words='enormous damage unless something is done immediately'
#we use dict3 to store term_id and its respective documents_id
dict3={}
##we use dict4 to store evry word and its respective documents_id
dict4={}
csv.field_size_limit(sys.maxsize)
#in listWords we have a list that contains all words about inout query
listWords = words.split()
listWords=[x.lower() for x in listWords]

#with vocabulary.tsv we start to build a dict3 with term_id for every words in wordsList
with open('tsv/vocobulary.tsv', 'r', newline='') as f_output:
    tsv_vocabulary = list(csv.reader(f_output, delimiter='\t'))
    for word in listWords:
        word=word.lower()
        present=False
        for row in tsv_vocabulary:
            if word.lower()==row[0]:
                dict3[row[1]]=[]
                present=True
        #case where word is not in vocabulary
        if present==False:
            dict4[word]=[]
            
    #we continue to match dicumnets_id to every term_id in dict3
    with open('tsv/index2.tsv', 'r', newline='') as f_output:
        tsv_index = list(csv.reader(f_output, delimiter='\t'))
        for k in dict3.keys():  
            for row in tsv_index:
                if row[0]==k:
                    dict3[k]=row[1]
                    continue
    
    
    #finally we build dict4 where evry word matches to respective documents_id
    for k in dict3.keys():
        
        for row in tsv_vocabulary:
            if k==row[1]:
                dict4[row[0]]=dict3[row[1]]
            
    document=ast.literal_eval(dict4[listWords[0]])         
    #interection between every list in values dict4. In this way we have documnets_id where all words (in query input) are present
    for value in dict4.values():
        document=intersection(document,ast.literal_eval(value))
    print(document)
    

#build the dataframe with info for every documents_id
df=pd.DataFrame(columns=['title', 'intro', 'url'])
for index in range(len(document)):
    #get id of documnets_is
    numberDocument=document[index][9:]
    #get wikipedia url
    url=listUrl_Movies3[int(numberDocument)]
    name="aritcle_"
    extension2=".tsv"
    index=int(numberDocument)
    file="{}{}{}".format(name,index,extension2)
    #get info about title and intro for evert film that corresponds to every documents_id
    with open('tsv/'+file, 'r', newline='') as f_output:
        tsv_index = list(csv.reader(f_output, delimiter='\t'))
        title=tsv_index[1][3]
        intro=tsv_index[1][1]
        film=[title,intro,url]
        #put all info for every film in a single row of df dataframe
        df.loc[index] = film

