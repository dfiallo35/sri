import streamlit as st
from vector_model import Datasets, Model, VectorModel
from probabilistic_model import ProbabilisticModel
from latent_semantics_model import LSIModel
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
        self.queries:dict = dict()

    @st.cache(suppress_st_warning=False, allow_output_mutation=True)
    def models():
        return { 
            'Vector Model': VectorModel(),
            'Probabilistic Model': ProbabilisticModel(),
            'Latent Semantics Model': LSIModel()
        }

    

    def main(self):
        img_dir= os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)) , os.path.join('imgs', 'logo.png')))
        st.image(Image.open(img_dir), width= 200)
        self.sidebar()

        if self.limit == 0:
            self.limit= 25
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

            for q in zip(Datasets.print_query_data(self.dataset), Datasets.get_query_data(self.dataset)):
                self.queries[q[0]]= q[1]

            query= col1.selectbox(" ", list(self.queries.keys()), label_visibility='hidden')
            query= self.queries[query]

            col2.text('')
            col2.text('')
            run= col2.button('Search')

        if run:
            results= Visual.models()[self.method].run(query=query['query'], dataset=self.dataset, umbral=self.threshold, limit=self.limit)
            self.show_results(results, Visual.models()[self.method])

            self.sbar.dataframe(Datasets.get_qrels_coincidence(self.dataset, query['id'], results))



    def sidebar(self):
        self.sbar= st.sidebar

        self.sbar.title("Options")
        self.method= self.sbar.selectbox("Method", list(Visual.models().keys()))

        self.dataset= self.sbar.selectbox("Dataset", ['cranfield', 'beir/arguana'])

        self.input_type= self.sbar.selectbox("Input type", ["Example queries", "Text"])

        self.sbar.markdown('-----------------')
        with self.sbar.expander(label='Options'):
            self.limit= st.number_input("Limit", min_value=0, max_value=100, value=0, step=1)
            self.threshold= st.number_input("Threshold", min_value=0.0, max_value=1.0, value=0.0, step= 0.1)


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
