"""
Contains the generator class for generating lookup tables for the
marching cubes 33 algorithm
"""

import logging

from pprint import pprint
from transformation import Transformation
from referenceelements import ReferenceElements
from cases import Case, BaseCase

LOGGER = logging.getLogger('lutgen.generator')

class LookupGenerator(object):
    """
    class for generating a lookup-table for different geometry-types in
    different dimensions
    Currently supported: (2, simplex), (3, simplex), (2, cube), 
      (3, cube), (4, cube)
    """
    def __init__(self, dim, basic_type):
        self.dim = dim
        self.basic_type = basic_type
        self.geometry_type = (dim, basic_type)
        self.ref_elem = ReferenceElements[self.geometry_type]
        self.p_size = len(self.ref_elem)
        LOGGER.info("dim = {0}; p_size = {1}; ".format(self.dim, 
                                                       self.p_size))

        # Generate transformation group from generators
        # ie all valid transformations
        generators = self.get_generators()
        # start with identity and inverted identity
        self.transformation_group = set([Transformation(1, 0, 
                                                        range(self.p_size)) ,
                                         Transformation(1, 1, 
                                                        range(self.p_size))])
        i = 0
        g_size = 0
        # apply all generator-transformations to all elements in G, until
        # nothing changes anymore
        while len(self.transformation_group) != g_size:
            g_size = len(self.transformation_group)
            new_group = set()
            for trans in self.transformation_group:
                for perm in generators:
                    new_group.add(perm*trans)
            self.transformation_group = \
                self.transformation_group.union(new_group)
            i += 1
        LOGGER.info("g_size: {0}; wortlaenge: {1}".format(g_size, i-1))

        # Generate list of base cases
        # and save base case and permutation for each case
        self.all_cases = [Case(dim, tuple((i >> x) & 1 
                                          for x in range(self.p_size)))
                          for i in range(1<<self.p_size)]
        self.base_cases = []

        # for every case, check if it can be constructed from a base case
        # using the transformation group. If not, the case is marked as
        # a base case
        for entry in self.all_cases:
            found = False
            for trans in self.transformation_group:
                base_case = BaseCase(dim, trans**entry.case)
                if base_case in self.base_cases:
                    found = True
                    entry.transformation = trans
                    entry.base_case = \
                        self.base_cases[self.base_cases.index(base_case)]
                    break
            if not found:
                self.base_cases.append(BaseCase(dim, entry.case))
                entry.transformation = Transformation(1, 0, range(self.p_size))
                entry.base_case = self.base_cases[-1]
    def get_generators(self):
        """
        returns a list of transformations which can generate the transformations
        according to the symmetries of the given geometry type
        """
        if self.dim == 0:
            return []
        elif self.dim == 1:
            return [Transformation(1, 0, (1, 0))]
        elif self.geometry_type == (2,"simplex"):
            return [Transformation(1, 0, (1, 2, 0))]
        elif self.geometry_type == (2,"cube"):
            return [Transformation(1, 0, (1, 3, 0, 2))]
        elif self.geometry_type == (3,"simplex"):
            return [Transformation(1, 0, (3, 1, 0, 2)),
                    Transformation(1, 0, (3, 0, 2, 1))]
        elif self.geometry_type == (3,"cube"): # mirror, rotate, rotate
            return [Transformation(-1, 0, (4, 5, 6, 7, 0, 1, 2, 3)),
                    Transformation(1, 0, (1, 5, 3, 7, 0, 4, 2, 6)),
                    Transformation(1, 0, (1, 3, 0, 2, 5, 7, 4, 6))]
        elif self.geometry_type == (3,"prism"):
            assert 0
        elif self.geometry_type == (3,"pyramid"):
            assert 0
        elif self.geometry_type == (4,"cube"):
            return [Transformation(-1, 0, (8,9,10,11,12,13,14,15,
                                           0,1,2,3,4,5,6,7)),
                    Transformation(1, 0, (2,3,6,7,10,11,14,15,0,
                                          1,4,5,8,9,12,13)),
                    Transformation(1, 0, (1,5,3,7,9,13,11,15,0,4,
                                          2,6,8,12,10,14)),
                    Transformation(1, 0, (1,3,9,11,5,7,13,15,0,2,
                                          8,10,4,6,12,14))]
        assert 0
    def generate(self):
        """
        call update method of every case to let it fetch its triangulation 
        from its base case.
        """        
        for entry in self.all_cases:
            entry.update()

    def print_base(self, prefix="lut", face_count=0, cell_count=0):
        """ print all base cases """
        print '# base cases {0} {1}D'.format(self.basic_type, self.dim)
        for (i, entry) in enumerate(self.base_cases):
            case = list(entry.case)
            case.reverse()
            print '# {0} -> {1}'.format(",".join(str(x) for x in entry.case),
                                        "".join(str(x) for x in case))
            while len(entry.faces) < face_count:
                entry.faces.append([])
            print '{0}.base_cases[{1}].faces = {2}'.format(prefix, i,
                                                           entry.faces)
            while len(entry.exterior) < cell_count:
                entry.exterior.append([])
            print '{0}.base_cases[{1}].exterior = {2}'.format(prefix, i,
                                                              entry.exterior)
            while len(entry.interior) < cell_count:
                entry.interior.append([])
            print '{0}.base_cases[{1}].interior = {2}'.format(prefix, i,
                                                              entry.interior)
        print

    def print_info(self):
        """ print all information on this generator """
        trans_list = list(self.transformation_group)
        trans_list.sort()
        print len(self.transformation_group)
        pprint(trans_list)

        print len(self.base_cases)
        pprint(self.base_cases)

        print len(self.all_cases)
        pprint(self.all_cases)
