from base_model import *




class VectorModel(Model):
    def __init__(self):
        """
        :param stopwords: list of stopwords
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param queryterms: dictionary with query terms and their weight
        :param querysim: dictionary with documents and their similarity
        """
        super().__init__()
        # dictionary with keys as terms and values as a dictionary with keys as documents and values as a dictionary with keys as freq, tf, idf and w
        # {terms: {docs: {freq, tf, idf, w}}}
        self.docterms= dict()
        # dictionary with keys as query terms and values as their weight
        self.queryterms= dict()
        # dictionary with keys as documents and values as their similarity
        self.querysim= dict()
        # list of stopwords
        


    def run(self, query:str, dataset:str, limit:int= None, umbral:float= None, alpha:float=0.5) -> list:
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

        if not self.compare_datasets(dataset) and not self.docterms:
            self.dataset.build_dataset(dataset)
            self.data()
    
        return self.find(query, limit, umbral, alpha)
        

    def find(self, query:str, limit:int= None, umbral:float= None, alpha:float=0.5) -> list:
        """
        :param query: query to search
        :param documents: list of documents
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get queryterms: dictionary with query terms and their weight
        :get querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        self.query_data(query, alpha)
        self.sim()
        return self.ranking(limit, umbral, self.querysim)

    
    def sim(self):
        """
        Calculate the similarity between the query and the documents and store it in the querysim dictionary
        :get queryterms: dictionary with query terms and their weight
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get querysim: empty dictionary to store documents and their similarity
        :return: dictionary with documents and their similarity"""

        sim= dict()
        aux= dict()
        for term in self.docterms:
            if term in self.queryterms:
                aux[term]= self.queryterms[term]
            else:
                aux[term]= 0

        for term in aux:
            for doc in self.docterms[term]:
                if not sim.get(doc):
                    sim[doc]= {'wiq2': pow(aux[term], 2), 'wij2': pow(self.docterms[term][doc]['w'], 2), 'wijxwiq': aux[term] * self.docterms[term][doc]['w']}
                else:
                    sim[doc]['wiq2'] += pow(aux[term], 2)
                    sim[doc]['wij2'] += pow(self.docterms[term][doc]['w'], 2)
                    sim[doc]['wijxwiq'] += aux[term] * self.docterms[term][doc]['w']
        for doc in sim:
            if pow(sim[doc]['wiq2'], 1/2) * pow(sim[doc]['wij2'], 1/2) != 0:
                self.querysim[doc] = round(sim[doc]['wijxwiq'] / ( pow(sim[doc]['wiq2'], 1/2) * pow(sim[doc]['wij2'], 1/2) ), 3)
            else:
                self.querysim[doc]= 0


    def query_data(self, query:str, alpha:float):
        """
        Calculate the weight of the query terms and store it in the queryterms dictionary
        :param query: query to search
        :get queryterms: empty dictionary to store terms and their weight
        :param alpha: parameter to calculate w
        :return: dictionary with the query terms and their weight
        """
        terms_count= Datasets.get_frequency([term for term in self.normalize_query(query) if self.docterms.get(term)])
        max= Datasets.get_max_frequency(terms_count)
        
        for term in terms_count:
            idf= 0
            for freq in self.docterms[term].values():
                idf= freq['idf']
            if max != 0:
                self.queryterms[term] = (alpha + (1 - alpha) * ((terms_count[term])/(max)))*idf
            else:
                self.queryterms[term] = 0


    def data(self):
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
            
            for term in terms_freq:
                if not self.docterms.get(term):
                    self.docterms[term] = {doc['id']:{'freq':terms_freq[term], 'tf':terms_freq[term]/max, 'idf':0, 'w':0}}
                else:
                    self.docterms[term][doc['id']] = {'freq':terms_freq[term], 'tf':terms_freq[term]/max, 'idf':0, 'w':0}
            
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = log(self.dataset.docslen / len(self.docterms[term]), 10)
                self.docterms[term][doc]['w'] = self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf']