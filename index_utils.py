#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import string
import ast
from itertools import islice
import csv
from nltk.tokenize import RegexpTokenizer

def createTsvFile_Search1(listUrl_Movies3):
    #create tsv file in 'tsv_correct' directory wehere we have preprocessed the tsv file (just created in parser.py)
    tokenizer = RegexpTokenizer(r'\w+')
    name="article_"
    extension2=".tsv"
    exclude = string.punctuation
    for index in range(totalMovies):
        print(index)


        file="{}{}{}".format(name,index,extension2)
        with open("HW3 ADM/tsv/"+file,"r") as tsvfile, open("HW3 ADM/tsv_correct/"+file,"w") as outfile:
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
            
            
            
            

#create tsv file in 'tsv_correct2' directory wehere we have preprocessed the tsv file (just created in parser.py). These preprocessed files contain preprocessed texts.
#The difference between these tvs files and other tsv files in tsv_correct is that these files contains duplicates words in texts. It's important for the second search engine
def createTsvFile_Search2(listUrl_Movies3):
    
    tokenizer = RegexpTokenizer(r'\w+')
    name="article_"
    extension2=".tsv"
    exclude = string.punctuation
    for index in range(totalMovies):
        print(index)


        file="{}{}{}".format(name,index,extension2)
        with open("HW3 ADM/tsv/"+file,"r") as tsvfile, open("HW3 ADM/tsv_correct2/"+file,"w") as outfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            tsvwriter = csv.writer(outfile, delimiter="\t")
            for row in tsvreader:
                for i in range(len(row)):
                    #take every words, deleting ountuaction and other symbols
                    row[i] = tokenizer.tokenize(row[i])
                    #remove duplicate case-insensitive elements
                    row[i]= list(map(str.lower, row[i]))
                    #row[i] = row[i].translate({ord(c): None for c in string.punctuation})

                tsvwriter.writerow(row)




                
                


            