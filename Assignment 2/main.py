from alive_progress import alive_bar

import os
import re
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
ps = PorterStemmer()

# import nltk
# nltk.download('stopwords')

#returns a list of words in the file
def parse_file(address: str):
    f = open(address)

    flag = 0
    content = []
    for x in f.readlines():
        # print(x)
        if x == "</TEXT>\n":
            flag = 0

        if flag == 1 and x!='\n':
            for y in re.findall('[a-zA-Z]+',x):
                # content.append([ps.stem(y.lower()), f" {y.lower()}"])
                content.append(y.lower())

        if x == "<TEXT>\n":
            flag = 1
        
    return content

files = []

# uncomment this path for complete indexing for dataset
# path = "/home/nitin/Desktop/IR/Assignment 2/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/"
path = "/home/nitin/Desktop/IR/Assignment 2/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/2004_utf8/atleisure/"
for root, d_names, f_names in os.walk(path):
    for f in f_names:
        files.append(os.path.join(root, f))

#index will be a dictionary where key is the terms and keyvalues will again be a dictionary which will contain document as key and term frequency as an key value for that document
ind = dict() 


with alive_bar(len(files), bar = 'bubbles', spinner = 'notes2') as bar:
    for x in files:
        content = parse_file(x)

        #Remove stop words and insert stemmed word in index
        for word in content:
            stemmed_word = ps.stem(word)
            if word not in stopwords.words('english'):
                if stemmed_word in ind.keys():
                    # print(x, ps.stem(word))
                    if x in ind[stemmed_word]:
                        ind[stemmed_word][x]+=1
                    else:
                        ind[stemmed_word][x] = 1

                else:
                    ind[stemmed_word] = dict({x: 1})

        bar()

#returns set of docs according to the query words and operator
def boolean_ret(query_words: list, operator):
    ret = set()
    f = 0
    for word in query_words:
        stemmed_word = ps.stem(word)
        if operator=='|':
            try:
                ret.update(ind[stemmed_word].keys())
            except:
                pass
        elif operator=='&':
            try:
                if f == 0:
                    ret = set(ind[stemmed_word].keys())
                    f = 1
                ret = ret.intersection(set(ind[stemmed_word].keys()))

            except:
                ret = set()
                f = 1

    return ret

#prints term frequency 
def tf(term):
    try:
        print("term freq for respecive docs: ", ind[ps.stem(term)])
    except:
        print("term not found")

def doc_f(term):
    try:
        print("doc freq: ", len(ind[ps.stem(term)]))
    except:
        print("doc freq: ", 0)


print(boolean_ret(["voice", "oscar"], '&'))
doc_f("oscar")