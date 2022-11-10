import re
from os import getcwd, listdir
from os.path import isfile, join, isdir
from math import log


#TODO: get data set
#TODO: make data sets
#TODO: ranking limit
#TODO: verify if the file exists
#TODO: verify log(0) and division by zero
#TODO: visual
class VectorModel:
    def __init__(self):
        """
        :param stopwords: list of stopwords
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param queryterms: dictionary with query terms and their weight
        :param querysim: dictionary with documents and their similarity
        """
        self.docterms= dict()
        self.queryterms= dict()
        self.querysim= dict()
        self.stopwords= self.__get_stopwords()

    def find(self, query:str, documents:list):
        """
        :param query: query to search
        :param documents: list of documents
        :return: list of documents sorted by similarity
        """
        return self.__vectorial_model(query, documents)

    def __vectorial_model(self, query:str, documents:list):
        """
        :param query: query to search
        :param documents: list of documents
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param queryterms: dictionary with query terms and their weight
        :param querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        self.__docterms_data(documents)
        self.__query_data(query.lower())
        self.__sim()
        return self.__ranking()
    
    def __ranking(self):
        """
        :param querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        return sorted(self.querysim.items(), key=lambda x: x[1], reverse=True)
    
    def __sim(self):
        """
        :param queryterms: dictionary with query terms and their weight
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param querysim: empty dictionary to store documents and their similarity
        :return: dictionary with documents and their similarity"""

        sim= dict()
        for term in self.queryterms:
            for doc in self.docterms[term]:
                if sim.get(doc) == None:
                    sim[doc]= {'wiq2': pow(self.queryterms[term], 2), 'wij2': pow(self.docterms[term][doc]['w'], 2), 'wiq': self.queryterms[term], 'wij': self.docterms[term][doc]['w']}
                else:
                    sim[doc]['wiq2'] += pow(self.queryterms[term], 2)
                    sim[doc]['wij2'] += pow(self.docterms[term][doc]['w'], 2)
                    sim[doc]['wiq'] += self.queryterms[term]
                    sim[doc]['wij'] += self.docterms[term][doc]['w']
        for doc in sim:
            self.querysim[doc] = round( (sim[doc]['wiq'] * sim[doc]['wij']) / ( pow(sim[doc]['wiq2'], 1/2) * pow(sim[doc]['wij2'], 1/2) ), 3 )



    def __query_data(self, query:str, alpha:int=0):
        """
        :param query: query to search
        :param queryterms: empty dictionary to store terms and their weight
        :param alpha: parameter to calculate w
        :return: dictionary with the query terms and their weight
        """
        terms= self.__get_query_terms_docs(query)
        terms_count= self.__get_terms_count(terms)
        max= self.__get_max_count_query(terms_count)
        
        for term in terms_count:
            idf= 0
            for freq in self.docterms[term].values():
                idf= freq['idf']
            if max != 0:
                self.queryterms[term] = round((alpha + (1 - alpha) * ((terms_count[term])/(max)))*idf, 3)
            else:
                self.queryterms[term] = 0
        return self.queryterms
    
    def __get_max_count_query(self, count:dict):
        max=0
        for term in count:
            if max < count[term]:
                max = count[term]
        return max

    def __get_terms_count(self, terms:list):
        count= dict()
        for term in terms:
            count[term]= terms.count(term)
        return count

    def __get_query_terms_docs(self, query:str):
        terms= []
        for term in self.__get_split_terms(query):
            if self.docterms.get(term) != None:
                terms.append(term)
        return terms
        

    def __docterms_data(self, documents:list):
        """
        :param documents: list of documents
        :docterms: empty dictionary to store terms and their frequency, tf, idf and w
        :return: dictionary with terms and their frequency, tf, idf and w
        """
        for doc in documents:
            data= self.__get_doc_data(doc)
            terms= self.__get_split_terms(data)
            max= 0
            for term in terms:
                if self.docterms.get(term) == None:
                    self.docterms[term] = {doc:{'freq':1, 'tf':0, 'idf':0, 'w':0}}
                    if max < 1:
                        max= 1
                    
                else:
                    if self.docterms.get(term).get(doc) == None:
                        self.docterms[term][doc] = {'freq':1, 'tf':0, 'idf':0, 'w':0}
                        if max < 1:
                            max= 1
                    else:
                        self.docterms[term][doc]['freq'] = self.docterms[term][doc]['freq'] + 1
                        if max < self.docterms[term][doc]['freq']:
                            max= self.docterms[term][doc]['freq']
            self.__tf(doc, terms, max)
        self.__idf(len(documents))
        self.__w()
        return self.docterms


    def __tf(self, doc:str, terms:list, max:int):
        """
        :param doc: document to calculate tf
        :param terms: terms of the document
        :param max: max frequency of the document
        :return: tf of the document
        """
        for term in terms:
            if max != 0:
                self.docterms[term][doc]['tf'] = round(self.docterms[term][doc]['freq']/max, 3)
            else:
                self.docterms[term][doc]['freq'] = 0

    #TODO: log(0) error
    def __idf(self, docslen):
        """
        :param docslen: number of documents
        :return: idf of the term
        """
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = round( ( log(docslen / len(self.docterms[term]) ) ), 3)
    
    def __w(self):
        """
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :return: dictionary with terms and their frequency, tf, idf and w
        """
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['w'] = round(self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf'], 3)



    def __get_not_stopwords_terms(self, terms:list):
        """
        :param terms: list of terms
        :return: list of terms without stopwords
        """
        for term in terms:
            if term in self.stopwords:
                terms.remove(term)
        return terms

    def __get_doc_data(self, document:str):
        """
        :param document: document to get data
        :return: data of the document
        """
        doc= open(document, 'r')
        docdata=doc.read()
        doc.close()
        return docdata.lower()

    def __get_split_terms(self, document:str):
        """
        :param document: document to split
        :return: list of terms
        """
        doc= re.findall(r'\w+', document)
        return self.__get_not_stopwords_terms(doc)

    def __get_stopwords(self):
        """
        :return: list of stopwords
        """
        stopwords_doc = open(join(getcwd(), 'data\\spanish_stopwords.txt'), 'r')
        stopwords_data = stopwords_doc.read()
        stopwords_doc.close()
        return re.findall(r'\w+', stopwords_data)


