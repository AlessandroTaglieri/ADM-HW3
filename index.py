#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import index_utils
import string
import ast
from itertools import islice
import csv
from bs4 import BeautifulSoup
import requests
import time
import random
f = open("/Users/digitalfirst/Desktop/HW3 ADM/movies3.html")
soup = BeautifulSoup(f)
listUrl_Movies3=[]
for link in soup.select('a'):
    listUrl_Movies3.append(link.text)

#call function that creates tsv files where there are texts without puntuaction and duplicate words. It is on parser_utils.py
index_utils.createTsvFile_Search1(listUrl_Movies3)

#create vocabulary and save it on vocabulary.tsv

dict1 = dict()
term_id=0
present=False
with open('tsv/vocobulary.tsv', 'w', newline='') as f_output:
        tsv_vocabulary = csv.writer(f_output, delimiter='\t')
        tsv_vocabulary.writerow(['word','term_id'])
        name="aritcle_"
        extension2=".tsv"
        h=0
        for index in range(len(listUrl_Movies3)):
            h+=1
            print(h)
            file="{}{}{}".format(name,index,extension2)
            with open("tsv_correct/"+file,"r") as tsvfile:
                data_list = list(csv.reader(tsvfile, delimiter="\t"))
                tsvreader = csv.reader(tsvfile, delimiter="\t")
                #put in intro a list of all words that we have in intro of i-th page
                intro=data_list[1][2]
                intro = ast.literal_eval(intro)
                #put in plot a list of all words that we have in plot of i-th page
                plot=data_list[1][1]
                plot = ast.literal_eval(plot)
                
                #put in text, a list that contains all words that are in plot and word for every page (no duplicate)
                text=plot+intro
                text= list(set(map(str.lower, text)))
                
                #put in dict1 every words with its term_id (no duplicate)
                for i in text:
                    if i in dict1:    
                        continue
                    else:
                        dict1[i]=term_id
                        term_id+=1
                
        #put dict1 element in vocabulary.tsv file                
        for key, val in dict1.items():
                    tsv_vocabulary.writerow([key, val])



               

 #create index and save it on index2.tsv                

dict2 = {}
count=0
present=False
with open('tsv/vocobulary.tsv', 'r', newline='') as f_output:
        tsv_vocabulary = list(csv.reader(f_output, delimiter='\t'))
        name="aritcle_"
        extension2=".tsv"
        h=0
        for row in tsv_vocabulary:
            
            dict2[row[1]]=[]
        for index in range(len(listUrl_Movies3)):
            h+=1
            print(h)
            file="{}{}{}".format(name,index,extension2)
            with open("tsv_correct/"+file,"r") as tsvfile:
                data_list = list(csv.reader(tsvfile, delimiter="\t"))
                tsvreader = csv.reader(tsvfile, delimiter="\t")
                intro=data_list[1][1]
                intro = ast.literal_eval(intro)
                plot=data_list[1][2]
                plot = ast.literal_eval(plot)
                text=plot+intro
                text= list(set(map(str.lower, text)))
                
#for evry words in plot adn intro (for every page) we get every word. From every word we get its term_id and put it whit their occurences (document_id) in dict2

                for i in text:
                    for row in tsv_vocabulary:
                        if i==row[0]:
                            name="document_"+index
                            dict2[row[1]].append(name)
                            break
                        else:
                            continue
                            
        #put dict2 in index2.tsv file. In. evry row we have a single term_id with occurences of respective word.
        with open('tsv/index2.tsv', 'w', newline='') as f_output:
            tsv_vocabulary = csv.writer(f_output, delimiter='\t')           
            for key, val in dict2.items():
                tsv_vocabulary.writerow([key, val])           
#Finally, in index2.tsv we'll have our index that we'll use for the first search engine


#INDEX ABOUT SECOND SEARCH ENGINE
                    

import sys    
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

csv.field_size_limit(sys.maxsize)
               
#call function that creates tsv files where there are preprocessed texts. It is on parser_utils.py
index_utils.createTsvFile_Search2(listUrl_Movies3)

dict2 = {}
count=0
present=False
documents=[]
name='aritcle_'
extension2='.tsv'
with open('HW3 ADM/tsv/vocobulary.tsv', 'r', newline='') as f_output:
        tsv_vocabulary = list(csv.reader(f_output, delimiter='\t'))
        for index in range(0,10000):
            print(index)
            file="{}{}{}".format(name,index,extension2)
            with open("HW3 ADM/tsv_correct2/"+file,"r") as tsvfile:
                data_list = list(csv.reader(tsvfile, delimiter="\t"))
                tsvreader = csv.reader(tsvfile, delimiter="\t")
                intro=data_list[1][1]
                intro = ast.literal_eval(intro)
                plot=data_list[1][2]
                plot = ast.literal_eval(plot)
                text=plot+intro
                text=list(map(str.lower, text))
                documents.append(' '.join(text))
                #print(documents)
                # text2= list(set(map(str.lower, text)))
                
                
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        vectors = vectorizer.fit_transform(documents)
        #print(vectors)
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        denselist = dense.tolist()
        df2 = pd.DataFrame(denselist, columns=feature_names)


#create index and save it on index.tsv                
dict={}
dict2 = {}
count=0
present=False


name="aritcle_"
extension2=".tsv"
h=0
for row in tsv_vocabulary:
    h+=1
    dict[row[0]]=row[1]
    print(h)
    dict2[row[1]]=[]
for index in range(0,10000):
    print("numero documento "+ str(index))
    file="{}{}{}".format(name,index,extension2)
    with open("HW3 ADM/tsv_correct2/"+file,"r") as tsvfile:
        data_list = list(csv.reader(tsvfile, delimiter="\t"))
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        intro=data_list[1][1]
        intro = ast.literal_eval(intro)
        plot=data_list[1][2]
        plot = ast.literal_eval(plot)
        text=plot+intro
        text=list(map(str.lower, text))
    
        text2= list(set(map(str.lower, text)))
        
                        #for evry words in plot adn intro (for every page) we get every word. From every word we get its term_id and put it whit their occurences (document_id) in dict2
        for i in text2:

           
            res=df2.iloc[index][i]
                          
            for term in dict:
                if i==term:
                    print("key "+ str(term))
                    print("value "+ str(dict[term]))
                    doc="document_"
                    name2="{}{}".format(doc,index)
                    result=[name2,res]
                    dict2[dict[term]].append(result)
                    break
                else:
                    continue

            

#put dict2 in index.tsv file. In. evry row we have a single term_id with occurences of respective word.


with open('HW3 ADM/tsv/index.tsv', 'w', newline='') as f_output:
    tsv_index2 = csv.writer(f_output, delimiter='\t')           
    for key, val in dict2.items():
        tsv_index2.writerow([key, val])