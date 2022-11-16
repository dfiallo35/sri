import ir_datasets
from ir_datasets.datasets.cranfield import CranfieldDocs, CranfieldDoc


class Datasets:
    def __init__(self):
        self.dataset:CranfieldDocs= None
        self.documents= set()
        self.docslen= 0

    def get_dataset(self, dataset:str):
        self.dataset:CranfieldDocs = ir_datasets.load(dataset)
        for doc in self.dataset.docs_iter():
            self.documents.add(doc.doc_id)
        self.docslen= self.dataset.docs_count()

    def get_docs_data(self):
        for data in self.dataset.docs_iter():
            data:CranfieldDoc= data
            yield {'id':data.doc_id, 'text':data.text}

