import re
from os import getcwd
from os.path import isfile, join
import numpy as np
import operator

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


class VectorModel:
    def __init__(self):
        self.docterms= dict()
        self.stopwords= self.get_stopwords()
        # self.regex_stopwords=  self.get_regex_stopwords(self.stopwords)

    def vectorial_model(self, query:str, documents:list):
        docs_freq= self.get_docs_terms_frequency(documents)
        terms_freq= self.get_query_frequency(query)
        print(terms_freq)

        

    def get_docs_terms_frequency(self, documents:list):
        """
        :param documents: list of documents
        :return: dictionary with terms and their frequency in each document
        """
        for doc in documents:
            data= self.get_doc_data(doc)
            terms= self.get_split_terms(data)
            for term in terms:
                if self.docterms.get(term) == None:
                    self.docterms[term] = {doc:1}
                    
                else:
                    if self.docterms.get(term).get(doc) == None:
                        self.docterms[term][doc] = 1
                    else:
                        self.docterms[term][doc] = self.docterms[term][doc] + 1
        return self.docterms


    def get_regex_stopwords(self, stopwordslist:list):
        for i in range(len(stopwordslist)):
            stopwordslist[i]= '(' + stopwordslist[i] + ')'
        return ''.join(stopwordslist)

    def get_not_stopwords_terms(self, terms:list):
        for term in terms:
            if term in self.stopwords:
                terms.remove(term)
        return terms

    def get_doc_data(self, document:str):
        doc= open(document, 'r')
        docdata=doc.read()
        doc.close()
        return docdata.lower()

    def get_split_terms(self, document:str):
        doc= re.findall(r'\w+', document)
        return self.get_not_stopwords_terms(doc)

    def get_stopwords(self):
        stopwords_doc = open(join(getcwd(), 'data\\spanish_stopwords.txt'), 'r')
        stopwords_data = stopwords_doc.read()
        stopwords_doc.close()
        return re.findall(r'\w+', stopwords_data)

    #given a list of terms and documents return the frequency matrix of terms in documents
    def get_query_frequency(self, query:str):
        terms= re.findall('\w+', query)
        query_freq=dict()
        for term in terms:
            if self.docterms.get(term) != None:
                query_freq[term]= self.docterms.get(term)
        return query_freq

    def get_tf_idf(self, terms_frequency:dict):
        pass

                


a = VectorModel()
a.vectorial_model('pollo casa nodo', documentslist)