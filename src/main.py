from vector_model import *

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


a = VectorModel()
rank= a.run('pollo Pollo mesa  casa carro y de dedo mole masa perro mayonesa ', join(getcwd(), 'docs'), alpha=0.2)
print(rank)


