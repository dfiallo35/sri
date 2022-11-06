import re
from os.path import isfile
import numpy as np

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
    weight = get_term_weight(tf, idf)
    ranking = get_ranking(weight, documents)



#given a query return the list of terms
def get_terms(query:str):
    return re.findall(r'\w+', query)


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
            # tf[j].append(0)
            # tf[j][i]=terms_frequency[i][j]/max(terms_frequency[i])
            tf[j].append(terms_frequency[i][j]/max(terms_frequency[i]))
            if(terms_frequency[i][j]!=0):
                count_ni+=1        
        idf.append(np.log(len(terms_frequency)/count_ni))  
    return tf,idf
    

#given tf and idf return the weight of a term in a document
def get_term_weight(tf, idf):
    """
    :param tf: matrix tf of terms in documents
    :param idf: inverse document frequency
    :return: weight of a term in a document
    """    
    w=[]
    # for j in range(len(tf[0])):
    #     w.append([])
    #     w[j]=[]
    #     for i in range(len(tf)):
    #         w[j].append(tf[i][j]*idf[i])

    for j in range(len(tf[0])):
        w.append([])
        w[j]=[(tf[i][j]*idf[i]) for i in range(len(tf))]
        # for i in range(len(tf)):
        #     w[j].append(tf[i][j]*idf[i])
    return w

    


#calculate the similarity and return the ranking of documents
def get_ranking(weight, documents):
    """
    :param weight: matrix of weights of terms in documents
    :param documents: list of documents
    """

    raise NotImplementedError

