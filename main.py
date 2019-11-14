#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import random
import csv
import sys
import ast
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
f = open("/Users/digitalfirst/Desktop/HW3 ADM/movies3.html")

soup = BeautifulSoup(f)
listUrl_Movies3=[]
for link in soup.select('a'):
    listUrl_Movies3.append(link.text)





#define function that allows us to calculate a list that is an intersection from two list
def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 
def getDocuments(words,index):


    #we use dict3 to store term_id and its respective documents_id
    dict3={}
    ##we use dict4 to store evry word and its respective documents_id
    dict4={}
    csv.field_size_limit(sys.maxsize)
    #in listWords we have a list that contains all words about inout query
    listWords = words.split()
    listWords=[x.lower() for x in listWords]
    
    #with vocabulary.tsv we start to build a dict3 with term_id for every words in wordsList
    with open('HW3 ADM/tsv/vocobulary.tsv', 'r', newline='') as f_output:
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
        indexFile="index"+str(index)+".tsv"
        #we continue to match documnets_id to every term_id in dict3
        with open('HW3 ADM/tsv/'+indexFile, 'r', newline='') as f_output:
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
        #print(document)
    return document




def searchEngine1(words):
        #build the dataframe with info for every documents_id
    document=getDocuments(words,1)
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
        with open('HW3 ADM/tsv/'+file, 'r', newline='') as f_output:
            tsv_index = list(csv.reader(f_output, delimiter='\t'))
            title=tsv_index[1][3]
            intro=tsv_index[1][1]
            film=[title,intro,url]
            #put all info for every film in a single row of df dataframe
            df.loc[index] = film
    return df



def getTfidf_query(query):


    vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
      
    vectors = vectorizer.fit_transform([query])
        #print(vectors)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df_query = pd.DataFrame(denselist, columns=feature_names)
    return df_query

def getTfidf_document(words,document_id):
    dict={}
    
    listWords = words.split()
    listWords=[x.lower() for x in listWords]
    #print(listWords)
    df=pd.DataFrame(columns=listWords)
    tfIdf=[]
    with open('HW3 ADM/tsv/vocobulary.tsv', 'r', newline='') as f_output:
        tsv_vocabulary = list(csv.reader(f_output, delimiter='\t'))
        with open('HW3 ADM/tsv/index2.tsv', 'r', newline='') as f_output:
            tsv_index = list(csv.reader(f_output, delimiter='\t'))

        for word in listWords:
            listDoc=[]
            #print("word " + word)
            for row in tsv_vocabulary:
                if word.lower()==row[0]:
                    term=row[1]
                    #print("teerm" + str(term))
                    break
            for row in tsv_index:
                if term==row[0]:

                    listDoc=ast.literal_eval(row[1])

                    #print(listDoc)
                    break
            for index in listDoc:

                #print(index)
                if index[0]==document_id:
                    #print(index[0])

                    tfIdf.append(index[1])
                    #print(index[1])
                    break

        df.loc[0]=tfIdf
        df=df.reindex(sorted(df.columns), axis=1)
        return df

          


def coisine(list_query,list_document):
    
    res=(cosine_similarity([list_query,list_document]))
    #print(res)
    return res[0][1]


def searchEngine2(words):
    #build the dataframe with info for every documents_id
    document=getDocuments(words,1)
    df_query=getTfidf_query(words)
    df=pd.DataFrame(columns=['title', 'intro', 'url','similarity'])

    for index in range(len(document)):
        #get id of documnets_is
        df_document=getTfidf_document(words,document[index])
        #print(df_document)
        list_query=list(df_query.loc[0])
        #print(list_query)
        list_document=list(df_document.loc[0])
        #print(list_document)
        similiarity=coisine(list_document,list_query)
        #print("simi "+ str(similiarity))
        numberDocument=document[index][9:]
        #get wikipedia url
        url=listUrl_Movies3[int(numberDocument)]
        name="aritcle_"
        extension2=".tsv"
        index=int(numberDocument)
        file="{}{}{}".format(name,index,extension2)
        #get info about title and intro for evert film that corresponds to every documents_id
        with open('HW3 ADM/tsv/'+file, 'r', newline='') as f_output:
            tsv_index = list(csv.reader(f_output, delimiter='\t'))
            title=tsv_index[1][3]
            intro=tsv_index[1][1]
            film=[title,intro,url,similiarity]
            #put all info for every film in a single row of df dataframe
            df.loc[index] = film
            df=df.sort_values(by=['similarity'],ascending=False)
    return df


def search3(query):
    
    document=getDocuments2(query,3)
    listWords = query.split()
    listWords=[x.lower() for x in listWords]
    df=pd.DataFrame(columns=['title', 'intro', 'plot', 'music', 'score'])
    df_score=pd.DataFrame(columns=['title_score', 'intro_score', 'plot_score', 'music_score'])
    scores=[0.8,0.4,0.3,0.6]
    df_score.loc[0]=scores

    for index in range(len(document)):
        score=0
        #get id of documnets_is
        numberDocument=document[index][9:]
        #get wikipedia url
        url=listUrl_Movies3[int(numberDocument)]
        name="aritcle_"
        extension2=".tsv"
        index=int(numberDocument)
        file="{}{}{}".format(name,index,extension2)
        #get info about title and intro for evert film that corresponds to every documents_id
        with open("HW3 ADM/tsv_correct/"+file,"r") as tsvfile:
                    tsv_index = list(csv.reader(tsvfile, delimiter='\t'))
                    title=ast.literal_eval(tsv_index[1][3])
                    
                    intro=ast.literal_eval(tsv_index[1][1])

                    plot=ast.literal_eval(tsv_index[1][2])
                    
                    music=ast.literal_eval(tsv_index[1][8])
                   
                    
                    if (all(elem in title  for elem in listWords)) or (all(elem in listWords  for elem in title)):
                            score+=df_score.loc[0]['title_score']
                            print('title')
                    if all(elem in intro  for elem in listWords)==True:
                            score+=df_score.loc[0]['intro_score']
                            
                    if all(elem in plot  for elem in listWords)==True:
                            score+=df_score.loc[0]['plot_score']
                            
                    if any(elem in music  for elem in listWords)==True:
                        
                        score+=df_score.loc[0]['music_score']
                    

        with open('HW3 ADM/tsv/'+file, 'r', newline='') as f_output:
            tsv_file = list(csv.reader(f_output, delimiter='\t'))
            title2=tsv_file[1][3]
            intro2=tsv_file[1][1]
            plot2=tsv_file[1][2]
            music2=tsv_file[1][8]
            film=[title2,intro2,plot2,music2,score]
            df.loc[index] = film
           

    ndf=df.sort_values('score', ascending=False)
    scores
            #print(dict4.keys())
    return ndf



def searchEngine(query, num_search):
    if num_search==1:
        searchEngine1(query)
    elif num_search==2:
        searchEngine2(query)
    elif num_search==3:
        searchEngine3(query)
    else:
        print("error number search engine. Insert 1,2 or 3.")
        
        
query='life 2019 horror story'
searchEngine(query, 2)

