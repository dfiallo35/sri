import re
from os import getcwd, listdir
from os.path import isfile, join, isdir
from math import log


#TODO: make data sets
#TODO: verify log(0) and division by zero
#TODO: visual
#TODO: make documentation
#TODO: First process and save the document data, then just fetch the query
class VectorModel:
    def __init__(self):
        """
        :param stopwords: list of stopwords
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param queryterms: dictionary with query terms and their weight
        :param querysim: dictionary with documents and their similarity
        """

        # dictionary with keys as terms and values as a dictionary with keys as documents and values as a dictionary with keys as freq, tf, idf and w
        # {terms: {docs: {freq, tf, idf, w}}}
        self.docterms= dict()
        # dictionary with keys as query terms and values as their weight
        self.queryterms= dict()
        # dictionary with keys as documents and values as their similarity
        self.querysim= dict()
        # dictionary of stopwords
        self.stopwords= self.__get_stopwords()


    def find(self, query:str, dataset:str, limit:int= None, umbral:float= None, alpha:float=0.5, sensitive:bool= False):
        """
        Do the search of the query in the given documents
        :param query: query to search

    def __compare_documents(self, documents:list):
        """
        Compare the documents with the set of documents
        :param documents: list of documents
        :get documents: set of documents
        :return: True if the documents are the same, False if not
        """
        newdocs= set(documents)
        if self.documents == {}:
            return False
        if self.documents == newdocs:
            return True
        return False

    def docs_data(self, dataset:str, sensitive:bool= False):
        """
        Do the search of the query in the given documents
        :param query: query to search
        :param sensitive: if the query is case sensitive
        :return: ranked list of documents
        """
        documents= self.__get_docs(dataset)
        if not self.__compare_documents(documents):
            self.__add_docs_to_set(documents)
            self.__docterms_data(documents, sensitive)
        
        if umbral != None:
            rank= self.__umbral(rank, umbral)
        if limit != None:
            rank= rank[:limit]
        
        return rank

    def __get_docs(self, dir:str):
        """
        Get all the documents in the given directory
        :param dir: directory to search
        :return: list of documents
        """
        if isfile(dir):
            return dir
        if isdir(dir):
            docslist= []
            for doc in listdir(dir):
                docslist.append(self.__get_docs(join(dir, doc)))
            return docslist
        else:
            raise NotADirectoryError

    def __vectorial_model(self, query:str, documents:list, alpha:float, sensitive:bool):
        """
        Execute the vectorial model
        :param query: query to search
        :param documents: list of documents
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get queryterms: dictionary with query terms and their weight
        :get querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        self.__docterms_data(documents, sensitive)
        if sensitive:
            self.__query_data(query, alpha)
        else:
            self.__query_data(query.lower(), alpha)
        self.__sim()
        return self.__ranking()
    
    # TODO: define restrictions
    def __ranking(self):
        """
        Sort the documents by similarity and return the list based on the restrictions
        :get querysim: dictionary with documents and their similarity
        :return: list of documents sorted by similarity
        """
        return sorted(self.querysim.items(), key=lambda x: x[1], reverse=True)

    def __umbral(self, rank:list, umbral:float):
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
    
    def __sim(self):
        """
        Calculate the similarity between the query and the documents and store it in the querysim dictionary
        :get queryterms: dictionary with query terms and their weight
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        :get querysim: empty dictionary to store documents and their similarity
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



    def __query_data(self, query:str, alpha:float):
        """
        Calculate the weight of the query terms and store it in the queryterms dictionary
        :param query: query to search
        :get queryterms: empty dictionary to store terms and their weight
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

    def __get_terms_count(self, terms:list):
        """
        Get the frequency of the terms in the query and store it in a dictionary of key as term and value as frequency
        :param terms: list of terms
        :return: dictionary with terms and their frequency
        """
        count= dict()
        for term in terms:
            count[term]= terms.count(term)
        return count

    def __get_query_terms_docs(self, query:str):
        """
        Get the terms of the query and store it in a list
        :param query: query to search
        :return: list of terms
        """
        terms= []
        for term in self.__get_split_terms(query):
            if self.docterms.get(term) != None:
                terms.append(term)
        return terms
        

    def __docterms_data(self, documents:list, sensitive:bool):
        """
        Calculate the frequency, tf, idf and w of the terms in the documents and store it in the docterms dictionary
        :param documents: list of documents
        :get docterms: empty dictionary to store terms and their frequency, tf, idf and w
        :return: dictionary with terms and their frequency, tf, idf and w
        """
        for doc in documents:
            data= self.__get_doc_data(doc, sensitive)
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
        Calculate the tf of the terms in the documents and store it in the docterms dictionary
        :param doc: document to calculate tf
        :param terms: terms of the document
        :param max: max frequency of the document
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        """
        for term in terms:
            if max != 0:
                self.docterms[term][doc]['tf'] = round(self.docterms[term][doc]['freq']/max, 3)
            else:
                self.docterms[term][doc]['freq'] = 0

    #TODO: log(0) error
    def __idf(self, docslen):
        """
        Calculate the idf of the terms in the documents and store it in the docterms dictionary
        :param docslen: number of documents
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        """
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = round( ( log(docslen / len(self.docterms[term]) ) ), 3)
    
    def __w(self):
        """
        Calculate the w of the terms in the documents and store it in the docterms dictionary
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :get docterms: dictionary with terms and their frequency, tf, idf and w
        """
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['w'] = round(self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf'], 3)



    def __get_not_stopwords_terms(self, terms:list):
        """
        Get the terms that are not stopwords
        :param terms: list of terms
        :return: list of terms without stopwords
        """
        for term in terms:
            if term in self.stopwords:
                terms.remove(term)
        return terms

    def __get_doc_data(self, document:str, sensitive:bool):
        """
        Get the data of the document
        :param document: document to get data
        :return: data of the document
        """
        doc= open(document, 'r')
        docdata=doc.read()
        doc.close()
        if not sensitive:
            docdata= docdata.lower()
        return docdata

    def __get_split_terms(self, document:str):
        """
        Get the terms of the document that are not stopwords and store it in a list
        :param document: document to split
        :return: list of terms
        """
        doc= re.findall(r'\w+', document)
        return self.__get_not_stopwords_terms(doc)

    def __get_stopwords(self):
        """
        Get the stopwords from the file and store it in a list
        :return: list of stopwords
        """
        stopwords_doc = open(join(getcwd(), 'data\\spanish_stopwords.txt'), 'r')
        stopwords_data = stopwords_doc.read()
        stopwords_doc.close()
        return re.findall(r'\w+', stopwords_data)


