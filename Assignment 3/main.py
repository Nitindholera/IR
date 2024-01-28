from alive_progress import alive_bar

import os
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from math import log10

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

docs = []

# uncomment this path for complete indexing for dataset
# path = "/home/nitin/Desktop/IR/Assignment 2/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/"
path = "/home/nitin/Desktop/IR/Assignment 2/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/2004_utf8/atleisure/"
for root, d_names, f_names in os.walk(path):
    for f in f_names:
        docs.append(os.path.join(root, f))

#index will be a dictionary where key is the terms and keyvalues will again be a dictionary which will contain document as key and term frequency as an key value for that document
ind = dict() 


with alive_bar(len(docs), bar = 'bubbles', spinner = 'notes2') as bar:
    for x in docs:
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

def tf(term, doc):
    # print("term freq for respecive docs: ", ind[ps.stem(term)])
    try:
        return ind[ps.stem(term)][doc]
    except:
        return 0

def idf(term):
    try:
        return log10(len(docs)/len(ind[ps.stem(term)]))
    except:
        return 0

def sim(v1, v2):
    n = len(v1)
    val = 0
    for i in range(n):
        val += v1[i] * v2[i]
    return val

def vsm(query):
    q_ind = dict()
    for word in query.split():
        stemmed_word = ps.stem(word)
        if word not in stopwords.words('english'):
            if stemmed_word in q_ind.keys():
                q_ind[stemmed_word] +=1
            else:
                q_ind[stemmed_word] = 1
    q_terms = list(q_ind.keys())
    
    q_vec = []
    for term in q_terms:
        q_tf = 1+log10(q_ind[term])
        q_vec.append(q_tf*idf(term))
    
    results = {}
    for doc in docs:
        doc_vec = []
        for term in q_terms:
            tfidf = tf(term,doc) * idf(term)
            doc_vec.append(tfidf)
        results[doc] = sim(doc_vec, q_vec)
    final_result = sorted([(results[x],x) for x in results], reverse=True)

    print("Top 5 results are:")
    for x in final_result[:5]:
        print(x)


# print(tf("much", "/home/nitin/Desktop/IR/Assignment 2/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/2004_utf8/atleisure/1041207_atleisure_index.utf8"))
vsm("French fashion legend")
