import streamlit as st
from vector_model import Datasets, Model, VectorModel
from probabilistic_model import ProbabilisticModel
import os
from PIL import Image


class Visual:
    def __init__(self):
        self.sbar= None
        self.method:str = None
        self.dataset:str = None
        self.example_queries:str = None
        self.limit:int = None
        self.threshold:float = None
        self.example_queries:str = None
        self.input_type:str = None

    @st.cache(suppress_st_warning=False, allow_output_mutation=True)
    def models():
        return { 
            'Vector Model': VectorModel(),
            'Probabilistic Model': ProbabilisticModel()
        }

    

    def main(self):
        img_dir= os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)) , os.path.join('imgs', 'logo.png')))
        st.image(Image.open(img_dir), width= 200)
        self.sidebar()

        if self.limit == 0:
            self.limit= 100
        if self.threshold == 0.0:
            self.threshold= None

        if self.input_type == "Text":
            col1, col2= st.columns([4,1])
            query= col1.text_input("", key="different")
            col2.text('')
            col2.text('')
            run= col2.button('Search')
        if self.input_type == "Example queries":
            col1, col2= st.columns([4,1])
            query= col1.selectbox(" ", Datasets.get_query_data(self.dataset), label_visibility='hidden')
            col2.text('')
            col2.text('')
            run= col2.button('Search')
        
        if run:
            results= Visual.models()[self.method].run(query=query, dataset=self.dataset, umbral=self.threshold, limit=self.limit)
            self.show_results(results, Visual.models()[self.method])



    def sidebar(self):
        self.sbar= st.sidebar
        self.sbar.title("Options")
        self.method= self.sbar.selectbox("Method", ["Vector Model", "Probabilistic Model", "Generalized Vector Model"])
        self.dataset= self.sbar.selectbox("Dataset", ["cranfield"])
        self.input_type= self.sbar.selectbox("Input type", ["Example queries", "Text"])
        self.limit= self.sbar.number_input("Limit", min_value=0, max_value=100, value=0, step=1)
        self.threshold= self.sbar.number_input("Threshold", min_value=0.0, max_value=1.0, value=0.0, step= 0.1)


    def show_results(self, results, model: Model):
        docs = model.dataset.get_docs_data()
        for result in results:
            with st.expander(label=f'Document: {result[0]}'):
                st.text('Title: ' + docs[int(result[0])-1]['title'])
                st.text(f"Similarity: {result[1]}")
                st.text('Content:')
                st.text(docs[int(result[0])-1]['text'])


a= Visual()
a.main()
