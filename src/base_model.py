from dataset import *
from math import log
import numpy as np

class Model:
    def __init__(self):
        self.dataset= Datasets()

    def run(self, query:str, dataset:str, threshold:float= None) -> list: ...

    def find(self, query:str, threshold:float= None) -> list: ...

    def data(self): ...

    def sim(self): ...

    def query_data(self, query:str): ...


    def reuse_data(self):
        '''
        Reuse the data of the dataset if it is already calculated
        :return: True if the data is reused, False if it is not
        '''
        return self.dataset.docterms_dict or self.dataset.docterms_matrix
    
    def clear(self, clearlist: list):
        '''
        Clear all the elements that are not going to be used in the next execution
        :param clearlist: list of elements to clear
        '''
        for element in clearlist:
            element.clear()
    
    def ranking(self, threshold: float, querysim: dict) -> list:
        '''
        Rank the documents by their similarity
        :param threshold: similarity threshold
        :param querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        '''
        new_query_sim = dict()
        for doc in querysim:
            if querysim[doc] > 0:
                new_query_sim[doc] = querysim[doc]

        rank = sorted(new_query_sim.items(), key=lambda x: x[1], reverse=True)
        
        if threshold:
            rank= self.threshold(rank, threshold)
        
        return rank
    
    def threshold(self, rank:list, threshold:float) -> list:
        """
        Filter the documents by the similarity using the threshold
        :param rank: list of documents sorted by similarity
        :param threshold: similarity threshold
        :return: list of documents that pass the threshold
        """
        newrank= []
        for doc in rank:
            if doc[1] >= threshold:
                newrank.append(doc)
        return newrank

    def normalize(self, document:str) -> list:
        """
        Normalize the document using the lexemizer
        :param document: document to normalize
        :return: list of terms
        """
        return self.dataset.lexemizer.normalize(document)
    
    def normalize_query(self, query:str) -> list:
        '''
        Normalize and expand the query using the lexemizer
        :param query: query to normalize
        :return: list of terms
        '''
        return self.dataset.lexemizer.consult_expansion(query)