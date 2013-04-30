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
    and interface along with information about connected groups
    """
    def __init__(self,name = "", vertex_groups = None, faces = None, exterior = None, 
                 exterior_groups = None, interior = None, 
                 interior_groups = None):
        self.name = name
        self.vertex_groups = vertex_groups if vertex_groups is not None else []
        self.faces = faces if faces is not None else [[]]
        self.exterior = exterior if exterior is not None else [[]]
        self.exterior_groups = exterior_groups if exterior_groups is not None else []
        self.interior = interior if interior is not None else [[]]
        self.interior_groups = interior_groups if interior_groups is not None else []
    def __repr__(self):
        return "{0} - {1}::{2} - ({3})::{4} - ({5})".format(self.vertex_groups, 
                                                            self.faces, 
                                                            self.exterior, 
                                                            self.exterior_groups, 
                                                            self.interior, 
                                                            self.interior_groups)

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
    def update(self, global_type):
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
        # update the triangulation
        self.name = self.base_case.name
        self.faces = permute_geom_list(dim-1, global_type, self.base_case.faces, 
                                       self.transformation)
        self.exterior = permute_geom_list(dim, global_type, self.base_case.exterior, 
                                          self.transformation)
        self.exterior_groups = self.base_case.exterior_groups
        self.interior = permute_geom_list(dim, global_type, self.base_case.interior, 
                                          self.transformation)
        self.interior_groups = self.base_case.interior_groups
        self.tests = [ permute_single_test(test, self.transformation) 
                       for test in self.base_case.tests ]
        # update mc33 triangulations
        self.mc33 = [ Triangulation(triang.name,
                                    self.transformation*triang.vertex_groups,
                                    permute_geom_list(dim-1, global_type, triang.faces, 
                                                      self.transformation),
                                    permute_geom_list(dim, global_type, triang.exterior, 
                                                      self.transformation),
                                    triang.exterior_groups,
                                    permute_geom_list(dim, global_type, triang.interior, 
                                                      self.transformation),
                                    triang.interior_groups)
                      for triang in self.base_case.mc33 ]
        # if necessary, invert the case, ie swap interior and exterior
        if self.transformation.inverted == 1:
            self.interior, self.exterior = self.exterior, self.interior
            self.interior_groups, self.exterior_groups = self.exterior_groups, self.interior_groups
            for tri in self.mc33:
                tri.interior, tri.exterior = tri.exterior, tri.interior
                tri.interior_groups, tri.exterior_groups = tri.exterior_groups, tri.interior_groups
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
