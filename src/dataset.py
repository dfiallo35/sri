import ir_datasets
from ir_datasets.datasets.cranfield import CranfieldDocs, CranfieldDoc


class Datasets:
    def __init__(self):
        self.dataset:CranfieldDocs= None
        self.documents= set()
        self.docslen= 0
        self.dataset_name= None

    def get_dataset(self, dataset:str):
        self.dataset_name= dataset
        self.dataset:CranfieldDocs = ir_datasets.load(dataset)
        for doc in self.dataset.docs_iter():
            self.documents.add(doc.doc_id)
        self.docslen= self.dataset.docs_count()

    def get_docs_data(self):
        return [{'id':data.doc_id, 'text':data.text} for data in self.dataset.docs_iter()]

    def get_query_data(dataset: str):
        return [data.text for data in ir_datasets.load(dataset).queries_iter()]


# a= ir_datasets.load('gov2')
# for i in a.docs_iter():
#     print(i)