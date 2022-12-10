from dataset import Datasets
from math import log
import numpy as np

class Model:
    def __init__(self):
        self.dataset= Datasets()

    def run(self, query:str, dataset:str, limit:int= None, umbral:float= None) -> list: ...

    def find(self, query:str, limit:int= None, umbral:float= None) -> list: ...

    def data(self): ...

    def sim(self): ...

    def query_data(self, query:str): ...


    def compare_datasets(self, dataset:str):
        """
        Compare the documents with the set of documents
        :param documents: list of documents
        :get documents: set of documents
        :return: True if the documents are the same, False if not
        """
        return self.dataset.docterms_dict or self.dataset.docterms_matrix
    
    def clear(self, clearlist: list):
        for element in clearlist:
            element.clear()
    
    def ranking(self, limit: int, umbral: float, querysim: dict) -> list:
        new_query_sim = dict()
        for doc in querysim:
            if querysim[doc] > 0:
                new_query_sim[doc] = querysim[doc]
        rank = sorted(new_query_sim.items(), key=lambda x: x[1], reverse=True)

        # rank = sorted(querysim.items(), key=lambda x: x[1], reverse=True)
        
        if umbral:
            rank= self.umbral(rank, umbral)
        
        if limit:
            rank= rank[:limit]
        
        return rank
    
    def umbral(self, rank:list, umbral:float) -> list:
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

    def normalize(self, document:str) -> list:
        """
        Get the terms of the document that are not stopwords and store it in a list
        :param document: document to split
        :return: list of terms
        """
        return self.dataset.lexemizer.normalize(document)