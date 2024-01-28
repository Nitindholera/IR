import re
import os
from collections import Counter
import matplotlib.pyplot as plt
from math import log10
#returns a list of all the words in the file
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

frequency = []
for x in ind.most_common():
    frequency.append(log10(x[1]))
rank = []

for i, _ in enumerate(frequency):
    rank.append(log10(i+1))

plt.plot(rank,frequency)
plt.xlabel("log(rank)")
plt.ylabel("log(frequency)")
plt.savefig("rankvsfreq2.png")
plt.show()