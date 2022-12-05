from base_model import Model
from dataset import Datasets
from stopwords import Stopwords
import numpy as np


class Probabilistic_Model(Model):

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

        # list of stopwords
        self.stopwords = Stopwords('english')

        self.dataset = Datasets()


    def run(self, query: str, dataset: str, limit: int=None, umbral: float=None, sensitive: bool=False):
        self.__clean_query_data()

        if not self.__compare_datasets(dataset):
            self.docs_data(dataset, sensitive)

        return self.find(query, limit, umbral, sensitive)


    def __compare_datasets(self, dataset: str):
        """
        Compare the documents with the set of documents
        :param documents: list of documents
        :get documents: set of documents
        :return: True if the documents are the same, False if not
        """

        if self.dataset.dataset_name == dataset:
            return True

        return False


    def docs_data(self, dataset: str, sensitive: bool= False):
        self.dataset.get_dataset(dataset)
        self.__get_term_docs(sensitive)

    
    def find(self, query: str, limit: int=None, umbral: float=None, sensitive: bool=False):
        """
        :param query: query to search
        :param documents: list of documents
        :get query_terms: list with query terms
        :return: list of documents sorted by similarity
        """

        if sensitive:
            self.__query_terms(query)
        else:
            self.__query_terms(query.lower())

        self.__sim()

        rank = self.__ranking(limit, umbral)
        
        return rank


    def __clean_query_data(self):
        """
        Clean the query data
        :get query_terms: empty dictionary to store query terms
        """

        self.query_terms.clear()


    def __ranking(self, limit: int, umbral: float):
        new_query_sim = dict()

        for doc in self.query_doc_sim:
            if self.query_doc_sim[doc] != 0:
                new_query_sim[doc] = self.query_doc_sim[doc]

        self.query_doc_sim = new_query_sim

        rank = sorted(self.query_doc_sim.items(), key=lambda x: x[1], reverse=True)
        
        if umbral != None:
            rank= self.__umbral(rank, umbral)
        
        if limit != None:
            rank= rank[:limit]
        
        return rank


    def __umbral(self, rank: list, umbral: float):
        """
        Filter the documents by the similarity using the umbral
        :param rank: list of documents sorted by similarity
        :param umbral: similarity umbral
        :return: list of documents that pass the umbral
        """
        newrank= []

        for doc in rank:
            if doc[1] >= umbral:
                newrank.append(doc)

        return newrank


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


    def __sim(self):
        """
        Computes the similarity between the query and the documents from the collection
        takes as a constant value p_i = 0.5
        :get query_doc_sim: saves the similarity between the query and a documents
        """

        for term in self.term_docs:
            r_term = len(self.term_docs[term]) / self.dataset.docslen
            
            for doc in self.term_docs[term]:      
                if term in self.query_terms:          
                    if self.query_doc_sim.get(doc) == None:
                        if (1 - r_term) != 0 and r_term != 0:
                                self.query_doc_sim[doc] = np.log10((1 - r_term) / r_term)
                        else:
                                self.query_doc_sim[doc] = 0

                    else:
                        self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10((1 - r_term) / r_term)

                # else:                      
                #     if self.query_doc_sim.get(doc) == None:                           
                #         self.query_doc_sim[doc] = 0