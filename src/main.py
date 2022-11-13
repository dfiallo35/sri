from vector_model import *

documentslist= [join(getcwd(), join('docs', 'a.txt')),
                join(getcwd(), join('docs', 'b.txt')),
                join(getcwd(), join('docs', 'c.txt')),
                join(getcwd(), join('docs', 'd.txt'))
        ]


a = VectorModel()
print(a.run('leon oso nutria perro es de la casa del zorro', join(getcwd(), 'docs\\1')))