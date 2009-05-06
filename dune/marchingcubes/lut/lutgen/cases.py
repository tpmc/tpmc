from permutation import Permutation
from geomobj import GeomObject
from disambiguate import *

class Case(object):
    def __init__(self, x):
        self.case = x
        self.permutation = None
        self.base_case = None
        self.faces = [[]]
        self.cells = [[]]
        self.tests = []
    def __repr__(self):
        return "%s, %s, %s, %s" % (repr(self.case), repr(self.permutation),
                                   repr(self.faces), repr(self.cells))
    def update(self):
        self.faces = self.base_case.permute_faces(self.permutation)
        self.cells = self.base_case.permute_cells(self.permutation)
        self.tests = self.base_case.permute_tests(self.permutation)
        
class BaseCase(object):
    def __init__(self, dim, x):
        self.dim = dim
        self.case = x
        self.faces = [[]]
        self.cells = [[]]
        self.tests = []
    def __repr__(self):
        return "%s, %s, %s" % (repr(self.case), repr(self.faces),
                               repr(self.cells))
    def __eq__(self, other):
        return self.case == other.case
    def permute_faces(self,p):
        return [ GeomObject(self.dim-1, face) * p
                 for face in self.faces ]
    def permute_cells(self,p):
        return [ GeomObject(self.dim, cell) * p
                 for cell in self.cells ]
    def permute_single_test(self,test,p):
        if type(test) in (TestInvalid, TestRegular, TestInterior, TestFace):
            if self.dim == 3 and len(self.case) == 8:
                return test * p
            else:
                return test
        else:
            return test
        
    def permute_tests(self,p):
        return [ self.permute_single_test(test,p)
                 for test in self.tests ]

