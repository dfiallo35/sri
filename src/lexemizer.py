import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
nltk.download('stopwords')

#todo: use module for estopwords
class Lexemizer:
    def __init__(self):
        self.stopwords:set = set(nltk.corpus.stopwords.words('english'))
        self.lancaster = LancasterStemmer()

    def not_stopwords_terms(self, terms:list):
        new_terms= []
        for term in terms:
            if self.stopwords.get(term) == None:
                new_terms.append(term)
        return terms
    
    def normalize(self, text: str):
        return [self.lancaster.stem(token.lower()) for token in re.split(r'\W+', text) if token not in self.stopwords]