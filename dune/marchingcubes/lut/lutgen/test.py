from referenceelements import *

def remove_all_from_list(l, r):
    return [x for x in l if x not in r]

def compare_with_reference_face(dim, reference_face, intersecting_faces):
    # returns index in face
    def can_extend(base, face):
        lb = len(base)
        lf = len(face)
        for i in range(len(face)):
            if face[i] in base:
                index = base.index(face[i])
                if face[(i+1)%lf] == base[(index+1)%lb]:
                    return i
        return -1
    renumber = {
        (2,4): [0,1,3,2]
        }
    l = len(reference_face)
    if (dim, l) in renumber:
        reference_face = [reference_face[i] for i in renumber[(dim, l)]]
    renumbered_faces = []
    for face in intersecting_faces:
        l = len(face)
        if (dim, l) in renumber:
            renumbered_faces.append([face[i] for i in renumber[(dim,l)]])
        else:
            renumbered_faces.append(face)
    if len(intersecting_faces) == 0:
        return False
    base = renumbered_faces.pop()
    if dim == 2:
        changed = True
        while changed:
            changed = False
            # search for a face which can extend the base
            for face in renumbered_faces:                
                i = can_extend(base,face)
                if i<0:
                    face.reverse()
                    i = can_extend(base,face)
                if i>=0 :
                    lf = len(face)
                    lb = len(base)
                    # extend at i
                    ibase = (base.index(face[i])+1) % lb
                    k = (i+2) % lf
                    while k!=i:
                        base.insert(ibase, face[k])
                        k = (k+1) % lf
                    # remove inner nodes
                    lb = len(base)
                    indices = [i for i in range(lb) if type(base[i]) is not int and base[(i-1) % lb] in base[i] and base[(i+1) % lb] in base[i]]
                    indices.sort()
                    indices.reverse()
                    for i in indices:
                        base.pop(i)
                    # remove merged face
                    renumbered_faces.remove(face)
                    changed = True
                    break
        if len(renumbered_faces)>0:
            return False
        if set(reference_face) == set(base):
            return True
    return False

class Test(object):
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometryType]
    def test_interface(self, bc):
        if self.verbose:
            print '#### testing interface'
        return 0
    def test_surface(self, bc):
        if self.verbose:
            print '#### testing surface'        
        elements = bc.interior + bc.exterior
        faces = []
        for e in [e for e in elements if len(e)>0]:
            # get reference element of local element
            local_refelem = ReferenceElements[GeometryType.type(self.generator.dim, e)]
            # get the element faces
            faces += [[e[v] for v in face] for face in local_refelem.faces]
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
    def test_base_case(self, bc):
        if self.verbose:
            print '## testing case ',bc.name, ' (', bc.case, ')'
        (count, passed) = (0, 0)
        count += 1
        result = self.test_interface(bc)
        if self.verbose:
            print '#### test', ['not passed', 'passed'][result]
        passed += result
        count += 1
        result = self.test_surface(bc)
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
            (ct, pt) = self.test_base_case(bc)
            count += ct
            passed += pt
        if self.verbose:
            print '# ',passed, ' of ',count, ' tests passed'
        return passed == count
