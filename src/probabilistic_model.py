from base_model import Model
from utils import *
from dataset import Datasets
from stopwords import Stopwords
import numpy as np


class Probabilistic_model(Model):

    def __init__(self):
        super().__init__()
        
        # dictionary with keys as documents and values as lists of terms
        # self.doc_terms = dict()

        # number of docs in the collection
        self.N = 0

        # dictionary with keys as terms and values as lists of documents
        self.term_docs = dict()
        
        # list of terms of the query
        self.query_terms = []

    	# dictonary with the similarity between the query and documents
        self.query_doc_sim = dict()

        # dictionary with keys as terms and values as tuple 
        # with the first element as the number of documents in which the term appears
        # and the second element as the term frequency in the collection
        self.term_freq = dict()


    def __get_term_docs(self, sensitive: bool):
        """
        For each term saves a in a list the document in which it appears
        :param document: document from which the terms will be search analyzed
        :get doc_terms: dictionary in which the terms of the document are saved 
        :get terms_doc: dictionary in which the list of documents that contain the term will be saved
        """    
    
        for doc in self.dataset.get_docs_data():
            self.N = self.N + 1

            doc_split = []

            if sensitive:
                doc_split = self.get_split_terms(doc['text'])
            
            else:
                doc_split = self.get_split_terms(doc['text'].lower())

            self.__get_term_frequency(doc_split)

            # for term in list(set(doc_split)):
            for term in doc_split:
                if self.term_docs.get(term) == None:
                    self.term_docs = []
                    self.term_docs[term].append(doc)

                else:
                    if doc not in self.term_docs[term]:
                        self.term_docs[term].append(doc)


    def __query_terms(self, query: str):
        """
        Saves the query terms in a list
        :param query: the query string
        :get query_terms: list of query terms
        """

        for term in self.get_split_terms(query):
            if term not in self.query_terms:
                self.query_terms.append(term)
        # query_terms = list(set(self.get_split_terms(query)))


    def __sim_const(self):
        """
        Computes the similarity between the query and the documents from the collection
        takes as a constant value p_i = 0.5
        :get query_doc_sim: saves the similarity between the query and a documents
        """
        # p_i = 0.5

        for term in self.term_docs:
            n_i = len(self.term_docs[term])
            r_i = n_i / self.N
            
            for doc in self.term_docs[term]:                
                if self.query_doc_sim.get(doc) == None:
                    if 0.5*(1 - r_i) != 0 and r_i*0.5 != 0:
                        self.query_doc_sim[doc] = 0
                    else: 
                        self.query_doc_sim[doc] = np.log10(0.5*(1 - r_i) / r_i*(0.5))


                else:                      
                    if term in self.query_terms and 0.5*(1 - r_i) != 0 and r_i*(0.5) != 0:                           
                        self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10(0.5*(1 - r_i) / r_i*(0.5))


    def __sim_df(self):
        """
        Computes the similarity between the query and the documents from the collection
        takes p_i = df_i: term frequency in the collection
        :get query_doc_sim: saves the similarity between the query and a documents
        """
        for term in self.term_docs:
            p_i = (1 / 3) + ((2 / 3) * (self.term_freq[term][1] / self.N))
            
            # n_i = len(self.term_docs[term])
            # n_i = self.term_freq[term][0]
            # r_i = n_i / self.N

            r_i = self.term_freq[term][0] / self.N 

            for doc in self.term_docs[term]:
                if self.query_doc_sim.get(doc) == None:
                    if p_i*(1 - r_i) != 0 and r_i*(1 - p_i) != 0:
                        self.query_doc_sim[doc] = np.log10(p_i*(1 - r_i) / r_i*(1 - p_i))
                    else:
                        self.query_doc_sim[doc] = 0

                else:
                    if term in self.query_terms and p_i*(1 - r_i) != 0 and r_i*(1 - p_i) != 0:                           
                        self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10(p_i*(1 - r_i) / r_i*(1 - p_i))

   
    def __get_term_frequency(self, terms: list):
        """
        Saves the frequency of a term in a document
        :param terms: terms of the document to count 
        :get term_freq: saves the frequency of a term in the collection, the sum of the frequency in each document of the collection 
        """

        temp = dict()

        for t in terms:
            temp[t] = terms.count(t)
        
        for t in temp:
            if self.term_freq.get(t):
                self.term_freq[t] = (len(self.term_docs[t]), self.term_freq[t] + temp[t])
            else: 
                self.term_freq[t] = (len(self.term_docs[t]), temp[t])


    # def __get_doc_terms(self, sensitive: bool):
    #     """
    #     Analyze de terms occurrency in each document from de collection 
    #     :param documents: list of documents
    #     :get doc_terms: empty dictionary to store docs and their terms
    #     :param sensitive: boolean to know if the search is sensitive or not
    #     """

    #     for doc in self.dataset.get_docs_data():
    #         self.N = self.N + 1

    #         if sensitive:
    #             self.doc_terms[doc] = list(set(self.get_split_terms(doc['text'])))
                
    #             self.__get_term_docs(doc)

    #         else:
    #             self.doc_terms[doc] = list(set(self.get_split_terms(doc['text'].lower())))

    #             self.__get_term_docs(doc)


    # def __get_term_docs(self, document: str):
    #     """
    #     For each term saves a in a list the document in which it appears
    #     :param document: document from which the terms will be search analyzed
    #     :get doc_terms: dictionary in which the terms of the document are saved 
    #     :get terms_doc: dictionary in which the list of documents that contain the term will be saved
    #     """    
    
    #     for term in self.doc_terms[document]:
    #         if self.term_docs.get(term) == None:
    #             self.term_docs[term] = []
    #             self.term_docs[term].append(document)

    #         else:
    #             self.term_docs[term].append(document)