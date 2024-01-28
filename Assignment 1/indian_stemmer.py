#"/home/nitin/Desktop/IR/bengali/bn.docs.2012.19032012/bn_ABP/2007/desh/1070323_23desh11.pc.utf8" file has unsupported text encoding
from collections import Counter
import os, re
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
path = "/home/nitin/Desktop/IR/Assignment 1/bengali/bn.docs.2012.19032012/bn_ABP/2001"

for root, d_names, f_names in os.walk(path):
    for f in f_names:
        files.append(os.path.join(root, f))

ind = Counter()

for x in files:
    content = parse_file(x)
    ind.update(content)

stemmed_words = set()
words_without_stemming = set()

for x in ind:
    stemmed_words.add(bs.stem(x))
    words_without_stemming.add(x)

print("Before Stemming: " + str(len(words_without_stemming)))
print("After Stemming: " + str(len(stemmed_words)))
print("Difference: " + str(len(words_without_stemming) - len(stemmed_words)))