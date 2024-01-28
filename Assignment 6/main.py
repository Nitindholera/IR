from bs4 import BeautifulSoup
import lxml
import requests
import numpy as np
from numpy import linalg as LA

def fetch(url):
    try:
        f = requests.get(url)
        return f.text
    except:
        return None

def extract_urls(data: str):
    soup = BeautifulSoup(data, 'lxml')
    urls = []
    for url in soup.find_all('a'):
        href = url.get('href')
        ancor_text = url.text
        if href and href.startswith('https'):
            urls.append(href)
    
    return urls

visited_urls = set()
mapping = dict() #key: url of a page, value: list of urls in that page
web_docs = []
def crawl(seed_url):
    if len(web_docs)>=max_size or seed_url in visited_urls:
        return

    print(seed_url)
    visited_urls.add(seed_url)
    data = fetch(seed_url)
    if data:
        web_docs.append((seed_url, data))
        urls = extract_urls(data)
        mapping[seed_url] = urls[:5]
        for url in urls[:5]:
            crawl(url)

#crawling
url = "https://en.wikipedia.org/wiki/Anime"
max_size = 100
crawl(url)


#Making Adjancency Matrix for web-graph using numpy
A = np.zeros((max_size, max_size))
doc_labels = []
for label, _ in web_docs:
    doc_labels.append(label)


for i in range(max_size):
    for j in range(max_size):
        if doc_labels[j] in mapping[doc_labels[i]]:
            A[i][j] = 1


#Page rank calculation
lambda_val = 0.15
P = np.zeros((max_size, max_size))
for i in range(max_size):
    row_sum = 0
    for j in range(max_size):
        row_sum += A[i][j]
    for j in range(max_size):
        if row_sum == 0:
            P[i][j] = 1/max_size + lambda_val/max_size
        else:           
            P[i][j] = lambda_val/max_size + (1-lambda_val)*(A[i][j]/row_sum)

#initial pagerank vector
X = np.array([1/max_size for x in range(max_size)])
epochs = 50


for _ in range(epochs):
    X = np.matmul(X, P)


#Hub and Authority Scores calculation
h = np.array([1/max_size for x in range(max_size)]) #initial hub scores
a = np.array([1/max_size for x in range(max_size)]) #initial authority scores

AAT = np.matmul(A, A.T) #AAtranspose matrix
ATA = np.matmul(A.T, A) #AtransposeA matrix

lambda_h = max(LA.eig(AAT)[0])
lambda_a = max(LA.eig(ATA)[0])
epochs = 50
for _ in range(epochs):
    h = (1/lambda_h) * np.matmul(AAT, h)
    a = (1/lambda_a) * np.matmul(ATA, a)


pageRank = dict()
HubScore = dict()
AuthorityScore = dict()

for i in range(max_size):
    pageRank[doc_labels[i]] = X[i]
    HubScore[doc_labels[i]] = h[i]
    AuthorityScore[doc_labels[i]] = a[i]

def giv_top_10(data: dict):
    v = []
    for i in data:
        v.append([data[i], i])
    v.sort(reverse=True)
    return v[:10]

print("Top 10 docs based on pagerank: ")
print(*giv_top_10(pageRank), sep="\n")

print("Top 10 docs based on hub scores: ")
print(*giv_top_10(HubScore), sep="\n")

print("Top 10 docs based on authority scores: ")
print(*giv_top_10(AuthorityScore), sep="\n")