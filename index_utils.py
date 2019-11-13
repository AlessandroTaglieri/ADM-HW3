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
                    #deleting puntuaction and other symbols
                    row[i] = tokenizer.tokenize(row[i])
                    #remove duplicate elements and case-insensitive elements
                    row[i]= list(set(map(str.lower, row[i])))
                    #row[i] = row[i].translate({ord(c): None for c in string.punctuation})

                tsvwriter.writerow(row)
            
            
            
            
import string

from shutil import move
from nltk.tokenize import RegexpTokenizer
#create tsv file in 'tsv_correct2' directory wehere we have preprocessed the tsv file (just created in parser.py). These preprocessed files contain preprocessed texts.
#The difference between these tvs files and other tsv files in tsv_correct is that these files contains duplicates words in texts. It's important for the second search engine
def createTsvFile_Search2(listUrl_Movies3):
    
    tokenizer = RegexpTokenizer(r'\w+')
    name="aritcle_"
    extension2=".tsv"
    exclude = string.punctuation
    for index in range(len(listUrl_Movies3)):

        file="{}{}{}".format(name,index,extension2)
        with open("tsv/"+file,"r") as tsvfile, open("tsv_correct2/"+file,"w") as outfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            tsvwriter = csv.writer(outfile, delimiter="\t")
            for row in tsvreader:
                for i in range(len(row)):
                    #deleting puntuaction and other symbols
                    row[i] = tokenizer.tokenize(row[i])
                    #remove duplicate case-insensitive elements
                    row[i]= list(map(str.lower, row[i]))
                    #row[i] = row[i].translate({ord(c): None for c in string.punctuation})             
                tsvwriter.writerow(row)

