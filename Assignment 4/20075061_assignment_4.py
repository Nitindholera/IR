import sys

# input result_file qrel_file and query_no from command line
result_file = open(sys.argv[1], 'r') 
qrel_file = open(sys.argv[2], 'r' , encoding='utf-8-sig')
query_no = int(sys.argv[3])

# store retrieved docs for given query in retrieved_docs list
retrieved_docs = []
for x  in result_file:
    if(query_no == int(x.split()[0])):
        retrieved_docs.append(int(x.split()[2]))

#store relevent docs for the given query in rel_docs set
rel_docs = set()
for x in qrel_file:
    if(int(x.split()[0]) == query_no and int(x.split()[3]) == 1):
        rel_docs.add(int(x.split()[2]))

#store precision at the points where an actual relevant document is found in precision_at_k list
precision_at_k = []
rel_doc_no_dynamic = 0
k = 0
for doc in retrieved_docs:
    k+=1
    if doc in rel_docs:
        # relevent document is found from the retrieved documents
        rel_doc_no_dynamic+=1
        precision_at_k.append(rel_doc_no_dynamic/k)

avg_precision = sum(precision_at_k)/len(rel_docs)
print(f"Average Precision for query {query_no} is: {avg_precision}")