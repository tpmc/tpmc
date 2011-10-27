from pprint import pprint
from permutation import Permutation
from transformation import Transformation
from referenceelements import ReferenceElements
from cases import *

class LookupGenerator(object):
    def __init__(self, dim, basicType, verbose=False):
        self.dim = dim
        self.basicType = basicType
        self.geometryType = (dim,basicType)
        self.refElem = ReferenceElements[self.geometryType]
        self.p_size = len(self.refElem)
        if verbose:
            print "dim = %i\np_size = %i\ng_size = \n" \
                  % (self.dim, self.p_size)

        # Generate Permutation Group from generators
        P = self.get_generators()
        self.G = set([Transformation(1,0,range(self.p_size)),Transformation(1,1,range(self.p_size))])
        i = 0
        g_size = 0
        while len(self.G) != g_size:
            g_size = len(self.G)
            H = set()
            for g in self.G:
                for p in P:
                    H.add(p*g)
            self.G = self.G.union(H)
            i+=1
        if verbose:
            print "g_size:",g_size
            print "wortlaenge:",i-1

        # Generate list of base cases
        # and save base case and permutation for each case
        self.all_cases = [Case(tuple((i >> x) & 1 for x in range(self.p_size)))
                          for i in range(1<<self.p_size)]
        self.base_cases = []

        for entry in self.all_cases:
            found = False
            for g in self.G:
                bc = BaseCase(dim, g**entry.case)
                if bc in self.base_cases:
                    found = True
                    entry.transformation = g
                    entry.base_case = self.base_cases[self.base_cases.index(bc)]
                    break
            if not found:
                self.base_cases.append(BaseCase(dim, entry.case))
                entry.transformation = Transformation(1,0,range(self.p_size))
                entry.base_case = self.base_cases[-1]

    def get_generators(self):
        if self.dim == 0:
            return []
        elif self.dim == 1:
            return [Transformation(1, 0, (1,0))]
        elif self.geometryType == (2,"simplex"):
            return [Transformation(1, 0, (1,2,0))]
        elif self.geometryType == (2,"cube"):
            return [Transformation(1, 0, (1,3,0,2))]
        elif self.geometryType == (3,"simplex"):
            return [Transformation(1, 0, (3,1,0,2)),
                    Transformation(1, 0, (3,0,2,1))]
        elif self.geometryType == (3,"cube"):
            return [Transformation(-1, 0, (4,5,6,7,0,1,2,3)),
                    Transformation(1, 0, (1,5,3,7,0,4,2,6)),
                    Transformation(1, 0, (1,3,0,2,5,7,4,6))]
        elif self.geometryType == (3,"prism"):
            assert 0
        elif self.geometryType == (3,"pyramid"):
            assert 0
        elif self.geometryType == (4,"cube"):
            return [Transformation(-1, 0, (8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7)),
                    Transformation(1, 0, (2,3,6,7,10,11,14,15,0,1,4,5,8,9,12,13)),
                    Transformation(1, 0, (1,5,3,7,9,13,11,15,0,4,2,6,8,12,10,14)),
                    Transformation(1, 0, (1,3,9,11,5,7,13,15,0,2,8,10,4,6,12,14))]
        assert 0

    def generate(self):
        # Generate lookup entries from base cases
        for entry in self.all_cases:
            entry.update()

    def print_base(self, foo="lut", f=0, c=0):
        print "# base cases %s %iD:" % (self.basicType, self.dim)
        i = 0
        for entry in self.base_cases:
            e = list(entry.case)
            e.reverse()
            print "# " + ",".join(map(str,entry.case)) + " -> " + "".join(map(str,e))
            while len(entry.faces) < f:
                entry.faces.append([])
            print foo + ".base_cases[%i].faces = " % i + repr(entry.faces)
            while len(entry.cells) < c:
                entry.cells.append([])
            print foo + ".base_cases[%i].cells = " % i + repr(entry.cells)
            i += 1
        print

    def print_info(self):
        l = list(self.G)
        l.sort()
        print len(self.G)
        pprint(l)

        print len(self.base_cases)
        pprint(self.base_cases)

        print len(self.all_cases)
        pprint(self.all_cases)
