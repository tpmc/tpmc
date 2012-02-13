"""
contains classes for the description of marching cubes cases, including
triangulation and base cases
"""

from math import log, floor
from geomobj import permute_geom_list
from disambiguate import TestInvalid, TestRegular, TestInterior, TestFace

class Triangulation(object):
    """
    class containg a triangulation of an object into interior, exterior
    and interface
    """
    def __init__(self, faces = None, exterior = None, interior = None):
        self.name = ""
        self.faces = faces if faces is not None else [[]]
        self.exterior = exterior if exterior is not None else [[]]
        self.interior = interior if interior is not None else [[]]
    def __repr__(self):
        return "{0}::{1}::{2}".format(self.faces, self.exterior, self.interior)

class BaseCase(Triangulation):
    """
    class representing a marching cubes base case, ie a triangulation of the
    object with a list of tests to be performed and a list of mc33
    triangulations to be used according to the test results
    """
    def __init__(self, dim, case):
        Triangulation.__init__(self)
        self.dim = dim
        self.case = case
        self.tests = []
        self.mc33 = []
    def __repr__(self):
        return "{0}: {1}".format("".join(str(x) for x in self.case), 
                                 Triangulation.__repr__(self))
    def __eq__(self, other):
        return self.case == other.case

class Case(BaseCase):
    """
    class representing a normal marching cubes case. it can be transformed to
    a base case using a given transformation.
    """
    def __init__(self, dim, case):
        BaseCase.__init__(self, dim, case)
        self.transformation = None
        self.base_case = None
    def __repr__(self):
        return "{0}, {1}".format(BaseCase.__repr__(self), self.transformation)
    def update(self):
        """
        updates itself according to its base case using the transformation
        stored.
        """
        dim = self.base_case.dim
        def permute_single_test(test, perm):
            """ permutes the test (eg face-number) """
            if type(test) in (TestInvalid, TestRegular, TestInterior, TestFace):
                if dim == 3 and (len(self.case) == 8 or len(self.case) == 6):
                    return test * perm
                else:
                    return test
            else:
                return test
        # update the triangulation #
        self.faces = permute_geom_list(dim-1, self.base_case.faces, 
                                       self.transformation)
        self.exterior = permute_geom_list(dim, self.base_case.exterior, 
                                          self.transformation)
        self.interior = permute_geom_list(dim, self.base_case.interior, 
                                          self.transformation)
        self.tests = [ permute_single_test(test, self.transformation) 
                       for test in self.base_case.tests ]
        # update mc33 triangulations
        self.mc33 = [ Triangulation(permute_geom_list(dim-1, triang.faces, 
                                                      self.transformation),
                                    permute_geom_list(dim, triang.exterior, 
                                                      self.transformation),
                                    permute_geom_list(dim, triang.interior, 
                                                      self.transformation))
                      for triang in self.base_case.mc33 ]
        # if necessary, invert the case, ie swap interior and exterior
        if self.transformation.inverted == 1:
            self.interior, self.exterior = self.exterior, self.interior
            for tri in self.mc33:
                tri.interior, tri.exterior = tri.exterior, tri.interior
            # mirror the test heap
            def swap_subtrees(tree, index):
                count = 0
                while index < len(tree):
                    left = 2*index+1
                    if count>0:
                        right = index+count
                        tree[index:right], tree[right:right+count] = tree[right:right+count], tree[index:right]
                        count *= 2
                    else:
                        count = 1
                    index = left
            count = len(self.tests)
            index = 0;
            while 2*index+1 < len(self.tests):
                # no swap for InteriorTest
                if type(self.tests[index]) is not TestInterior:
                    swap_subtrees(self.tests, index)
                index += 1
