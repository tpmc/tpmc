""" 
containing test object for marching subes 33 tests, eg 
face-tests, interior-test
"""
from math import log, floor
from permutation import Permutation
from transformation import Transformation
from referenceelements import ReferenceElements

def permute_faceid(faceid, perm, faces):
    """ permutes the number of a tested face """
    perm_vertices = perm*range(len(perm))
    facesets = [set(f) for f in faces]
    permface = set([perm_vertices[i] for i in facesets[faceid]])
    return facesets.index(permface)

class TestFace(object):
    """ representing test for an ambiguous face """
    def __init__(self, i, refv=0):
        self.idx = int(i)
        self.refv = int(refv)    
    def __mul__(self, perm):
        assert type(perm) is Permutation or type(perm) is Transformation
        assert len(perm) == 4 or len(perm) == 8
        if len(perm) == 8:
            dim = 3
            faces = ReferenceElements[(dim,"cube")].faces
            # get id of the permutated face
            newidx = permute_faceid(self.idx, perm, faces)
            face = faces[newidx]
            # index of refv in base_case
            refidx = faces[self.idx][self.refv]
            # perm * case = base_case
            vertices = perm * range(len(ReferenceElements[(3,"cube")]))
            # index of refv in case
            refidx2 = vertices[refidx]
            refv = [0, 1, 1, 0][face.index(refidx2)]
            return TestFace(newidx, refv)
        elif len(perm) == 4:
            vertices = perm * range(4)
            refv = [0, 1, 1, 0][vertices[refv]]
            refidx = 0
    def __repr__(self):
        return "TEST_FACE_" + repr(self.idx) + "_" + repr(self.refv)

class TestInterior(object):
    """ representing test for an ambigous interior """
    def __init__(self, refv):
        self.refv = int(refv)
    def __mul__(self, perm):
        assert type(perm) is Permutation or type(perm) is Transformation
        return TestInterior([0,1,2,3,3,2,1,0][perm[self.refv]])
    def __repr__(self):
        return "TEST_INTERIOR_" + repr(self.refv)

class TestRegular(object):
    """ dummy-object for regular case """
    def __mul__(self, perm):
        return self
    def __repr__(self):
        return "CASE_IS_REGULAR"

class TestInvalid(object):
    """ dummy-object for invalid case """
    def __mul__(self, perm):
        return self
    def __repr__(self):
        return "TEST_INVALID"

def binaryheap(entry, heap=None, index=0):
    """ creates a binary heap as a list using the triple entry """
    if heap is None:
        heap = []
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
            heap[index] = entry[0]
        else:
            assert(len(entry) == 3)
            # write myself into heap
            heap[index] = entry[0]
            index += 1
            # call children
            binaryheap(entry[1], heap, 2*index-1)
            binaryheap(entry[2], heap, 2*index)
    else:
        heap[index] = entry
    return list(heap)

# Constants for mc 33 test order
TEST_FACE_0 = TestFace(0)
TEST_FACE_1 = TestFace(1)
TEST_FACE_2 = TestFace(2)
TEST_FACE_3 = TestFace(3)
TEST_FACE_4 = TestFace(4)
TEST_FACE_5 = TestFace(5)
TEST_INTERIOR_0 = TestInterior(0)
TEST_INTERIOR_1 = TestInterior(1)
TEST_INTERIOR_2 = TestInterior(2)
TEST_INTERIOR_3 = TestInterior(3)
TEST_INVALID = TestInvalid()
CASE_IS_REGULAR = TestRegular()
