#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import string
import ast
from itertools import islice
import csv
from nltk.tokenize import RegexpTokenizer

#create tsv file in 'tsv_correct' directory wehere we have preprocessed the tsv file (just created in parser.py)
tokenizer = RegexpTokenizer(r'\w+')
name="aritcle_"
extension2=".tsv"
exclude = string.punctuation
for index in range(len(listUrl_Movies3)):



    file="{}{}{}".format(name,index,extension2)
    with open("tsv/"+file,"r") as tsvfile, open("tsv_correct/"+file,"w") as outfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        tsvwriter = csv.writer(outfile, delimiter="\t")
        for row in tsvreader:
            for i in range(len(row)):
                #take every words, deleting ountuaction and other symbols
                row[i] = tokenizer.tokenize(row[i])
                #remove duplicate case-insensitive elements
                row[i]= list(set(map(str.lower, row[i])))
                #row[i] = row[i].translate({ord(c): None for c in string.punctuation})
                
            tsvwriter.writerow(row)
            
            
           
        
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


                
                

#create index and save it on index.tsv                

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
                            
        #put dict2 in index.tsv file. In. evry row we have a single term_id with occurences of respective word.
        with open('tsv/index.tsv', 'w', newline='') as f_output:
            tsv_vocabulary = csv.writer(f_output, delimiter='\t')           
            for key, val in dict2.items():
                tsv_vocabulary.writerow([key, val])           
                    

