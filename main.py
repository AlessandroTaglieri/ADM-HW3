

#import libraries
from bs4 import BeautifulSoup
import random
import csv
import sys
import ast
import heapq
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx 
from operator import itemgetter
import matplotlib.pyplot as plt

# Get a list of Wikipedia URLs from movies1.html/ movies2.html/ movies3.html
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
#Merge these 3 list in single list that contains all 30 000 urls
totalMovies=listUrl_Movies1+listUrl_Movies2+listUrl_Movies3


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
    with open('HW3 ADM/tsv/vocabulary.tsv', 'r', newline='') as f_output:
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
        #return "no results" if any query words isn't at least in one document
        for i in dict4.values():
            if not i:
                error='No results'
                return error
        #interection between every list in values dict4. In this way we have documnets_id where all words (in query input) are present
        for value in dict4.values():
            document=intersection(document,ast.literal_eval(value))
        
    return document

#SEARCH 1:

def searchEngine1(words):
        #build the dataframe with info for every documents_id
    document=getDocuments(words,1)
    if document=='No results':
        return document
    df=pd.DataFrame(columns=['title', 'intro', 'url'])
    for index in range(len(document)):
        #get id of documnets_is
        numberDocument=document[index][9:]
        #get wikipedia url
        url=totalMovies[int(numberDocument)]
        
        name="article_"
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

#SEARCH2:

#This 'getTfidf_query' function allow to calculate TfIdf value about input query.

def getTfidf_query(query):
    vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
      
    vectors = vectorizer.fit_transform([query])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df_query = pd.DataFrame(denselist, columns=feature_names)
    return df_query


#This 'getTfidf_document' function allow to get TfIdf about every word in query for a specific document.

def getTfidf_document(words,document_id):
    dict={}
    
    listWords = words.split()
    listWords=[x.lower() for x in listWords]
    #print(listWords)
    df=pd.DataFrame(columns=listWords)
    tfIdf=[]
    with open('HW3 ADM/tsv/vocabulary.tsv', 'r', newline='') as f_output:
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



#'coisine' function allow to calculate coisine similairity from two list of TfIdf values.

def coisine(list_query,list_document):
    
    res=(cosine_similarity([list_query,list_document]))
    #print(res)
    return res[0][1]

#function that execute search2
def searchEngine2(words):
    #build the dataframe with info for every documents_id
    document=getDocuments(words,1)
    
    if document=='No results':
        return document
    df_query=getTfidf_query(words)
    df=pd.DataFrame(columns=['title', 'intro', 'url','similarity'])

    for index in range(len(document)):
        #get id of documnets_is
        
        df_document=getTfidf_document(words,document[index])
        
        
        #get Tfidf list from df_query dataframe
        list_query=list(df_query.loc[0])
        #get Tfidf list from df_document dataframe
        list_document=list(df_document.loc[0])
        
        similiarity=coisine(list_document,list_query)
        
        numberDocument=document[index][9:]
        #get wikipedia url
        url=listUrl_Movies3[int(numberDocument)-20000]
        name="article_"
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


#These following function 'heapSortK' allow us to use a heap data structure (using heapq library) for maintaining the top-k documents. This function has a list and a k value. This value is the number of ordered results that we want to show

def heappush(h, item, key=lambda x: x):
    heapq.heappush(h, (key(item), item))

def heappop(h):
    return heapq.heappop(h)[1]

def heapify(h, key=lambda x: x):
    for idx, item in enumerate(h):
        h[idx] = (key(item), item)
    heapq.heapify(h)
def heapFunction(a,k): 
    df=pd.DataFrame(columns=['title', 'intro', 'plot', 'music','starring', 'score'])
    result=[]
    h = []
    for item in a:
        heappush(h, item, key=itemgetter(-1))
    #print(h)
    while h:
        result.append(heappop(h))
    
    
    j=0    #print(result)
    result.reverse()
    
    for i in range(k):
      
        if len(a)>i:
            
            df.loc[j] = result[i]
            j+=1
        else:
            break
    return df


#With this following function 'graph' we did the bonus section. This function has a nested list of actor, as parameter, about every film in results of search3. 

def graph(listMovies):
    G = nx.Graph() 
    couple=[]
    count=0
    for i in range(len(listMovies)):
        for j in range(len(listMovies[i])):
            for y in range(1,len(listMovies[i])):
                couple=[listMovies[i][j],listMovies[i][y]]
                count=0
                for k in listMovies:
                    if (couple[0] in k) and (couple[1] in k):
                        
                        count+=1
                        if count>=2 and not couple[0] == couple[1]:
                            
                            G.add_edge(couple[0],couple[1])
                            break
     
 
    
    if not nx.is_empty(G):
        pos = nx.spring_layout(G)   #<<<<<<<<<< Initialize this only once
        nx.draw(G,pos=pos, with_labels=True, node_size = 100, font_size=10)
        nx.draw_networkx_nodes(G,pos=pos, with_labels=True, node_size = 1500, font_size=10)
        nx.draw_networkx_edges(G, pos, alpha=0.3)#<<<<<<<<< pass the pos variable
        #plt.draw() 
        plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
         # To plot the next graph in a new figure
        plt.show()

#SEARCH3:

def searchEngine3(query,k):
    
    document=getDocuments(query,3)
    if document=='No results':
        
        return document
    listWords = query.split()
    listWords=[x.lower() for x in listWords]
    df=pd.DataFrame(columns=['title', 'intro', 'plot', 'music','starring', 'score'])
    #Create datarame that indicates score for every section.
    df_score=pd.DataFrame(columns=['title_score', 'intro_score', 'plot_score', 'music_score'])
    scores=[0.8,0.4,0.3,0.6]
    df_score.loc[0]=scores
    resultMovies=[]
    actors=[]
    
    for index in range(len(document)):
        score=0
        lista=[]
        #get id of documnets_is
        numberDocument=document[index][9:]
        #get wikipedia url
        url=listUrl_Movies3[int(numberDocument)-20000]
        name="article_"
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
                    #actors.append(tsv_index[1][7])
                    
                    if (all(elem in title  for elem in listWords)) or (all(elem in listWords  for elem in title)):
                            score+=df_score.loc[0]['title_score']
                            
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
            listActors=ast.literal_eval(tsv_file[1][7])
            actors=listActors
            film=[title2,intro2,plot2,music2,actors,score]
            resultMovies.append(film)
            
            
       
    df=heapFunction(resultMovies,k)
    actorsGraph=[]
    for index, row in df.iterrows():
        actorsGraph.append(row['starring'])
    
    graph(actorsGraph)
    return df




#FUNCTION THAT ALLOW TO CHOOSE WHICH SEARCH WE WANT EXECUTEAND THEIR RESPECTIVE PARAMETERS

def searchEngine(query, num_search, *k):
    if num_search==1:
        return searchEngine1(query)
    elif num_search==2:
        
        return searchEngine2(query)
    elif num_search==3:
        if k:
            return searchEngine3(query,k)
        else:
            print('insert third parameter K to define top-k document about search3')
    else:
        print("error number search engine. Insert 1,2 or 3.")
        
#EXECUTE QUERY_: REMEMBER TO INSERT K VALUES IN 3RD ARGUMENT ONLY IF YOU CHOOSE SEARCH3
#EXAMPLE: searchEngine(QUERY, SEARCH NUMBER, K)

query='United States Mark Strong '
df = searchEngine(query, 1)
df

