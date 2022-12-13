import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
nltk.download('wordnet')
nltk.download('stopwords')

class Lexemizer:
    def __init__(self):
        self.stopwords:set = set(stopwords.words('english'))
        self.lexemizer = WordNetLemmatizer()
    
    def normalize(self, text: str) -> list:
        '''
        Normalize the text ussing stopwords and lemmatizer with WordNet Lemmatizer from nltk
        :param text: text to normalize
        :return: normalized text
        '''
        return [self.lexemizer.lemmatize(token.lower()) for token in re.split(r'\W+', text) if token not in self.stopwords]
    

    def consult_expansion(self, query: list) -> list:
        '''
        Expand the query using synonyms from WordNet
        :param query: query to expand
        :return: expanded query
        '''
        query= self.normalize(query)
        newquery=[]
        for term in query:
            for synset in wordnet.synsets(term):
                for lemma in synset.lemmas():
                    newquery.append(lemma.name())
        return list(set(newquery))