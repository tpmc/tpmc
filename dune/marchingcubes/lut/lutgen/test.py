from referenceelements import *

class Polygon(list):
    def __new__(cls, v):
        return list.__new__(cls,v)
    # returns index in face
    def connected_at(self, other):
        ls = len(self)
        lf = len(other)
        for i in range(lf):
            if other[i] in self:
                index = self.index(other[i])
                if other[(i+1)%lf] == self[(index+1)%ls]:
                    return i
        return -1
    def strip_inner_nodes(self):
        ls = len(self)
        indices = [i for i in range(ls) if type(self[i]) is not int and self[(i-1) % ls] in self[i] and self[(i+1) % ls] in self[i]]
        indices.sort()
        indices.reverse()
        for i in indices:
            self.pop(i)
    def connect(self, other, i):
        lo = len(other)
        ls = len(self)
        # extend at i
        iself = (self.index(other[i])+1) % ls
        k = (i+2) % lo
        while k!=i:
            self.insert(iself, other[k])
            k = (k+1) % lo

def remove_all_from_list(l, r):
    return [x for x in l if x not in r]
# merges the faces in faces as far as possible. faces are represented as a consecutive sequence of points
def merge_faces(faces):    
    if len(faces)<2:
        return faces
    base = faces.pop()
    changed = True
    while changed:
        changed = False
        # search for a face which can extend the base
        for face in faces:                
            i = base.connected_at(face)
            if i<0:
                face.reverse()
                i = base.connected_at(face)
            if i>=0 :
                base.connect(face,i)
                base.strip_inner_nodes()
                # remove merged face
                faces.remove(face)
                changed = True
                break
    faces.append(base)
    return faces

def equal(dim, faces1, faces2):
    def renumber_faces(faces):
        # if necessary renumber faces for polygons
        renumber = {
            (2,4): [0,1,3,2]
            }
        lf = len(faces)
        for i in range(lf):
            l = len(faces[i])
            if (dim, l) in renumber:
                faces[i] = [faces[i][j] for j in renumber[(dim,l)]]
    renumber_faces(faces1)
    renumber_faces(faces2)
    faces1 = [Polygon(x) for x in faces1]
    faces2 = [Polygon(x) for x in faces2]
    if (len(faces1) == 0) != (len(faces2) == 0):
        return False
    faces1 = merge_faces(faces1)
    faces2 = merge_faces(faces2)
    if len(faces1)>1 or len(faces2)>1:
        return False
    return set(faces1[0]) == set(faces2[0])
            
def compare_with_reference_face(dim, rface, faces):    
    if dim == 1:        
        # for dim 1 there are only 2 possible decompositions
        if len(faces) == 1:
            return set(rface) == set(faces[0])
        elif len(faces) == 2:
            a,b = faces[0],faces[1]
            return len(a) == 2 and len(b) == 2 and (set(a+b) == set([rface[0],rface[1],(rface[0],rface[1])]) or set(a+b) == set([rface[0], rface[1], (rface[1],rface[0])]))
        return False
    elif dim == 2:
        return equal(dim, [rface], faces)
    return False

def get_all_faces(dim,elements):
    faces = []
    for e in [e for e in elements if len(e)>0]:
        # get reference element of local element
        local_refelem = ReferenceElements[GeometryType.type(dim, e)]
        # get the element faces
        faces += [[e[v] for v in face] for face in local_refelem.faces]
    return faces

class Test(object):
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometryType]
    def test_interface(self, bc):
        if self.verbose:
            print '#### testing interface'
        fi = get_all_faces(self.generator.dim, bc.interior)
        fe = get_all_faces(self.generator.dim, bc.exterior)
        fi_sets = [set(x) for x in fi]
        fe_sets = [set(x) for x in fe]
        seen = set()
        interface = [x for x in fi+fe if set(x) in fi_sets and set(x) in fe_sets and frozenset(x) not in seen and not seen.add(frozenset(x))]
        # for now, just check if the interface is exactly matched
        
        if self.verbose:
            print '#### interface: ', interface
        return 0
    def test_surface(self, bc):
        if self.verbose:
            print '#### testing surface'        
        elements = bc.interior + bc.exterior
        faces = get_all_faces(self.generator.dim, elements)
        faces_sets = [set(f) for f in faces]
        surface = [x for x in faces if faces_sets.count(set(x)) == 1]
        for reference_face in self.reference_element.faces:
            intersecting_faces = []
            for f in surface:
                a = len([x for x in f if type(x) is int and x in reference_face])
                b = len([x for x in f if type(x) is not int and x[0] in reference_face and x[1] in reference_face])
                if a+b == len(f):
                    intersecting_faces.append(f)
            surface = remove_all_from_list(surface,intersecting_faces)
            if not compare_with_reference_face(self.generator.dim-1,reference_face, intersecting_faces):
                if self.verbose:
                    print '###### faces do not match reference face:'
                    print '######## reference face: ', reference_face
                    print '######## faces: ', intersecting_faces
                return 0
        if len(surface)>0:
            if self.verbose:
                print '###### surface not empty:, ', surface
            return 0
        return 1
    def test_triangulation(self, t):
        if self.verbose:
            print '## testing triangulation ',t.name
        (count, passed) = (0, 0)
        count += 1
        result = self.test_interface(t)
        if self.verbose:
            print '#### test', ['not passed', 'passed'][result]
        passed += result
        count += 1
        result = self.test_surface(t)
        if self.verbose:
            print '#### test', ['not passed', 'passed'][result]
        passed += result
        return (count, passed)
    def test(self):
        if self.verbose:
            print '# starting test of ', self.generator.geometryType
        passed = 0
        count = 0
        for bc in self.generator.base_cases:
            (ct, pt) = self.test_triangulation(bc)
            count += ct
            passed += pt
            for mc in bc.mc33:
                (ct, pt) = self.test_triangulation(mc)
                count += ct
                passed += pt
        if self.verbose:
            print '# ',passed, ' of ',count, ' tests passed'
        return passed == count
