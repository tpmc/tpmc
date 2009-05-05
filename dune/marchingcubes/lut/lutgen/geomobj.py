from permutation import Permutation

class GeomObject(object):
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
    def get_flip(self):
        dim = self.dim
        l = len(self.vertices)
        if (dim, l) == (1, 2):
            return Permutation(1, (0,1))
        if (dim, l) == (2, 3):
            return Permutation(-1, (2,1,0))
        if (dim, l) == (2, 4):
            return Permutation(-1, (1,0,3,2))
        if (dim, l) == (3, 4):
            return Permutation(-1, (3,0,2,1))
        if (dim, l) == (3, 5):
            return Permutation(-1, (1,0,3,2,4))
        if (dim, l) == (3, 6):
            return Permutation(-1, (3,4,5,0,1,2))
        if (dim, l) == (3, 8):
            return Permutation(-1, (4,5,6,7,0,1,2,3))
        assert 0
    def __mul__ (self, p):
        assert type(p) is Permutation
        def f(x):
            if type(x) is int:
                return p[x]
            # return p*x
            return (p[x[0]], p[x[1]])
        entity = self.vertices
        if len(self.vertices) == 0:
            return []
        if p.orientation == -1:
            entity = self.get_flip() * entity
        return [ f(vertex) for vertex in entity ]

