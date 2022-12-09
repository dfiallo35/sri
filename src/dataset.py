from itertools import count
from ir_datasets import load
from ir_datasets.datasets.base import Dataset
from lexemizer import Lexemizer
import numpy as np

class Datasets:
    def __init__(self):
        self.dataset:Dataset= None

        self.documents:set = None
        self.terms:set = None

        self.docslen:int = 0
        self.dataset_name:str = None
        self.lexemizer= Lexemizer()

        self.docterms_matrix: list= None
        self.docterms_dict: dict= None


    def build_dataset(self, dataset:str):
        self.dataset_name= dataset

        self.documents= set()
        self.dataset:Dataset = load(dataset)

        for doc in self.dataset.docs_iter():
            self.documents.add(doc.doc_id)
        self.docslen= self.dataset.docs_count()
    
    def build_dataset_matrix(self, dataset:str):
        self.build_dataset(dataset)
        self.__make_docs_matrix()
    
    def build_dataset_dict(self, dataset:str):
        self.build_dataset(dataset)
        self.__make_docs_dict()


    @property
    def terms_docs_frequency_matrix(self) -> list:
        return np.transpose(self.docterms_matrix)
    
    @property
    def terms_docs_boolean_matrix(self) -> list:
        matrix= []
        for row in self.terms_docs_frequency_matrix:
            newrow=[]
            for x in row:
                if x == 0:
                    newrow.append(0)
                else:
                    newrow.append(1)
            matrix.append(newrow)
        return matrix
    
    @property
    def docs_terms_frequency_matrix(self) -> list:
        return self.docterms_matrix
    
    @property
    def docs_terms_boolean_matrix(self) -> list:
        matrix= []
        for row in self.docs_terms_frequency_matrix:
            newrow=[]
            for x in row:
                if x == 0:
                    newrow.append(0)
                else:
                    newrow.append(1)
            matrix.append(newrow)
        return matrix

    @property
    def docs_terms_frequency_dict(self) -> dict:
        return self.docterms_dict
    
    
    def __make_docs_dict(self):
        self.docterms_dict= dict()
        for doc in self.get_docs_data():
            self.docterms_dict[doc['id']]= self.lexemizer.normalize(doc['text'])
    

    def __make_docs_matrix(self):
        docterms_matrix= []
        for doc in self.get_docs_data():
            docterms_matrix.append(self.lexemizer.normalize(doc['text']))
        
        self.terms= set()
        for doc in docterms_matrix:
            for term in doc:
                self.terms.add(term)
        
        self.docterms_matrix= []
        for doc in docterms_matrix:
            freq= Datasets.get_frequency(doc)
            newdoc= []
            for term in self.terms:
                if not freq.get(term):
                    newdoc.append(0)
                else:
                    newdoc.append(freq[term])
            self.docterms_matrix.append(newdoc)

    
    def get_frequency(elements:list) -> dict:
        """
        Count the frequency of the elements in the list
        :param list: list of elements
        :return: dictionary with the elements and their frequency
        """
        count= dict()
        for element in elements:
            if not count.get(element):
                count[element]= 1
            else:
                count[element] += 1
        return count
    
    def get_max_frequency(count:dict) -> int:
        """
        Get the max frequency of the terms in the query
        :param count: dictionary with terms and their frequency
        :return: max frequency
        """
        max=0
        for term in count:
            if max < count[term]:
                max = count[term]
        return max


    def get_docs_data(self) -> list:
        return [{'id':data.doc_id, 'text':data.text, 'title':data.title} for data in self.dataset.docs_iter()]


    def get_query_data(dataset: str) -> list:
        return [{'id':data.query_id, 'query':data.text} for data in load(dataset).queries_iter()]
    
    def print_query_data(dataset: str) -> list:
        return [data['id'] + ': ' + data['query'] for data in Datasets.get_query_data(dataset)]
            
    def get_qrels(dataset: str, id:str) -> list:
        qrel= [{'query':data.query_id, 'doc':data.doc_id, 'relevance':data.relevance} for data in load(dataset).qrels_iter() if data.query_id == id]
        return sorted(qrel, key=lambda x: x['relevance'])
    
    def get_qrels_coincidence(dataset: str, id:str, results: list) -> list:
        qrel= Datasets.get_qrels(dataset, id)
        new_qrel= []
        for result in results:
            for qr in qrel:
                if result[0] == qr['doc']:
                    qr['coincidence']= 'True'
                    new_qrel.append(qr)
                else:
                    qr['coincidence']= 'False'
                    new_qrel.append(qr)
        return qrel





import ir_datasets
dataset = ir_datasets.load('cranfield')


_count= dict()
for qrel in dataset.qrels_iter():
    if not _count.get(qrel.query_id):
        _count[qrel.query_id]= 1
    else:
        _count[qrel.query_id] += 1
print(_count)

for qrel in dataset.qrels_iter():
    if qrel.query_id =='1':
        print(qrel)
        