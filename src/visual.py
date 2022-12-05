import streamlit as st
from vector_model import *
import os
from PIL import Image

def main():
    img_dir= os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)) , os.path.join('imgs', 'logo.png')))
    st.image(Image.open(img_dir), width= 200)
    method, dataset, limit, threshold, sensitive= sidebar()
    col1, col2= st.columns([4,1])
    query= col1.text_input("", key="different")
    col2.text('')
    col2.text('')
    run= col2.button('Search')
    
    if limit == 0:
        limit= 100
    if threshold == 0.0:
        threshold= None

    models= {'Vector Model': VectorModel()}
    if run:
        results= models[method].run(query=query, dataset=dataset, umbral=threshold, sensitive=sensitive, limit=limit)
        show_results(results, models[method])



def sidebar():
    sidebar= st.sidebar
    sidebar.title("Options")
    method= sidebar.selectbox("Method", ["Vector Model", "Probabilistic Model", "Generalized Vector Model"])
    dataset= sidebar.selectbox("Dataset", ["cranfield"])
    example_queries= sidebar.selectbox("Example Queries", Datasets.get_query_data(dataset))
    limit= sidebar.number_input("Limit", min_value=0, max_value=100, value=0, step=1)
    threshold= sidebar.number_input("Threshold", min_value=0.0, max_value=1.0, value=0.0, step= 0.1)
    sensitive= sidebar.checkbox("Sensitive", value=False)

    return method, dataset, limit, threshold, sensitive


def show_results(results, model: Model):
    for result in results:
        doc: Datasets= model.dataset.dataset.docs_iter()[int(result[0])]
        with st.expander(label=f'Document: {result[0]}'):
            st.text('Title: ' + doc.title)
            st.text(f"Similarity: {result[1]}")
            st.text('Content:')
            st.text(doc.text)


main()
