import streamlit as st
import streamlit.components.v1 as components

from vector_model import Datasets, Model, VectorModel
from probabilistic_model import ProbabilisticModel
from latent_semantics_model import LSIModel


from math import ceil
from os.path import realpath, join, dirname
from PIL import Image
from time import time
img_dir= realpath(join(dirname(__file__) ,'imgs'))



class Visual:
    '''
    Class to visualize the results of the models
    '''
    def __init__(self):
        self.method:str = None
        self.dataset:str = None
        self.example_queries:str = None
        self.threshold:float = None
        self.beta:float = None

        self.example_queries:str = None
        self.mode:str = None

        self.queries:dict = dict()
        self.query:str= None

        self.run:bool= False
        self.results:list= None
        self.exe_time:float= None


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
        self.search_box()

        if self.threshold == 0.0:
            self.threshold= None
        
        if self.run:

            if self.mode == 'All queries':
                all_metrics= dict()

                progressbar = st.progress(0)
                for add_progressbar, query in enumerate(self.queries):
                    progressbar.progress(add_progressbar/ len(self.queries))

                    self.query= self.queries[query]

                    init= time()
                    self.results= Visual.models()[self.method].run(query=self.query['query'], dataset=self.dataset, threshold=self.threshold)
                    end= time()
                    self.exe_time= round(end- init, 3)

                    metrics= Datasets.eval(self.dataset, self.query['id'], self.results, B=self.beta)
                    metrics.update({'time': self.exe_time})
                    all_metrics[query]= metrics
                
                new_metrics= dict()
                for metric in ['P', 'R', 'F', 'F1', 'time']:
                    new_metrics[metric]= round(sum([all_metrics[query][metric] for query in all_metrics])/len(all_metrics), 3)

                self.dataset_metrics(new_metrics)
                progressbar.empty()
                    
            else:
                init= time()
                self.results= Visual.models()[self.method].run(query=self.query['query'], dataset=self.dataset, threshold=self.threshold)
                end= time()
                self.exe_time= round(end- init, 3)

                self.show_results(self.results, Visual.models()[self.method])
                self.metrics()
        else:
            self.empty_metrics()


    def logo_img(self):
        '''
        Show the logo of the app
        '''
        img_dir= realpath(join(dirname(realpath(__file__)) , join('imgs', 'logo.png')))
        st.image(Image.open(img_dir), width= 200)


    def sidebar(self):
        '''
        Create the sidebar with the options
        '''
        st.sidebar.title("Options")
        self.method= st.sidebar.selectbox("Method", list(Visual.models().keys()))
        self.dataset= st.sidebar.selectbox("Dataset", ['cranfield', 'vaswani'])
        self.mode= st.sidebar.selectbox("Mode", ["Example queries", "Text", 'All queries'])

        with st.sidebar.expander(label='Options'):
            self.threshold= st.slider("Threshold", min_value=0.0, max_value=1.0, value=0.2, step= 0.01)
            self.beta= st.slider('Beta', min_value=0.0, max_value=2.0, value=1.0, step= 0.01)

        st.sidebar.markdown('-----------------')


    def search_box(self):
        '''
        Create the search box with the input type selected and the search button
        '''
        if self.mode == "Text":
            col1, col2= st.columns([4,1])
            self.query= col1.text_input("", key="different")
            col2.text('')
            col2.text('')
            self.run= col2.button('Search')


        if self.mode == "Example queries":
            col1, col2= st.columns([4,1])

            for q in zip(Datasets.print_query_data(self.dataset), Datasets.get_query_data(self.dataset)):
                self.queries[q[0]]= q[1]

            self.query= col1.selectbox(" ", list(self.queries.keys()), label_visibility='hidden')
            self.query= self.queries[self.query]

            col2.text('')
            col2.text('')
            self.run= col2.button('Search')
        

        if self.mode == 'All queries':
            #todo: run the model for all the queries in the dataset
            #todo: calculate the avg metrics
            for q in zip(Datasets.print_query_data(self.dataset), Datasets.get_query_data(self.dataset)):
                self.queries[q[0]]= q[1]
            st.text('')
            st.text('')
            self.run= st.button('Calculate Metrics')
            

    def empty_metrics(self):
        '''
        Show the metrics with empty values
        '''
        with st.sidebar.expander('Metrics'):
            c1, c2= st.columns([1,1])
            c1.metric('P', 0)
            c2.metric('R', 0)
            c3, c4= st.columns([1,1])
            c3.metric('F', 0)
            c4.metric('F1', 0)
            st.metric('Execution Time', '0 s')
        
        with st.sidebar.expander('Documents Relevance'):
            st.text('')

    def metrics(self):
        '''
        Show the metrics of the results
        '''
        with st.sidebar.expander('Metrics', expanded=True):
            metrics= Datasets.eval(self.dataset, self.query['id'], self.results, B=self.beta)
            c1, c2= st.columns([1,1])
            c1.metric('P', round(metrics['P'], 3))
            c2.metric('R', round(metrics['R'], 3))
            c3, c4= st.columns([1,1])
            c3.metric('F', round(metrics['F'], 3))
            c4.metric('F1', round(metrics['F1'], 3))
            st.metric('Execution Time', str(self.exe_time) + ' s')
        
        with st.sidebar.expander('Documents Relevance'):
            st.dataframe(Datasets.get_qrels_coincidence(self.dataset, self.query['id'], self.results))
        
    def dataset_metrics(self, metrics: dict):
        '''
        Show the metrics of the dataset
        '''
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        c1, c2= st.columns([1,1])
        c1.metric('P', round(metrics['P'], 3))
        c2.metric('R', round(metrics['R'], 3))
        c3, c4= st.columns([1,1])
        c3.metric('F', round(metrics['F'], 3))
        c4.metric('F1', round(metrics['F1'], 3))
        st.metric('Execution Time', str(metrics['time']) + ' s')
        

    #bug: list index out of range
    def show_results(self, results, model: Model):
        '''
        Show the results of the search
        :param results: list of results
        :param model: model instance
        '''
        docs = model.dataset.get_docs_data()
        for i, tab in enumerate(st.tabs([str(i) for i in range(0, ceil(len(results)/10))])):
            with tab:
                for result in results[i*10:(i+1)*10]:
                    with st.expander(label=f'Document: {result[0]}'):
                        if self.dataset != 'vaswani':
                            st.text('Title: ' + docs[int(result[0])-1]['title'])
                        st.text(f"Similarity: {result[1]}")
                        st.text('Content:')
                        st.text(docs[int(result[0])-1]['text'])


a= Visual()
a.main()
