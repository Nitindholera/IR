import os
from collections import Counter
from math import log10
import sys
def parse(doc, cat):
    f = open(doc)
    try:
        x = f.readlines()
        for line in x:
            collectionfreq[cat]+=len(line.split())
            for word in line.split():
                termfreq[(word,cat)]+=1
                vocab.add(word)
        f.close()
    except:
        print(f"warning :{doc} cant be read properly")


path = '20_newsgroups'
termfreq = Counter() #stores class wise term frequency
docfreq = Counter() #stores documents in a perticular class
collectionfreq = Counter() #stores total number of terms in a particular class
vocab = set() #stores number of unique words in the whole collection

for root, dirs, files in os.walk(path):
    if len(files):
        docfreq[root] += len(files)
        for file in files:
            f = os.path.join(root, file)
            parse(f, root)


def find_total_docs(docfreq):
    val = 0
    for fg in docfreq:
        val += docfreq[fg]
    
    return val

def find_cat(test_file):
    testf = open(test_file)
    x = testf.readlines()
    vocab_test_file = set()
    for word in vocab:
        vocab_test_file.add(word)
    for line in x:
        for word in line.split():
            vocab_test_file.add(word)

    probability = dict() #Probability of a category c for given test_file
    for cat in docfreq:
        val = 0
        for line in x:
            for word in line.split():
                val += log10((termfreq[(word, cat)] + 1)/(collectionfreq[cat] + len(vocab_test_file)))
        probability[cat] = log10(docfreq[cat] / find_total_docs(docfreq)) + val
    
    return max(probability, key=probability.get)

testfilepath = sys.argv[1]
out = open(sys.argv[2], "w")
for root, dirs, files in os.walk(testfilepath):
    for file in files:
        out.write(f"{file}, {find_cat(os.path.join(root, file))}\n")
out.close()