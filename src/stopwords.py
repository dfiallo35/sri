from os import getcwd
from os.path import join
import re
import nltk
nltk.download('stopwords')


#todo: use module for estopwords
class Stopwords:
    def __init__(self, languaje:str):
        #TODO: make it a dictionary for O(1)
        self.stopwords:dict= self.__get_stopwords(languaje)

    def __get_stopwords(self, languaje:str):
        if languaje == 'english':
            stw   = set(nltk.corpus.stopwords.words('english'))
        if languaje == 'spanish':
            stw   = set(nltk.corpus.stopwords.words('english'))
        
        stpw= dict()
        for term in stw:
            stpw[term]= term
        return stpw
        

    def not_stopwords_terms(self, terms:list):
        new_terms= []
        for term in terms:
            if self.stopwords.get(term) == None:
                new_terms.append(term)
        return terms