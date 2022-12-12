import streamlit as st
from vector_model import Datasets, Model, VectorModel
from probabilistic_model import ProbabilisticModel
from latent_semantics_model import LSIModel
import os
from PIL import Image

#todo: use delta in F1
#todo: use delta in metric for the arrow
#todo: R-presicion and Fallout
class Visual:
    '''
    Class to visualize the results of the models
    '''
    def __init__(self):
        self.sbar= None

        self.method:str = None
        self.dataset:str = None
        self.example_queries:str = None
        self.threshold:float = None

        self.example_queries:str = None
        self.input_type:str = None

        self.queries:dict = dict()
        self.query:str= None

        self.run:bool= False
        self.results:list= None


    @st.cache(suppress_st_warning=False, allow_output_mutation=True)
    def models():
        '''
        Use cache to load the models intances and save the data
        :return: dictionary with the models
        '''
        return { 
            'Vector Model': VectorModel(),
            'Probabilistic Model': ProbabilisticModel(),
            'Latent Semantics Model': LSIModel()
        }

    
    def main(self):
        '''
        Main function to run the app
        '''
        self.logo_img()
        self.sidebar()
        self.set_threshold()
        self.search_box()

        if self.run:
            self.results= Visual.models()[self.method].run(query=self.query['query'], dataset=self.dataset, threshold=self.threshold)
            self.show_results(self.results, Visual.models()[self.method])
            self.metrics()
        else:
            self.empty_metrics()


    def logo_img(self):
        '''
        Show the logo of the app
        '''
        img_dir= os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)) , os.path.join('imgs', 'logo.png')))
        st.image(Image.open(img_dir), width= 200)
    

    def set_threshold(self):
        '''
        Set the threshold to the default values if they are 0 or None respectively
        '''
        if self.threshold == 0.0:
            self.threshold= None


    def sidebar(self):
        '''
        Create the sidebar with the options
        '''
        self.sbar= st.sidebar

        self.sbar.title("Options")
        self.method= self.sbar.selectbox("Method", list(Visual.models().keys()))
        self.dataset= self.sbar.selectbox("Dataset", ['cranfield', 'beir/arguana'])

        with self.sbar.expander(label='Options'):
            self.input_type= st.selectbox("Input type", ["Example queries", "Text"])
            self.threshold= st.slider("Threshold", min_value=0.0, max_value=1.0, value=0.0, step= 0.01)
        self.sbar.markdown('-----------------')


    def search_box(self):
        '''
        Create the search box with the input type selected and the search button
        '''
        if self.input_type == "Text":
            col1, col2= st.columns([4,1])
            self.query= col1.text_input("", key="different")
            col2.text('')
            col2.text('')
            run= col2.button('Search')

        if self.input_type == "Example queries":
            col1, col2= st.columns([4,1])

            for q in zip(Datasets.print_query_data(self.dataset), Datasets.get_query_data(self.dataset)):
                self.queries[q[0]]= q[1]

            self.query= col1.selectbox(" ", list(self.queries.keys()), label_visibility='hidden')
            self.query= self.queries[self.query]

            col2.text('')
            col2.text('')
            self.run= col2.button('Search')

    def empty_metrics(self):
        '''
        Show the metrics with empty values
        '''
        with self.sbar.expander('Metrics'):
            c1, c2= st.columns([1,1])
            c1.metric('P', 0)
            c2.metric('R', 0)
            c3, c4= st.columns([1,1])
            c3.metric('F', 0)
            c4.metric('F1', 0)
        
        with self.sbar.expander('Documents Relevance'):
            st.text('')

    def metrics(self):
        '''
        Show the metrics of the results
        '''
        with self.sbar.expander('Metrics', expanded=True):
            metrics= Datasets.eval(self.dataset, self.query['id'], self.results, B=1)
            c1, c2= st.columns([1,1])
            c1.metric('P', round(metrics['P'], 3))
            c2.metric('R', round(metrics['R'], 3))
            c3, c4= st.columns([1,1])
            c3.metric('F', round(metrics['F'], 3))
            c4.metric('F1', round(metrics['F1'], 3))
        
        with self.sbar.expander('Documents Relevance'):
            st.dataframe(Datasets.get_qrels_coincidence(self.dataset, self.query['id'], self.results))
        

    def show_results(self, results, model: Model):
        '''
        Show the results of the search
        :param results: list of results
        :param model: model instance
        '''
        docs = model.dataset.get_docs_data()
        for result in results:
            with st.expander(label=f'Document: {result[0]}'):
                st.text('Title: ' + docs[int(result[0])-1]['title'])
                st.text(f"Similarity: {result[1]}")
                st.text('Content:')
                st.text(docs[int(result[0])-1]['text'])


a= Visual()
a.main()
