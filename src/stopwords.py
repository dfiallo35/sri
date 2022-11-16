from os import getcwd
from os.path import join
import re

class Stopwords:
    def __init__(self, languaje:str):
        #TODO: make it a dictionary for O(1)
        self.stopwords:dict= self.__get_stopwords(languaje)

    def __get_stopwords(self, languaje:str):
        if languaje == 'english':
            stopwords_doc = open(join(getcwd(), 'data\\english_stopwords.txt'), 'r')
        if languaje == 'spanish':
            stopwords_doc = open(join(getcwd(), 'data\\spanish_stopwords.txt'), 'r')
        
        stopwords_data = stopwords_doc.read()
        stopwords_doc.close()
        sw= re.findall(r'\w+', stopwords_data)
        stpw= dict()
        for term in sw:
            stpw[term]= term
        return stpw
        

    def not_stopwords_terms(self, terms:list):
        new_terms= []
        for term in terms:
            if self.stopwords.get(term) == None:
                new_terms.append(term)
        return terms