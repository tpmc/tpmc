from math import log, floor
from permutation import Permutation
from transformation import Transformation
from geomobj import GeomObject
from referenceelements import ReferenceElements

class TestFace(object):
    def __init__(self, i, v=0):
        self.idx = int(i)
        self.refv = int(v)
    def permute_faceid(self, faceid, p, faces):        
        v = p*range(len(p))
        facesets = [set(f) for f in faces]
        permface = set([v.index(i) for i in facesets[faceid]])
        return facesets.index(permface)
    def __mul__(self, p):
        assert type(p) is Permutation or type(p) is Transformation
        assert len(p) == 4 or len(p) == 8
        if len(p) == 8:
            dim = 3
            faces = ReferenceElements[(dim,"cube")].faces
            # get id of the permutated face
            newidx = self.permute_faceid(self.idx,p , faces)
            face = faces[newidx]
            refidx = faces[self.idx][self.refv]
            vertices = p * range(len(ReferenceElements[(3,"cube")]))
            refidx2 = vertices.index(refidx)
            refv = [0, 1, 1, 0][face.index(refidx2)]
            return TestFace(newidx, refv)
        elif len(p) == 4:
            vertices = p * range(4)
            refv = [0, 1, 1, 0][vertices.index(refv)]
            refidx = 0
    def __repr__(self):
        return "TEST_FACE_" + repr(self.idx) + "_" + repr(self.refv)

class TestInterior(object):
    def __init__(self, v):
        self.refv = int(v)
    def __mul__(self, p):
        assert type(p) is Permutation or type(p) is Transformation
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
TEST_INTERIOR_0 = TestInterior(0)
TEST_INTERIOR_1 = TestInterior(1)
TEST_INTERIOR_2 = TestInterior(2)
TEST_INTERIOR_3 = TestInterior(3)
TEST_INVALID = TestInvalid()
CASE_IS_REGULAR = TestRegular()
