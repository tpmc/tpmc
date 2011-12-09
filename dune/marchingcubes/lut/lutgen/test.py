from referenceelements import ReferenceElements, GeometryType
from base_case_triangulation import LookupGenerators

# returns -1 or 1
def vertex_value(test, case_index, vertex):
    return -1

class Polygon(object):
    def __init__(self, vertices):
        self.vertices = vertices
    def reverse(self):
        t = type(self.vertices)
        n = t(self.vertices)
        n.reverse()
        return Polygon(n)
    def connected(self, other):
        srev = self.reverse()
    def __lshift__(self, a):
        return Polygon(self.vertices[a:]+self.vertices[:a])
    def __rshift__(self, a):
        return self.__lshift__(-a)
    def __eq__(self, other):        
        if len(self.vertices)!=len(other.vertices):
            return False
        srev = self.reverse
        for x in range(len(self.vertices)):
            if (self >> x).vertices == other.vertices or (srev >> x).vertices == other.vertices:
                return False
        return True

class Element(object):
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
        self.reference = ReferenceElements[GeometryType.type(dim, vertices)]
    # returns a generator for the faces of this element as defined by the faces of the reference element
    def faces(self):
        return [[self.vertices[i] for i in face] for face in self.reference.faces]
    # check if the union of the subelements matches this element
    def matches(self, subelements, verbose = False):
        if self.dim == 0:
            return subelements == [self]
        # merge all faces of all subelements
        faces = [Element(element.dim-1,face) for element in subelements for face in element.faces()]
        # retrieve faces which only occur onces
        surface = [x for x in faces if faces.count(x) == 1]
        # check if every face of self can be matched by the surface-faces intersecting it
        for reference_face in [Element(self.dim-1, face) for face in self.faces()]:
            intersecting_faces = [face for face in surface if face in reference_face]            
            surface = [face for face in surface if face not in intersecting_faces]
            if not reference_face.matches(intersecting_faces, verbose):
                if verbose:
                    print '## ',reference_face,' is not matched by ', intersecting_faces
                return False
        # if there are faces in the surface which could used to match a reference face, the subelements don't match
        if len(surface)>0:
            if verbose:
                print '## following faces could no be matched with ',self, ':'
                print '## ', surface
            return False
        return True
    def polygon(self):
        assert(self.dim<2)
        if self.reference.type == (2,'cube'):
            return self.vertices[0,1,3,2]
        return self.vertices
    def __contains__(self, other):
        # check if all vertices of other are inside self
        # number of intersecting points
        a = sum(1 for x in other.vertices if x in self.vertices)
        # number of points on edges not in self, of which both adjoining vertices are in self
        b = sum(1 for x in other.vertices if type(x) is not int \
                 and x not in self.vertices \
                 and x[0] in self.vertices and x[1] in self.vertices)
        return a+b == len(other.vertices)
    # elements are equal if they contain the same vertices
    def __eq__(self, other):
        return self.dim == other.dim \
            and set(self.vertices) == set(other.vertices)
    def __repr__(self):
        return 'Element: '+repr(self.reference.type)+': '+repr(self.vertices)

class Test(object):
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometryType]
    def test_faces(self, triangulation, case_number, test_results):
        # check if the decomposition of the reference-faces based on the interior/exterior
        # matches the decomposition in lower dimension
        # test_results: face-number-->test-result
        # 0 equals left, ie outside, 1 equals right, ie inside
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        interior_faces = [Element(self.generator.dim-1,x) for element in triangulation.interior for x in element]
        exterior_faces = [Element(self.generator.dim-1,x) for element in triangulation.exterior for x in element]
        reference_faces = reference.faces()
        for ref_face in reference.faces():
            ref_face_element = Element(reference.dim-1,ref_face)
            # retrieve the decomposition of ref_face based on triangulation
            intersecting_interior = [x for x in interior_faces if x in ref_face_element]
            intersecting_exterior = [x for x in exterior_faces if x in ref_face_element]
            # now get the dim-1 dimensional decomposition of ref_face
            lower_case_number = [case_number[i] for i in ref_face.vertices]
            lower_generator = LookupGenerators[ref_face.reference.type];
            lower_case = next((case for case in lower_generator.all_cases if case.case == lower_case_number), None)
            assert(lower_case!=None)
            if len(lower_case.mc33) == 0:
                lower_triangulation = lower_case
            else:
                faceid = reference_faces.index(ref_face)
                test_result = test_results[faceid]
                lower_triangulation = lower_case.mc33[2+test_result]
            lower_interior = [Element(self.generator.dim-1, x) for x in lower_triangulation.interior]
            lower_exterior = [Element(self.generator.dim-1, x) for x in lower_triangulation.exterior]
            # compare intersecting_in/exterior with lower_in/exterior
        return 1
    def test_interface(self, triangulation):        
        def get_faces(reference, elements):
            faces = [Element(element.dim-1,face) for element in elements for face in element.faces()]
            faces = [x for x in faces if faces.count(x) != 2]
            for ref_face in (Element(reference.dim-1,x) for x in reference.faces()):
                faces = [x for x in faces if x not in ref_face]
            return faces
        def compare(a, b):
            return len(a) == len(b) and sum(1 for x in a if x in b) == len(a)
        # check if the interface between interior and exterior matches the faces of the
        # base case
        interface_base = [Element(self.generator.dim-1,x) for x in triangulation.faces if len(x)>0]
        # remove those faces from interface_base intersecting reference element
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        for ref_face in (Element(reference.dim-1,x) for x in reference.faces()):
            interface_base = [x for x in interface_base if x not in ref_face]
        for data in (triangulation.interior, triangulation.exterior):
            elements = (Element(self.generator.dim,x) for x in data if len(x)>0)
            interface = get_faces(reference, elements)
            if not compare(interface, interface_base):
                if self.verbose:
                    print 'interface: %r, base.faces: %r'%(interface, interface_base)
                    if data == triangulation.interior:
                        print '## interface of interior does not match triangulation interface'
                    else:
                        print '## interface of exterior does not match triangulation interface'
                return False
        return True
    def test_surface(self, triangulation):
        # compare the surface of the union of interior and exterior with the surface of the reference
        # element    
        elements = [Element(self.generator.dim,x) for x in triangulation.interior + triangulation.exterior if len(x)>0]
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        if not reference.matches(elements, self.verbose):
            if self.verbose:
                print '#### elements do not match reference element:'
                print '#### reference : ', self.reference_element.type
                print '#### elements: ', elements
            return 0
        return 1
    def test_triangulation(self, t, case):
        count, passed = 0,0
        count += 1
        result = self.test_interface(t)
        if self.verbose and result == 0:
            print '###### interface test for triangulation ',t.name, 'FAILED'
        passed += result
        count += 1
        result = self.test_surface(t)
        if self.verbose and result == 0:
            print '###### surface test for triangulation ',t.name, 'FAILED'
        passed += result
        # count += 1
        # result = self.test_faces(t, case)
        # if self.verbose and result == 0:
        #     print '###### faces test for triangulation ',t.name, 'FAILED'
        # passed += result
        return (count, passed)
    def test(self):
        if self.verbose:
            print '# starting test of ', self.generator.geometryType
        passed = 0
        count = 0
        for bc in self.generator.base_cases:
            (ct, pt) = self.test_triangulation(bc, bc.case)
            count += ct
            passed += pt
            for mc in bc.mc33:
                (ct, pt) = self.test_triangulation(mc, bc.case)
                count += ct
                passed += pt
        if self.verbose:
            print '# ',passed, ' of ',count, ' tests passed'
        return passed == count
