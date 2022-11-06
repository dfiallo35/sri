import vector_model as vm
import numpy as np
a=vm.get_terms_frequency(terms=['requerimientos','clase','class','trabajo'], 
                         documents=['./src/script.txt','./src/script2.txt'])
                        # documents=['./docs/Search Engine Optimization.docx','./docs/Seminario2(C++11,C++14).pdf','./docs/Seminario1(C++98).pdf',
                        # './docs/Seminario4(Golang).pdf'])
print(a)
tf,idf=vm.get_tf_idf(a)
print(f"Tf:{tf}")
print(f"Idf:{idf}")

w=vm.get_term_weight(tf,idf)
print(f"w:{w}")


# print(a[0][1])
# items = open("script.txt", 'r')
# lists = items.read().split("\n")
# lists = [item.split() for item in lists]
