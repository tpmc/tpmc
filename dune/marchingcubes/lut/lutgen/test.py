from referenceelements import *

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
        print elements
        faces = []
        for e in [e for e in elements if len(e)>0]:
            # get reference element of local element
            local_refelem = ReferenceElements[GeometryType.type(self.generator.dim, e)]
            # get the element faces
            faces += [[e[v] for v in face] for face in local_refelem.faces]
        # now faces contains all faces of all interior and exterior elements
        # now we need to find the surface
        for ref_face in self.reference_element.faces:
            # get all element faces intersecting ref_face
            intset = []
            for face in faces:
                c = [x for x in face if type(x) is int and x in ref_face] + [x for x in face if type(x) is not int and set(x).issubset(set(ref_face))]
                if len(c)>self.generator.dim-1: 
                    intset.append(face)
            print 'intset of ',ref_face
            print intset
            
        return 0
    def test_base_case(self, bc):
        if self.verbose:
            print '## testing case ',bc.name, ' (', bc.case, ')'
        (count, passed) = (0, 0)
        count += 1
        passed += self.test_interface(bc)
        count += 1
        passed += self.test_surface(bc)
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
