import re
from os import getcwd, listdir
from os.path import isfile, join, isdir
from math import log
import numpy as np

def split_words(text:str):
    return re.findall(r'\w+', text)



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
print(terms_docs_matrix)