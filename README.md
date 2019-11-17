

# Homework 3: What movie to watch tonight? - GROUP: 11
## Authors
* **Julia Nawaro**
* **Alessandro Taglieri**
* **Sabriye Ela Esme**

## Objective
Build a search engine over a list of movies that have a dedicated page on Wikipedia.


### Homework structure

The homework is divided into four parts: 

* **Data collection**
Write here
* **Search Engine**
Write here
* **Define a new score!**
Write here
* **Algorithmic question**
Write here

### Repository Structure

Our Repository contain the following files:

* **main.ipynb**
Containing all tasks that we implemented. It contains all description and comments about any decision. There is some example about all three search engines.
* **main.py**
It's a python file that once executed build up the search engine. It consist in a series of functions. To execute search engine, you can call searchEngine(query,number_search, k).
Query: input query that we want to search among all documents;
Number search: 1 for first search (Conjunctive query); 2 for second search (Conjunctive query & Ranking score); 3 for third search ( Define a new score!).
K: it's a optional parameter. You should insert this value when you want execute third search. K is a value that indicates a number of result that you want to show about this search (get top-k films).
* **collector.py**
Allow to download all wikipedia pages in html files.
* **parser.py**
Allow to parse evry html page and save some infos into different tsv files. We have three different tsv file that we save in three different directory.
tsv= it contains all tsv files with no-preprocessed texts
tsv_correct= it contains all tsv files with preprocessed texts.
tsv_correct2= it contains all tsv files with preprocessed texts. It contains also duplicate words. It's necessary about search3 to calculate TfIdf values.
* **index.py**
Allow to create vocabulary and index needed for the search engines. Indices are saved into three different tsv files.
Index1: it's an index that matches every word (expressed with its term_id) to a list of document (that contain respective word in intro/plot).
Index2: It's an index that matches every word (expressed with its term_id) to a list of document (taht contain respective word in intro/plot). For every document, there is TfIdf value for its document about specific word.
Index3: It's like index1. Here, every document can contain respective word also in title and music sections.
* **index_utils.py**
Containing functions that we used for creating indexes. These functions allow to create different tsv files that we used to create different indexes about all search engines.
* **README.md**
Containing the explaination of the content of the repository </br>


