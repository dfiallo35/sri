import vector_model

class generalized_vector_model(vector_model):
    
    def __init__(self):
        """
        :param stopwords: list of stopwords
        :param docterms: dictionary with terms and their frequency, tf, idf and w
        :param queryterms: dictionary with query terms and their weight
        :param querysim: dictionary with documents and their similarity
        """
        super().__init__()
        # dictionary with keys as terms and values as a dictionary with keys as documents and values as a dictionary with keys as freq, tf, idf and w
        # {terms: {docs: {freq, tf, idf, w}}}
        self.docterms= dict()
        # dictionary with keys as query terms and values as their weight
        self.queryterms= dict()
        # dictionary with keys as documents and values as their similarity
        self.querysim= dict()
        # list of stopwords
        