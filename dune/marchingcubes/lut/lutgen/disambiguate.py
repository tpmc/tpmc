from math import log, floor
from permutation import Permutation

class TestFace(object):
    def __init__(self, i, v=0):
        self.idx = int(i)
        self.refv = int(v)
    # Calculate face number with respect to permutation
    def permute_faceid(self, face, permutation):
        permutations = {(0, 1, 2, 3): [0, 1, 2, 3, 4, 5], \
                        (0, 2, 4, 6): [2, 3, 4, 5, 0, 1], \
                        (0, 4, 1, 5): [4, 5, 0, 1, 2, 3], \
                        (0, 4, 2, 6): [4, 5, 2, 3, 0, 1], \
                        (1, 0, 3, 2): [1, 0, 2, 3, 4, 5], \
                        (1, 3, 5, 7): [2, 3, 4, 5, 1, 0], \
                        (1, 5, 0, 4): [4, 5, 1, 0, 2, 3], \
                        (2, 0, 3, 1): [3, 2, 0, 1, 4, 5], \
                        (2, 0, 6, 4): [3, 2, 4, 5, 0, 1], \
                        (2, 3, 6, 7): [0, 1, 4, 5, 3, 2], \
                        (2, 6, 0, 4): [4, 5, 3, 2, 0, 1], \
                        (2, 6, 3, 7): [4, 5, 0, 1, 3, 2], \
                        (3, 1, 2, 0): [3, 2, 1, 0, 4, 5], \
                        (3, 1, 7, 5): [3, 2, 4, 5, 1, 0], \
                        (3, 2, 1, 0): [1, 0, 2, 3, 4, 5], \
                        (3, 2, 7, 6): [1, 0, 4, 5, 2, 3], \
                        (3, 7, 2, 6): [4, 5, 1, 0, 3, 2], \
                        (4, 0, 5, 1): [5, 4, 0, 1, 2, 3], \
                        (4, 0, 6, 2): [5, 4, 2, 3, 0, 1], \
                        (4, 5, 6, 7): [0, 1, 2, 3, 5, 4], \
                        (4, 6, 0, 2): [2, 3, 5, 4, 0, 1], \
                        (5, 1, 4, 0): [5, 4, 1, 0, 2, 3], \
                        (5, 1, 7, 3): [5, 4, 2, 3, 1, 0], \
                        (5, 4, 7, 6): [1, 0, 2, 3, 5, 4], \
                        (5, 7, 1, 3): [2, 3, 5, 4, 1, 0], \
                        (5, 7, 4, 6): [2, 3, 1, 0, 5, 4], \
                        (6, 2, 7, 3): [5, 4, 0, 1, 3, 2], \
                        (6, 4, 2, 0): [3, 2, 5, 4, 0, 1], \
                        (6, 4, 7, 5): [3, 2, 0, 1, 5, 4], \
                        (6, 7, 2, 3): [0, 1, 5, 4, 3, 2], \
                        (6, 7, 4, 5): [0, 1, 3, 2, 5, 4], \
                        (7, 3, 6, 2): [5, 4, 1, 0, 3, 2], \
                        (7, 5, 6, 4): [3, 2, 1, 0, 5, 4], \
                        (7, 5, 3, 1): [3, 2, 5, 4, 1, 0], \
                        (7, 6, 3, 2): [1, 0, 5, 4, 3, 2]};
        return permutations[permutation[0:4]][face]
    def __mul__(self, p):
        assert type(p) is Permutation
        # TODO refv funktioniert noch nicht
        return TestFace(self.permute_faceid(self.idx,p), p[self.refv])
    def __repr__(self):
        return "TEST_FACE_" + repr(self.idx)

class TestInterior(object):
    def __init__(self, v):
        self.refv = int(v)
    def __mul__(self, p):
        assert type(p) is Permutation
        return TestInterior(p[self.refv]%4)
    def __repr__(self):
        return "TEST_INTERIOR_" + repr(self.refv)

class TestRegular(object):
    def __mul__(self, p):
        return self
    def __repr__(self):
        return "CASE_IS_REGULAR"

class TestInvalid(object):
    def __mul__(self, p):
        return self
    def __repr__(self):
        return "TEST_INVALID"

def binaryheap(entry, heap=[], index=0):
    if index == 0:
        del heap[:]
        heap += [TestInvalid()]
    # ensure heap size, we need 2^(level+1)-1 entries
    level = int(floor(log(index+1)/log(2)))
    required = ((1<<level+1)-1)
    if len(heap) < required:
        append = required - len(heap)
        heap += [TestInvalid()]*append
    # process the entry
    if type(entry) is tuple:
        if len(entry) == 1:
            heap[index]=entry[0]
        else:
            assert(len(entry) == 3)
            # write myself into heap
            heap[index]=entry[0]
            index+=1
            # call children
            binaryheap(entry[1], heap, 2*index-1)
            binaryheap(entry[2], heap, 2*index)
    else:
        heap[index]=entry
    return list(heap)

# Constants for mc 33 test order
TEST_FACE_0 = TestFace(0)
TEST_FACE_1 = TestFace(1)
TEST_FACE_2 = TestFace(2)
TEST_FACE_3 = TestFace(3)
TEST_FACE_4 = TestFace(4)
TEST_FACE_5 = TestFace(5)
TEST_CENTER = TestInterior(0)
TEST_INTERIOR_0 = TestInterior(0)
TEST_INTERIOR_1 = TestInterior(1)
TEST_INTERIOR_2 = TestInterior(2)
TEST_INTERIOR_3 = TestInterior(3)
TEST_INVALID = TestInvalid()
CASE_IS_REGULAR = TestRegular()
