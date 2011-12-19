from permutation import Permutation
from transformation import Transformation

class GeomObject(object):
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
    def get_flip(self):
        dim = self.dim
        count = len(self.vertices)
        if (dim, count) == (1, 2):
            return Permutation(1, (0, 1))
        if (dim, count) == (2, 3):
            return Permutation(-1, (2, 1, 0))
        if (dim, count) == (2, 4):
            return Permutation(-1, (1, 0, 3, 2))
        if (dim, count) == (3, 4):
            return Permutation(-1, (3, 0, 2, 1))
        if (dim, count) == (3, 5):
            return Permutation(-1, (1, 0, 3, 2, 4))
        if (dim, count) == (3, 6):
            return Permutation(-1, (3, 4, 5, 0, 1, 2))
        if (dim, count) == (3, 8):
            return Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3))
        print "error: unkown geom obj %id, %i vertices" % (dim, count)
        assert 0
    def __mul__ (self, perm):
        assert type(perm) is Permutation or type(perm) is Transformation
        def apply_perm(vertex):
            if type(vertex) is int:
                return perm[vertex]
            # return perm*vertex
            return tuple(sorted((perm[vertex[0]], perm[vertex[1]])))
        entity = self.vertices
        if len(self.vertices) == 0:
            return []
        if perm.orientation == -1:
            entity = self.get_flip() * entity
        return [ apply_perm(vertex) for vertex in entity ]

def permute_geom_list(dim, entities, perm):
    return [ GeomObject(dim, e) * perm for e in entities ]
