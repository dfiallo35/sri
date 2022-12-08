import re
import nltk
from nltk.stem.lancaster import LancasterStemmer


class Lexemizer:
    def __init__(self):
        nltk.download('stopwords')
        self.stopwords:set = set(nltk.corpus.stopwords.words('english'))
        self.lancaster = LancasterStemmer()
    
    def normalize(self, text: str):
        return [self.lancaster.stem(token.lower()) for token in re.split(r'\W+', text) if token not in self.stopwords]