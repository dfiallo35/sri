from vector_model import *
import numpy as np


class LSI_Model(VectorModel):
    
    def __init__(self):
        super().__init__() 
        self.terms={}
        self.docs=[]
        self.terms_docs_matrix = None
        self.vector_query = []
    #no hay que cambiar nada en run ni en find, ni en ranking ni en query_data,
    #ni en umbral, ni en __get_query_terms_docs,, ni en los counts

    

    def __sim(self):
        """
        Calculate the similarity between the query and the documents and store it in the querysim dictionary
        :get queryterms: dictionary with query terms and their weight
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get querysim: empty dictionary to store documents and their similarity
        :return: dictionary with documents and their similarity"""

        T, S, DT = np.linalg.svd(self.terms_docs_matrix)
        S = np.diag(S)


    


    def __docterms_data(self, sensitive:bool):
        """
        Calculate the frequency, tf, idf and w of the terms in the documents and store it in the docterms dictionary
        :param documents: list of documents
        :get docterms: empty dictionary to store terms and their frequency, tf, idf and w
        :param sensitive: boolean to know if the search is sensitive or not
        """
        for i, doc in enumerate(self.dataset.get_docs_data()):
            self.docs.append(doc)
            if sensitive:
                terms_freq= self.__get_count(self.get_split_terms(doc['text']))
            else:
                terms_freq= self.__get_count(self.get_split_terms(doc['text'].lower()))
                 
            for term in terms_freq:  
                if not self.terms.__contains__(term):
                    self.terms[term]={}
                self.terms[term][doc]=terms_freq[term]
        
        terms_documets_list = []
        for i,term in enumerate(self.terms):
            terms_documets_list.append([])
            for j in range(len(self.terms[term])):
                if (not self.terms[term].__contains__(self.docs[j])):
                    terms_documets_list[i].append(0)
                else :
                    terms_documets_list[i].append(self.terms[term][self.docs[j]])
                        
        self.terms_docs_matrix = np.array(terms_documets_list)
        

    def __query_data(self, query:str, alpha:float):
        """
        Calculate the weight of the query terms and store it in the queryterms dictionary
        :param query: query to search
        :get queryterms: empty dictionary to store terms and their weight
        :param alpha: parameter to calculate w
        :return: dictionary with the query terms and their weight
        """
        terms= self.__get_query_terms_docs(query)
        terms_count= self.__get_count(terms)
        max= self.__get_max_count(terms_count)
        
        for term in terms_count:
            idf= 0
            for freq in self.docterms[term].values():
                idf= freq['idf']
            if max != 0:
                self.queryterms[term] = (alpha + (1 - alpha) * ((terms_count[term])/(max)))*idf
            else:
                self.queryterms[term] = 0
        return self.queryterms
    
    
    def __get_query_terms_docs(self, query:str):
        """
        Get the terms of the query and store it in a list
        :param query: query to search
        :return: list of terms
        """
        terms= []
        for term in self.get_split_terms(query):
            if self.docterms.get(term) != None:
                terms.append(term)
        return terms


    def __docterms_data(self, sensitive:bool):
        """
        Calculate the frequency, tf, idf and w of the terms in the documents and store it in the docterms dictionary
        :param documents: list of documents
        :get docterms: empty dictionary to store terms and their frequency, tf, idf and w
        :param sensitive: boolean to know if the search is sensitive or not
        """
        for doc in self.dataset.get_docs_data():
            if sensitive:
                terms_freq= self.__get_count(self.get_split_terms(doc['text']))
            else:
                terms_freq= self.__get_count(self.get_split_terms(doc['text'].lower()))
            
            max= self.__get_max_count(terms_freq)
            
            for term in terms_freq:
                if self.docterms.get(term) == None:
                    self.docterms[term] = {doc['id']:{'freq':terms_freq[term], 'tf':terms_freq[term]/max, 'idf':0, 'w':0}}
                else:
                    self.docterms[term][doc['id']] = {'freq':terms_freq[term], 'tf':terms_freq[term]/max, 'idf':0, 'w':0}
            
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = log(self.dataset.docslen / len(self.docterms[term]), 10)
                self.docterms[term][doc]['w'] = self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf']
    
