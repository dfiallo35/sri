import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords

class Lexemizer:
    def __init__(self):
        nltk.download('stopwords')
        self.stopwords:set = set(stopwords.words('english'))
        self.lexemizer = WordNetLemmatizer()
    
    def normalize(self, text: str) -> list:
        return [self.lexemizer.lemmatize(token.lower()) for token in re.split(r'\W+', text) if token not in self.stopwords]
    

    def consult_expansion(query: list) -> list:
        newquery=[]
        for term in query:
            for synset in wordnet.synsets(term):
                for lemma in synset.lemmas():
                    newquery.append(lemma.name())
        print('-------------------------------')
        print(query)
        print(list(set(newquery)))
        return list(set(newquery))