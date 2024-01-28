from nltk.stem import PorterStemmer
from collections import Counter
import re
import os

ps = PorterStemmer()

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
                content.append(y.lower())

        if x == "<TEXT>\n":
            flag = 1
        
    return content


files = []
path = "/home/nitin/Desktop/IR/Assignment 1/english/en.doc.2010/English-Data/TELEGRAPH_UTF8/2004_utf8/atleisure"

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
    stemmed_words.add(ps.stem(x))
    words_without_stemming.add(x)

print("Before Stemming: " + str(len(words_without_stemming)))
print("After Stemming: " + str(len(stemmed_words)))
print("Difference: " + str(len(words_without_stemming) - len(stemmed_words)))