import ir_datasets
from ir_datasets import load
from ir_datasets.datasets.base import Dataset
from lexemizer import Lexemizer

class Datasets:
    def __init__(self):
        self.dataset:Dataset= None

        self.documents:set = None
        self.terms:set = None
        
        self.docslen:int = 0
        self.dataset_name:str = None
        self.lexemizer= Lexemizer()
        self.docterms_matrix: list= None

    def get_dataset(self, dataset:str):
        self.dataset_name= dataset

        self.documents= set()
        self.dataset:Dataset = load(dataset)
        for doc in self.dataset.docs_iter():
            self.documents.add(doc.doc_id)
        self.docslen= self.dataset.docs_count()

        self.make_docs_matrix()


    def make_docs_matrix(self):
        docterms_matrix= []
        for doc in self.get_docs_data():
            docterms_matrix.append(self.lexemizer.normalize(doc['text']))
        
        self.terms= set()
        for doc in docterms_matrix:
            for term in doc:
                self.terms.add(term)
        

        self.docterms_matrix= []
        for doc in docterms_matrix:
            freq= self.get_frequency(doc)
            newdoc= []
            for term in self.terms:
                if not freq.get(term):
                    newdoc.append(0)
                else:
                    newdoc.append(freq[term])
            self.docterms_matrix.append(newdoc)
    

    
    def get_frequency(self, elements:list):
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

    def get_docs_data(self):
        return [{'id':data.doc_id, 'text':data.text, 'title':data.title} for data in self.dataset.docs_iter()]

    def get_query_data(dataset: str):
        return [data.text for data in load(dataset).queries_iter()]