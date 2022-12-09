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

        # dictionary with keys as terms and values as the values of p and r for the term
        self.term_p_r = dict()


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
        self.sim(False) # computes de similarity
        rank = self.ranking(limit, umbral, self.query_doc_sim) # compute the ranking with the siilarity values

        # Pseudo-feedback
        i = 0

        while i in range(0, 5):
            self.pseudo_feedback_p_r(rank) # compute the values of p and r for all terms based on the relevant recovered documents

            self.sim(True) # compute de similarity with new term's p and r values 

            i = i + 1

            rank = self.ranking(limit, umbral, self.query_doc_sim) # compute the ranking again with the new similarity values

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
                self.term_p_r[term] = (0.5, 0)
                
                if not self.term_docs.get(term):
                    self.term_docs[term] = [doc['id']]

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


    def sim(self, feedback: bool):
        """
        Computes the similarity between the query and the documents from the collection
        takes as a constant value p_i = 0.5
        :get query_doc_sim: saves the similarity between the query and a documents
        """
        for term in self.term_docs: # for each term
            r_term = len(self.term_docs[term]) / self.dataset.docslen # calculates the term r value

            if not feedback:                
                self.term_p_r[term] = (0.5, r_term) # safes in the dictionary the value of r for the term and p stays constant (p = 0.5)

            for doc in self.term_docs[term]: # for each doc in which the term apppears
                
                if term in self.queryterms: # if the term is a query term
                    
                    if not self.query_doc_sim.get(doc): # if it's the first time that the doc has a term in common with the query 
                        
                        if not feedback:
                            # if (1 - r_term) != 0 and r_term != 0: # if the values don't indetermine the log function
                            if (1 - self.term_p_r[term][1]) != 0 and self.term_p_r[term][1] != 0: # if the values don't indetermine the log function
                                # self.query_doc_sim[doc] = np.log10((1 - r_term) / r_term) # calculate the similarity
                                self.query_doc_sim[doc] = np.log10((self.term_p_r[term][0]) / (1 - self.term_p_r[term][0])) + np.log10((1 - self.term_p_r[term][1]) / self.term_p_r[term][1]) # calculate the similarity

                            else: # if some of the values indeterminate the log function
                                    self.query_doc_sim[doc] = 0

                    else: # if at least one term has already been found common between the document and the query
                        
                        # if (1 - r_term) != 0 and r_term != 0: # if the values don't indetermine the log function
                        if (1 - self.term_p_r[term][1]) != 0 and self.term_p_r[term][1] != 0: # if the values don't indetermine the log function
                            # self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10((1 - r_term) / r_term) # sum the similarity already saved from the others terms that coincide in the document and the query 
                            self.query_doc_sim[doc] = self.query_doc_sim[doc] + np.log10((self.term_p_r[term][0]) / (1 - self.term_p_r[term][0])) + np.log10((1 - self.term_p_r[term][1]) / self.term_p_r[term][1]) # sum the similarity already saved from the others terms that coincide in the document and the query 

                else: # if the term in the document isn't a query term              
                    
                    if not self.query_doc_sim.get(doc): # if the document hasn't been analyzed   
                        self.query_doc_sim[doc] = 0 # the current similarity between it and the query is 0

    
    def pseudo_feedback_p_r(self, rank: list):
        """"
        Computes the term's p (probability of a term appearing in a document relevant to the query) 
        and r (probability of a term appearing in a nonrelevant document) values
        """

        rr_doc = len(rank) # number of relevant recovered documents

        for term in self.term_docs:
            v_term = self.count_recov_with_term(term, rank)

            p_term = (v_term + 0.5) / (recov_doc + 1)

            r_term = (len(self.term_docs[term]) - v_term + 0.5) / (self.dataset.docslen - recov_doc + 1)

            self.term_p_r[term] = (p_term, r_term)


    def count_recov_with_term(self, term: str, rank: list):
        """
        Computes the number of relevant documents in which "term" appears
        """

        v_term = 0

        for doc in self.term_docs[term]:
            if doc in rank:
                v_term = v_term + 1

        return v_term
