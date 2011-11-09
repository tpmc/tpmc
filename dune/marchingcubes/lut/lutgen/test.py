from referenceelements import *

class Element(object):
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
        self.reference = ReferenceElements[GeometryType.type(dim, vertices)]
    def faces(self):
        return [[self.vertices[i] for i in face] for face in self.reference.faces]
    # check if the union of the subelements matches this element
    def matches(self, subelements):
        if self.dim == 0:
            return subelements == [self]
        faces = [Element(element.dim-1,face) for element in subelements for face in element.faces()]
        faces_sets = [set(f.vertices) for f in faces]
        surface = [x for x in faces if faces_sets.count(set(x.vertices)) == 1]
        for reference_face in [Element(self.dim-1, face) for face in self.faces()]:
            intersecting_faces = [face for face in surface if face in reference_face]            
            surface = [face for face in surface if face not in intersecting_faces]
            if not reference_face.matches(intersecting_faces):
                return False
        if len(surface)>0:
            return False
        return True
    def __contains__(self, other):
        # check if all vertices of other are inside self
        # number of intersecting points
        a = len([x for x in other.vertices if x in self.vertices])   
        # number of points on edges not in self, of which both adjoining vertices are in self
        b = len([x for x in other.vertices if type(x) is not int \
                 and x not in self.vertices \
                 and x[0] in self.vertices and x[1] in self.vertices])
        return a+b == len(other.vertices)
    def __eq__(self, other):
        return self.dim == other.dim \
            and self.vertices == other.vertices
    def __repr__(self):
        return 'Element: '+repr(self.dim)+'D: '+repr(self.vertices)

class Test(object):
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometryType]
    def test_interface(self, bc):
        if self.verbose:
            print '#### testing interface'        
        return 1
    def test_surface(self, bc):
        if self.verbose:
            print '#### testing surface'        
        elements = [Element(self.generator.dim,x) for x in bc.interior + bc.exterior if len(x)>0]
        reference = Element(self.generator.dim, range(len(self.reference_element)))
        if not reference.matches(elements):
            if self.verbose:
                print '###### faces do not match reference face:'
                print '######## reference face: ', self.reference_element.type
                print '######## faces: ', elements
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
