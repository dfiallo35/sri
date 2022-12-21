
from ir_datasets import load

for dataset in ['cranfield', 'vaswani']:
    ds= load(dataset)
    print('downloading....')
    for i in ds.docs_iter():
        i