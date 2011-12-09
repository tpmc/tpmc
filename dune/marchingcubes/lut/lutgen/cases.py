from geomobj import *
from disambiguate import *

class Triangulation(object):
    def __init__(self, f = [[]], e = [[]], i = [[]]):
        self.name = ""
        self.faces = f
        self.exterior = e
        self.interior = i
    def __repr__(self):
        return repr(self.faces) + "::" + repr(self.exterior) \
            + "::" + repr(self.interior)

class Case(object):
    def __init__(self, x):
        self.case = x
        self.transformation = None
        self.base_case = None
        self.faces = [[]]
        self.exterior = [[]]
        self.interior = [[]]
        self.tests = []
        self.mc33 = []
    def __repr__(self):
        return "%s, %s, %s, %s, %s" % \
            (repr(self.case), repr(self.transformation), repr(self.faces)\
                 , repr(self.exterior), repr(self.interior))
    def update(self):
        # updates itself according to the base-case-triangulation
        dim = self.base_case.dim
        def permute_single_test(test,p):
            if type(test) in (TestInvalid, TestRegular, TestInterior, TestFace):
                if dim == 3 and len(self.case) == 8:
                    return test * p
                else:
                    return test
            else:
                return test
        self.faces = permute_geom_list(dim-1, self.base_case.faces\
                                           , self.transformation)
        self.exterior = permute_geom_list(dim, self.base_case.exterior\
                                              , self.transformation)
        self.interior = permute_geom_list(dim, self.base_case.interior\
                                              , self.transformation)
        self.tests = [ permute_single_test(test,self.transformation) \
                           for test in self.base_case.tests ]
        self.mc33 = [ Triangulation(\
                permute_geom_list(dim-1, t.faces, self.transformation),
                permute_geom_list(dim, t.interior, self.transformation),
                permute_geom_list(dim, t.exterior, self.transformation))
                      for t in self.base_case.mc33 ]
        if self.transformation.inverted == 1:
            self.interior, self.exterior = self.exterior, self.interior
            for t in self.mc33:
                t.interior, t.exterior = t.exterior, t.interior
    def find_symmetries(self, group):        
        return [p for p in group if p*self.case == self.case]
class BaseCase(object):
    def __init__(self, dim, x):
        self.name = ""
        self.dim = dim
        self.case = x
        self.faces = [[]]
        self.exterior = [[]]
        self.interior = [[]]
        self.tests = []
        self.mc33 = []
    def __repr__(self):
        return "%s, %s, %s, %s" % (repr(self.case), repr(self.faces),
                               repr(self.exterior), repr(self.interior))
    def __eq__(self, other):
        return self.case == other.case
