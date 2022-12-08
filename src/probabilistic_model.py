from base_model import *


class ProbabilisticModel(Model):

    def __init__(self):
        super().__init__()

        # dictionary with keys as terms and values as lists of documents
        self.term_docs = dict()
        
        # set of terms of the query
        self.queryterms = set()

    	# dictonary with the similarity between the query and documents
        self.query_doc_sim = dict()


    def run(self, query: str, dataset: str, limit: int=None, umbral: float=None):
        self.clear([self.queryterms, self.query_doc_sim])

        if not self.compare_datasets(dataset) and not self.term_docs:
            self.dataset.build_dataset(dataset)
            self.data()

        return self.find(query, limit, umbral)

    
    def find(self, query: str, limit: int=None, umbral: float=None):
        """
        :param query: query to search
        :param documents: list of documents
        :get query: list with query terms
        :return: list of documents sorted by similarity
        """
        self.query_data(query)
        self.sim()
        rank = self.ranking(limit, umbral, self.query_doc_sim)
        return rank


    def data(self):
        """
        For each term saves a in a list the document in which it appears
        :param document: document from which the terms will be search analyzed
        :get doc_terms: dictionary in which the terms of the document are saved 
        :get terms_doc: dictionary in which the list of documents that contain the term will be saved
        """    
        for doc in self.dataset.get_docs_data():
            doc_split = self.normalize(doc['text'])

            for term in doc_split:
                if not self.term_docs.get(term):
                    self.term_docs[term]= [doc['id']]

                else:
                    if doc not in self.term_docs[term]:
                        self.term_docs[term].append(doc['id'])


    def query_data(self, query: str):
        """
        Saves the query terms in a list
        :param query: the query string
        :get query_terms: list of query terms
        """
        for term in self.normalize(query):
            self.queryterms.add(term)


    def sim(self):
        """
        Computes the similarity between the query and the documents from the collection
        takes as a constant value p_i = 0.5
        :get query_doc_sim: saves the similarity between the query and a documents
        """
        for term in self.term_docs:
            r_term = len(self.term_docs[term]) / self.dataset.docslen
            
            for doc in self.term_docs[term]:      
                if term in self.queryterms:
                    if not self.query_doc_sim.get(doc):
                        if (1 - r_term) != 0 and r_term != 0:
                                self.query_doc_sim[doc] = np.log10((1 - r_term) / r_term)
                        else:
                                self.query_doc_sim[doc] = 0

                    else:
                        self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10((1 - r_term) / r_term)

                # else:                      
                #     if self.query_doc_sim.get(doc) == None:                           
                #         self.query_doc_sim[doc] = 0