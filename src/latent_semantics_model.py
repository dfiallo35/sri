from vector_model import *
import numpy as np


class LSI_Model(VectorModel):
    
    def __init__(self):
        super().__init__() 

    def __sim(self):
        """
        Calculate the similarity between the query and the documents and store it in the querysim dictionary
        :get queryterms: dictionary with query terms and their weight
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get querysim: empty dictionary to store documents and their similarity
        :return: dictionary with documents and their similarity"""
        terms_docs_matrix = self.dataset.terms_docs_frequency_matrix
        q = self.__get_vector_query()    #vector query
        T, S, DT = np.linalg.svd(terms_docs_matrix)

        S = np.diag(S)
        print(len(S))
        k=int((len(S)+1)/2)

        Tk = T[0:len(T),0:k]
        Sk = S[0:k,0:k]
        DTk = DT[0:k,0:len(DT)] 

        qk=np.dot(np.dot(q.transpose(),Tk),np.linalg.inv(Sk))

        doc_vectors={}
        for i,doc in enumerate(self.dataset.documents):
            doc_vectors[doc]=np.array([[DTk[j,i]] for j in range(k)])
            self.querysim[doc]=self.__doc_sim(doc_vectors[doc],qk)[0]
         

    
    def __get_vector_query(self):   
        """saves at vector_query the vector of the query" putting 0 in the terms that are not in the query"""  
        vector_query=[]
        for term in self.dataset.terms:
            if self.queryterms.__contains__(self.dataset.terms[term]):
                self.vector_query.append(self.queryterms[term])
            else:
                self.vector_query.append(0)
        return vector_query

    
    def __doc_sim(dj, q):
        result = 0
        dj_norm = np.linalg.norm(dj)
        q_norm = np.linalg.norm(q)
        for i in range(0,min(len(dj),len(q))):
            result +=  dj[i]*q[i]
        return (result / (dj_norm * q_norm))


