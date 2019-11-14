import ast
from itertools import islice
import csv

#CREATEB INDEX3              

dict2 = {}
count=0
present=False
with open('HW3 ADM/tsv/vocobulary.tsv', 'r', newline='') as f_output:
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
            with open("HW3 ADM/tsv_correct/"+file,"r") as tsvfile:
                data_list = list(csv.reader(tsvfile, delimiter="\t"))
                tsvreader = csv.reader(tsvfile, delimiter="\t")
                intro=data_list[1][1]
                intro = ast.literal_eval(intro)
                plot=data_list[1][2]
                plot = ast.literal_eval(plot)
                music=data_list[1][8]
                music = ast.literal_eval(music)
                text=plot+intro+music
                text= list(set(map(str.lower, text)))
                
                #for evry words in plot adn intro (for every page) we get every word. From every word we get its term_id and put it whit their occurences (document_id) in dict2
                for i in text:
                    for row in tsv_vocabulary:
                        if i==row[0]:
                            doc="document_"
                            name2="{}{}".format(doc,index)
                            
                            dict2[row[1]].append(name2)
                            break
                        else:
                            continue
                            
        #put dict2 in index.tsv file. In. evry row we have a single term_id with occurences of respective word.
        with open('HW3 ADM/tsv/index3.tsv', 'w', newline='') as f_output:
            tsv_vocabulary = csv.writer(f_output, delimiter='\t')           
            for key, val in dict2.items():
                tsv_vocabulary.writerow([key, val])           
                    


#FUNCTION THAT GIVE US DOCUMENT FOR SEARCH ENGINE 3

import csv
import sys
import ast
#define function that allows us to calculate a list that is an intersection from two list
def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 
def getDocuments2(words):


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

        #we continue to match documnets_id to every term_id in dict3
        with open('HW3 ADM/tsv/index3.tsv', 'r', newline='') as f_output:
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


#SEARCH 3



import pandas as pd
def search3(query):
    
    document=getDocuments2(query)
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










#EXECUTE SEARCH3

query='Levi'
search3(query)

