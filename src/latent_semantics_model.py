from vector_model import *
import numpy as np


class LSIModel(VectorModel):
    
    def __init__(self):
        super().__init__() 
        self.k:int
        self.DTk= None
        self.Sk= None
        self.Uk= None

    def run(self, query:str, dataset:str, limit:int= None, umbral:float= None, k:int = 200) -> list:
        """
        Do the search of the query in the given dataset
        :param query: query to search
        :param dataset: dataset name
        :param limit: limit of documents to return
        :param umbral: similarity umbral
        :param alpha: alpha value for the similarity calculation of the query
        :return: ranked list of documents
        """
        self.clear([self.queryterms, self.querysim])
        self.k=k
        if not self.reuse_data() and not self.docterms:
            self.dataset.build_dataset_matrix(dataset)
            self.data(k)
    
        return self.find(query, limit, umbral)
        

    def find(self, query:str, limit:int= None, umbral:float= None) -> list:
        """
        :param query: query to search
        :param documents: list of documents
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get queryterms: dictionary with query terms and their weight
        :get querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        self.query_data(query)
        self.sim()
        return self.ranking(limit, umbral, self.querysim)


    def sim(self):
        """
        Calculate the similarity between the query and the documents and store it in the querysim dictionary
        :get queryterms: dictionary with query terms and their weight
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get querysim: empty dictionary to store documents and their similarity
        :return: dictionary with documents and their similarity"""

        q = np.array(self.__get_vector_query())#vector query
        qk=np.dot(np.dot(q.transpose(),self.Tk),np.linalg.inv(self.Sk))

        doc_vectors={}
        for i,doc in enumerate(self.dataset.documents):
            doc_vectors[doc]=np.array([[self.DTk[j,i]] for j in range(self.k)])
            self.querysim[doc]=self.__doc_sim(doc_vectors[doc],qk)[0]


    def data(self,k):
        """
        Calculate the frequency, tf, idf and w of the terms in the documents and store it in the docterms dictionary
        :param documents: list of documents
        :get docterms: empty dictionary to store terms and their frequency, tf, idf and w
        """
        for doc in self.dataset.get_docs_data():
            if doc['text'] == '':
                continue

            terms_freq= Datasets.get_frequency(self.normalize(doc['text']))
            max= Datasets.get_max_frequency(terms_freq)
        
        terms_docs_matrix = self.dataset.terms_docs_frequency_matrix
        T, S, DT = np.linalg.svd(terms_docs_matrix)

        S = np.diag(S)
        self.Tk = T[0:len(T),0:k]
        self.Sk = S[0:k,0:k]
        self.DTk = DT[0:k,0:len(DT)] 


    def query_data(self, query:str):
        """
        Calculate the weight of the query terms and store it in the queryterms dictionary
        :param query: query to search
        :get queryterms: empty dictionary to store terms and their weight
        :param alpha: parameter to calculate w
        :return: dictionary with the query terms and their weight
        """
        self.queryterms = Datasets.get_frequency(self.normalize(query))


    def __get_vector_query(self):   
        """saves at vector_query the vector of the query putting 0 in the terms that are not in the query"""  
        
        vector_query=[]
        for term in self.dataset.terms:
            if self.queryterms.__contains__(term):
                vector_query.append(self.queryterms[term])
            else:
                vector_query.append(0)
        return vector_query
        

    def __doc_sim(self,doc_j, query):
        """"calculate the similarity between the query and a document"""
        sim = 0
        dj_norm = np.linalg.norm(doc_j)
        q_norm = np.linalg.norm(query)
        for i in range(0,min(len(doc_j),len(query))):
            sim +=  doc_j[i]*query[i]
        return sim / (dj_norm * q_norm)


