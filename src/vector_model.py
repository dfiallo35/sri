import re
from os import getcwd
from os.path import isfile, join
from math import log

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


#TODO: get data set
#TODO: make data sets
#TODO: ranking limit
#TODO: verify if the file exists
#TODO: verify log(0) and division by zero
#TODO: visual
class VectorModel:
    def __init__(self):
        self.docterms= dict()
        self.queryterms= dict()
        self.querysim= dict()
        self.stopwords= self.__get_stopwords()

    def find(self, query:str, documents:list):
        self.__vectorial_model(query, documents)

    def __vectorial_model(self, query:str, documents:list):
        self.__docterms_data(documents)
        self.__query_data(query.lower())
        self.__sim()
        return self.__ranking()
    
    def __ranking(self):
        return sorted(self.querysim.items(), key=lambda x: x[1], reverse=True)
    
    def __sim(self):
        for term in self.queryterms:
            for doc in self.docterms[term]:
                if self.querysim.get(doc) == None:
                    self.querysim[doc] = round(self.queryterms[term] * self.docterms[term][doc]['w'], 3)
                else:
                    self.querysim[doc] = round(self.querysim[doc] + self.queryterms[term] * self.docterms[term][doc]['w'], 3)


    def __query_data(self, query:str, alpha:int=0):
        """
        :param query: query to search
        :param queryterms: empty dictionary to store terms and their weight
        :param alpha: parameter to calculate w
        :return: dictionary with the query terms and their weight
        """
        terms= self.__get_split_terms(query)
        terms_set= set(terms)
        for term in terms_set:
            if term in self.docterms:
                max_freq=0
                idf= 0
                for freq in self.docterms[term].values():
                    idf= freq['idf']
                    if max_freq < freq['freq']:
                        max_freq= freq['freq']
                
                if max_freq != 0:
                    self.queryterms[term] = round((alpha + (1 - alpha) * ((terms.count(term))/(max_freq)))*idf, 3)
                else:
                    self.queryterms[term] = 0
        return self.queryterms
            

        

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
        for term in terms:
            if max != 0:
                self.docterms[term][doc]['tf'] = round(self.docterms[term][doc]['freq']/max, 3)
            else:
                self.docterms[term][doc]['freq'] = 0

    #TODO: log(0) error
    def __idf(self, docslen):
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['idf'] = round( ( log(docslen / len(self.docterms[term]) ) ), 3)
    
    def __w(self):
        for term in self.docterms:
            for doc in self.docterms[term]:
                self.docterms[term][doc]['w'] = round(self.docterms[term][doc]['tf'] * self.docterms[term][doc]['idf'], 3)



    def __get_not_stopwords_terms(self, terms:list):
        for term in terms:
            if term in self.stopwords:
                terms.remove(term)
        return terms

    def __get_doc_data(self, document:str):
        doc= open(document, 'r')
        docdata=doc.read()
        doc.close()
        return docdata.lower()

    def __get_split_terms(self, document:str):
        doc= re.findall(r'\w+', document)
        return self.__get_not_stopwords_terms(doc)

    def __get_stopwords(self):
        stopwords_doc = open(join(getcwd(), 'data\\spanish_stopwords.txt'), 'r')
        stopwords_data = stopwords_doc.read()
        stopwords_doc.close()
        return re.findall(r'\w+', stopwords_data)


a = VectorModel()
rank= a.find(' ajo mano  Perro CaSa   pilar DadO dado', documentslist)
print(a.docterms)
print(a.queryterms)
print(a.querysim)
print(rank)