import re
from os import getcwd
from os.path import isfile, join
from math import log

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


class VectorModel:
    def __init__(self):
        self.docterms= dict()
        self.stopwords= self.get_stopwords()

    def vectorial_model(self, query:str, documents:list):
        docs_freq= self.get_docs_terms_frequency(documents)
        print(docs_freq)
        

    def get_docs_terms_frequency(self, documents:list):
        """
        :param documents: list of documents
        :return: dictionary with terms and their frequency in each document
        """
        for doc in documents:
            data= self.get_doc_data(doc)
            terms= self.get_split_terms(data)
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
            self.tf(doc, terms, max)
        self.idf()
        self.w()
            
        return self.docterms


    def tf(self, doc:str, terms:list, max:int):
        for term in terms:
            if max != 0:
                self.docterms[term][doc]['tf'] = round(self.docterms[term][doc]['freq']/max, 3)
            else:
                self.docterms[term][doc]['freq'] = 0

    #TODO: log(0) error
    def idf(self):
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = round(log(len(self.docterms)/len(self.docterms[term])), 3)
    
    def w(self):
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['w'] = round(self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf'], 3)



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


a = VectorModel()
a.vectorial_model('pollo casa nodo', documentslist)