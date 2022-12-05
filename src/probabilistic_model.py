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

        # dictionary with keys as terms and values as lists of documents
        self.term_docs = dict()
        
        # list of terms of the query
        self.query_terms = []

    	# dictonary with the similarity between the query and documents
        self.query_doc_sim = dict()


    def __get_term_docs(self, sensitive: bool):
        """
        For each term saves a in a list the document in which it appears
        :param document: document from which the terms will be search analyzed
        :get doc_terms: dictionary in which the terms of the document are saved 
        :get terms_doc: dictionary in which the list of documents that contain the term will be saved
        """    
    
        for doc in self.dataset.get_docs_data():
            doc_split = []

            if sensitive:
                doc_split = self.get_split_terms(doc['text'])
            
            else:
                doc_split = self.get_split_terms(doc['text'].lower())

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


    def __sim_const(self):
        """
        Computes the similarity between the query and the documents from the collection
        takes as a constant value p_i = 0.5
        :get query_doc_sim: saves the similarity between the query and a documents
        """
       
        for term in self.term_docs:
            r = len(self.term_docs[term]) / self.dataset.docslen
            
            for doc in self.term_docs[term]:                
                if self.query_doc_sim.get(doc) == None:
                    if 0.5 * (1 - r) != 0 and r * 0.5 != 0:
                        self.query_doc_sim[doc] = 0

                    else: 
                        self.query_doc_sim[doc] = np.log10(0.5 * (1 - r) / r * (0.5))

                else:                      
                    if term in self.query_terms and 0.5 * (1 - r) != 0 and r * (0.5) != 0:                           
                        self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10(0.5 * (1 - r) / r * 0.5)
