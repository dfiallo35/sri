import vector_model as vm
import numpy as np

terms=['requerimientos','clase','class','trabajo', 'clase','class']
documents=['./src/script.txt','./src/script2.txt']

freq=vm.get_terms_frequency(terms, documents)
print(f"freq:{freq}")


tf,idf=vm.get_tf_idf(freq)
print(f"Tf:{tf}")
print(f"Idf:{idf}")

w=vm.get_terms_weight(tf,idf)
print(f"w:{w}")

wq=vm.get_query_weight(terms,idf,0.5)
print(f"wq:{wq}")

sim=vm.get_similarity(w,wq)
print(f"sim:{sim}")

ranking=vm.get_ranking(sim, documents)
print(f"ranking:{ranking}")

