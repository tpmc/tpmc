from permutation import Permutation
from geomobj import *
from disambiguate import *

class Triangulation(object):
    def __init__(self, f = [[]], c = [[]]):
        self.faces = f
        self.cells = c
    def __repr__(self):
        return repr(self.faces) + "::" + repr(self.cells)

class Case(object):
    def __init__(self, x):
        self.case = x
        self.permutation = None
        self.base_case = None
        self.faces = [[]]
        self.cells = [[]]
        self.tests = []
        self.mc33 = []
    def __repr__(self):
        return "%s, %s, %s, %s" % (repr(self.case), repr(self.permutation),
                                   repr(self.faces), repr(self.cells))
    def update(self):
        dim = self.base_case.dim
        def permute_single_test(test,p):
            if type(test) in (TestInvalid, TestRegular, TestInterior, TestFace):
                if dim == 3 and len(self.case) == 8:
                    return test * p
                else:
                    return test
            else:
                return test
        self.faces = permute_geom_list(dim-1, self.base_case.faces, self.permutation)
        self.cells = permute_geom_list(dim, self.base_case.cells, self.permutation)
        self.tests = [ permute_single_test(test,self.permutation) for test in self.base_case.tests ]
        self.mc33 = [ Triangulation(permute_geom_list(dim-1, t.faces, self.permutation),
                                    permute_geom_list(dim, t.cells, self.permutation))
                      for t in self.base_case.mc33 ]

class BaseCase(object):
    def __init__(self, dim, x):
        self.dim = dim
        self.case = x
        self.faces = [[]]
        self.cells = [[]]
        self.tests = []
        self.mc33 = []
    def __repr__(self):
        return "%s, %s, %s" % (repr(self.case), repr(self.faces),
                               repr(self.cells))
    def __eq__(self, other):
        return self.case == other.case
