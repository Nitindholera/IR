import re
import os
from alive_progress import alive_bar
from bltk.langtools import remove_stopwords
from bangla_stemmer.stemmer import stemmer
bs = stemmer.BanglaStemmer()

def parse_file(address: str):
    f = open(address)

    flag = 0
    content = []
    try:      
        for x in f.readlines():
            # print(x)
            if x == "</TEXT>\n":
                flag = 0

            if flag == 1 and x!='\n' and x!='':
                for y in re.split("\s", x):
                    content.append(y)

            if x == "<TEXT>\n":
                flag = 1

    except:
        print(address+" has unsupported text encoding")
        
    return content


files = []
#uncomment this path for complete indexing for dataset
# path = "/home/nitin/Desktop/IR/Assignment 2/bengali/bn.docs.2012.19032012/"
path = "/home/nitin/Desktop/IR/Assignment 2/bengali/bn.docs.2012.19032012/bn_ABP/2001/aj-kol"
for root, d_names, f_names in os.walk(path):
    for f in f_names:
        files.append(os.path.join(root, f))

#index will be a dictionary where key is the terms and keyvalues will again be a dictionary which will contain document as key and term frequency as an key value for that document
ind = dict() 

with alive_bar(len(files), bar = 'bubbles', spinner = 'notes2') as bar:
    for x in files:
        content = parse_file(x)
        stemmed_content = []
        for word in content:
            stemmed_word = bs.stem(word)
            stemmed_content.append(stemmed_word)

        content = remove_stopwords(stemmed_content)

        for word in content:
            if word in ind.keys():
                    # print(x, ps.stem(word))
                    if x in ind[word]:
                        ind[word][x]+=1
                    else:
                        ind[word][x] = 1

            else:
                ind[word] = dict({x: 1})
        bar()


#returns set of docs according to the query words and operator
def boolean_ret(query_words: list, operator):
    ret = set()
    f = 0
    for word in query_words:
        stemmed_word = bs.stem(word)
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
        print("term freq for respecive docs: ", ind[bs.stem(term)])
    except:
        print("term not found")

def doc_f(term):
    try:
        print("doc freq: ", len(ind[bs.stem(term)]))
    except:
        print("doc freq: ", 0)

print(boolean_ret(["কোথাও", "অনেক", "মঙ্গলবার", "ভারতীয়", "সংবাদপত্রসেবী"], '&'))
print(doc_f("মঙ্গলবার"))