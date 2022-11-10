from vector_model import *

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


a = VectorModel()
rank= a.find(' ajo de a ojo carro  mano  Perro CaSa  un  pilar DadO dado peso pollo yuca ', documentslist)
print(a.queryterms)
print(a.querysim)
print(rank)