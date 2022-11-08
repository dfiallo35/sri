import re
from os import getcwd
from os.path import isfile, join
import numpy as np
import operator



#given a query and a list of documents, returns a list of documents sorted by relevance
def vector_model(query:str, documents:list):
    """
    :param query: string
    :param documents: list of documents
    :return: list of documents sorted by relevance
    """

    terms = get_terms(query)
    terms_frequency = get_terms_frequency(terms, documents)
    tf, idf = get_tf_idf(terms_frequency)
    weight = get_terms_weight(tf, idf)
    wq = get_query_weight(terms,idf,0.5)
    sim=get_similarity(weight,wq)
    ranking = get_ranking(sim, documents)



#given a query return the list of terms
def get_terms(query:str):
    return re.findall(r'\w+', query)


def get_doc_terms(documents:list):
    pass



#Convert each letter of the terms to [(lowercase)(uppercase)]
def convert_to_lower_upper(terms: list):
    """
    :param terms: list of terms
    :return: list of terms converted to [(lowercase)(uppercase)]
    """
    outterms= []
    for term in terms:
        word=''
        for letter in term:
            word += '[' + letter.lower() + letter.upper() + ']'
        outterms.append(word)
    return outterms


def all_lower(terms: list):
    """
    :param terms: list of terms
    :return: list of terms converted to lowercase
    """
    outterms= []
    for term in terms:
        word=''
        for letter in term:
            word += letter.lower()
        outterms.append(word)
    return outterms


#given a list of terms and documents return the frequency matrix of terms in documents
def get_terms_frequency(terms:list, documents:list):
    """
    :param terms: list of terms
    :param documents: list of documents
    :return: matrix of frequency of terms in documents
    """
    terms_freq = []
    for doc in documents:
        if isfile(doc):
            _document = open(doc, 'r')
            doc_data = _document.read()
            _document.close()
            terms_freq_doc = re.findall('\\b' + '\\b|\\b'.join(convert_to_lower_upper(terms)) + '\\b', doc_data)
            terms_freq.append([terms_freq_doc.count(term) for term in all_lower(terms)])
            
        else:
            raise FileNotFoundError
    return terms_freq


#given the frequency matrix return the matrix of tf-idf of terms in documents
def get_tf_idf(terms_frequency:list):
    """
    :param terms_frequency: matrix of frequency of terms in documents
    :return: matrix of tf-idf of terms in documents
    """
    tf=[]
    idf=[]
    for j in range(len(terms_frequency[0])):
        count_ni=0
        tf.append([])
        tf[j]=[]
        for i in range(len(terms_frequency)):
            tf[j].append(terms_frequency[i][j]/(max(terms_frequency[i]) if  max(terms_frequency[i])>0 else 1))
            if(terms_frequency[i][j]!=0):
                count_ni+=1        
        idf.append(np.log(len(terms_frequency)/count_ni))  
    return tf,idf



#given tf and idf return the weight of each term in each document
def get_terms_weight(tf, idf):
    """
    :param tf: matrix tf of terms in documents
    :param idf: inverse document frequency
    :param alpha: smoothed, dampens the frequency of the term
    :return: weight of each term in each document
    """    
    w=[]
    for j in range(len(tf[0])):
        w.append([(tf[i][j]*idf[i]) for i in range(len(tf))])        
    return w


#given query and return the weight of each term in the query
def get_query_weight(terms,idf,alpha=0):
    """
    :param tf: matrix tf of terms in documents
    :param idf: inverse document frequency
    :param alpha: smoothed, dampens the frequency of the term
    :return: weight of a term in a document
    """    
    freq=[terms.count(term) for term in terms]    
    wq=[(alpha + (1-alpha) * freq[i] / max(freq)) * idf[i] for i in range(len(terms))]
    return wq


#calculate the similarity between the query and the documents
def get_similarity(weight,wq):
    """
    :param weight: matrix of weights of terms in documents
    :param wq: list of weights of terms in query
    """
    sim=[]
    for j in range(len(weight)):  
        sum1=sum2=sum3=0
        for i in range(len(weight[0])):
            sum1 += weight[j][i]*wq[i]
            sum2 += np.power(weight[j][i],2)
            sum3 += np.power(wq[i],2)
        sim.append(sum1 / (np.sqrt(sum2)*np.sqrt(sum3) if (np.sqrt(sum2)*np.sqrt(sum3)!=0) else 1))
    return sim
        

#calculate the ranking of documents
def get_ranking(similarity, documents):
    """
    :param similarity: 
    :param documents: list of documents
    """
    sim_docs = { documents[i]:similarity[i] for i in range(len(similarity))}   
    ranking_sim = sorted(sim_docs.items(), key=operator.itemgetter(1), reverse=True) 
    return [key for (key,value) in ranking_sim]
    
        
    

