 
import re
from os import getcwd, listdir
from os.path import isfile, join, isdir
from math import log
import numpy as np

def split_words(text:str):
    return re.findall(r'\w+', text)


def sim(dj, q):
    result = 0
    dj_norm = np.linalg.norm(dj)
    q_norm = np.linalg.norm(q)
    for i in range(0,min(len(dj),len(q))):
        result +=  dj[i]*q[i]
    return (result / (dj_norm * q_norm))

def __get_count(elements:list):
        """
        Get the frequency of the terms in the query and store it in a dictionary of key as term and value as frequency
        :param terms: list of terms
        :return: dictionary with terms and their frequency
        """
        count= dict()
        for element in elements:
            count[element]= elements.count(element)
        return count

def get_split_terms(document:str):
    """
    Get the terms of the document that are not stopwords and store it in a list
    :param document: document to split
    :return: list of terms
    """
    doc= split_words(document)
    return doc

terms={}
docs=[]
for i, doc in enumerate(["papa quiere mas pan","yas mofd sdfno onfd","adnfsd idsbfid iudbf pan"]):

    docs.append(doc)
    if False:
        terms_freq= self.__get_count(self.get_split_terms(doc['text']))
    else:
        terms_freq= __get_count(get_split_terms(doc))

    # terms_documets_list[i]=[]
    for term in terms_freq:
        if not terms.__contains__(term):
            terms[term]={}
        terms[term][doc]=terms_freq[term]
        ###########################################recordar que en la matriz hay que agregar tambien los documentos aunque no esten con valor 0
terms_documets_list = []
for i,term in enumerate(terms):
    terms_documets_list.append([])
    for j in range(docs.__len__()):
        if(not terms[term].__contains__(docs[j])):
            terms_documets_list[i].append(0)
        else :
            terms_documets_list[i].append(terms[term][docs[j]])
    # for i,doc in enumerate(terms[term]):
    #     terms_documets_list[i].append(terms[term][doc])

terms_docs_matrix = np.array(terms_documets_list)
# print(terms_docs_matrix)
# T:np.array
# DT:np.array
T, S, DT = np.linalg.svd(terms_docs_matrix)
# print("\n T:",T,"\n S:",np.diag(S),"\n DT:",DT)
print(len(T))
#reducir a la dimension k calculada

# print("\n")
# print("Tk: ")
# print(T)
# print("\n")
# print("Sk: ")
# print(S)
# print("\n")
# print("DTk: ")
# print(DT)


#dimensionality reduction
S = np.diag(S)
print(len(S))
k=int((len(S)+1)/2)

Tk = T[0:len(T),0:k]
Sk = S[0:k,0:k]
DTk = DT[0:k,0:len(DT)]

print("\n")
print("Tk: ")
print(Tk)
print("\n")
print("Sk: ")
print(Sk)
print("\n")
print("DTk: ")
print(DTk)
print("\n")


#query vector in the reduced 2-dimensional space
q=np.array([0,0,0,1,1,1,0,2,0,1,0])
# q2 = np.dot(np.dot(np.linalg.inv(Sk),Tk.transpose()),q)
print(q.shape,DTk.shape,Tk.shape,Sk.shape)
qk=np.dot(np.dot(q.transpose(),Tk),np.linalg.inv(Sk))
# q2 = np.dot(np.dot(np.linalg.inv(Sk),Tk.transpose()),q)

print("\n")
print("qk: ")
print(qk)
print(np.round(qk,4))


# print("\n")
# print("q2: ")
# print(np.round(q2,4))

#documents vectors in the reduced 2-dimensional space
# d= [ [ np.array([[DTk[0,0]], [DTk[1,0]]]) for ] for ]

def doc_sim(dj, q):
    result = 0
    dj_norm = np.linalg.norm(dj)
    q_norm = np.linalg.norm(q)
    for i in range(0,min(len(dj),len(q))):
        result +=  dj[i]*q[i]
    return (result / (dj_norm * q_norm))


docs_sim={}
doc_vectors={}
for i,doc in enumerate(docs):
    doc_vectors[doc]=np.array([[DTk[j,i]] for j in range(k)])
    docs_sim[doc]=doc_sim(doc_vectors[doc],qk)[0]
    # doc_vectors.append(doc:np.array([[DTk[j,i] for j in range(k)]]))

d1 = np.array([[DTk[0,0]], [DTk[1,0]]])
d2 = np.array([[DTk[0,1]], [DTk[1,1]]])
d3 = np.array([[DTk[0,2]], [DTk[1,2]]])

print("\n")
print("d1: ",d1)
print("\n")
print("d2: ",d2)
print("\n")
print("d3: ",d3)
print("\n")
print("doc vector: ",doc_vectors)
print("\n")



#Rank documents by calculating the query-document cosine similarities.
sim1 = np.round(sim(d1,qk),5)
sim2 = np.round(sim(d2,qk),5)
sim3 = np.round(sim(d3,qk),5)


# for i,doc in enumerate(docs):
#     docs_sim[doc]=doc_sim(doc_vectors[doc],qk)[0]
print("\n")
print("sim:", docs_sim)

print("\n")
print("sim1: ",sim1)
print("\n")
print("sim2: ",sim2)
print("\n")
print("sim3: ",sim3)
print("\n")


# for i in range(len(doc_vectors)):
#     sim = np.round(sim(doc_vectors[i],qk),5)
#     print("sim",i,": ",sim)
#     print("\n")




# doc_sim={}
# for i,doc in enumerate(docs):
#     doc_sim[doc]=np.round(sim(doc_vectors[doc],qk),5)

# print(doc_sim)

# print("\nsim(q,d1): ")
# print(sim1)
# print("\nsim(q,d2): ")
# print(sim2)
# print("\nsim(q,d3): ")
# print(sim3)
