from referenceelements import *

class Element(object):
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
        self.reference = ReferenceElements[GeometryType.type(dim, vertices)]
    def faces(self):
        return [[self.vertices[i] for i in face] for face in self.reference.faces]
    # check if the union of the subelements matches this element
    def matches(self, subelements, verbose = False):
        if self.dim == 0:
            return subelements == [self]
        faces = [Element(element.dim-1,face) for element in subelements for face in element.faces()]
        surface = [x for x in faces if faces.count(x) == 1]
        for reference_face in (Element(self.dim-1, face) for face in self.faces()):
            intersecting_faces = [face for face in surface if face in reference_face]            
            surface = [face for face in surface if face not in intersecting_faces]
            if not reference_face.matches(intersecting_faces, verbose):
                if verbose:
                    print '## ',reference_face,' is not matched by ', intersecting_faces
                return False
        if len(surface)>0:
            if verbose:
                print '## following faces could no be matched with ',self, ':'
                print '## ', surface
            return False
        return True
    def __contains__(self, other):
        # check if all vertices of other are inside self
        # number of intersecting points
        a = sum(1 for x in other.vertices if x in self.vertices)
        # number of points on edges not in self, of which both adjoining vertices are in self
        b = sum(1 for x in other.vertices if type(x) is not int \
                 and x not in self.vertices \
                 and x[0] in self.vertices and x[1] in self.vertices)
        return a+b == len(other.vertices)
    def __eq__(self, other):
        return self.dim == other.dim \
            and set(self.vertices) == set(other.vertices)
    def __repr__(self):
        return 'Element: '+repr(self.dim)+'D: '+repr(self.vertices)

class Test(object):
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometryType]
    def test_interface(self, bc):
        def get_faces(reference, elements):
            faces = [Element(element.dim-1,face) for element in elements for face in element.faces()]
            faces = [x for x in faces if faces.count(x) == 1]
            for ref_face in (Element(reference.dim-1,x) for x in reference.faces()):
                faces = [x for x in faces if x not in ref_face]
            return faces
        def compare(a, b):
            return len(a) == len(b) and sum(1 for x in a if x in b) == len(a)
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        elements_interior = (Element(self.generator.dim,x) for x in bc.interior if len(x)>0)
        elements_exterior = (Element(self.generator.dim,x) for x in bc.exterior if len(x)>0)
        interface_interior = get_faces(reference, elements_interior)
        interface_exterior = get_faces(reference, elements_exterior)
        interface_base = [Element(self.generator.dim-1,x) for x in bc.faces if len(x)>0]
        # remove those faces from interface_base intersecting reference element
        for ref_face in (Element(reference.dim-1,x) for x in reference.faces()):
            interface_base = [x for x in interface_base if x not in ref_face]
        res_exterior = compare(interface_exterior, interface_base)
        res_interior = compare(interface_interior, interface_base)
        if self.verbose:
            if not res_exterior:
                print '## interface of exterior does not match bc interface'
            if not res_interior:
                print '## interface of interior does not match bc interface'
        return res_exterior and res_interior
    def test_surface(self, bc):
        # compare the surface of the union of interior and exterior with the surface of the reference
        # element    
        elements = [Element(self.generator.dim,x) for x in bc.interior + bc.exterior if len(x)>0]
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        if not reference.matches(elements, self.verbose):
            if self.verbose:
                print '#### elements do not match reference element:'
                print '#### reference : ', self.reference_element.type
                print '#### elements: ', elements
            return 0
        return 1
    def test_triangulation(self, t):
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
