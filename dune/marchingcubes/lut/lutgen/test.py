"""
Containing a test-class to perform tests on a marching cubes 33 base
case triangulation. Currently four test are performed. For more
information see documentation pdf in the doc/ folder
"""

from base_case_triangulation import LookupGenerators
from disambiguate import TestFace, TestRegular
from polygon import PolygonList
from geomobj import GeomObject

class Test(object):
    """ class for testing a marching-cubes 33 triangulation """
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
    def find_test_results(self, base_case, mc33_index):
        """ returns the result for the face-test for mc33-case mc33_index """
        reference = self.generator.ref_elem
        result = [-1]*(len(reference.faces)+1)
        if mc33_index < 0 or not base_case.tests:
            return result
        heap = base_case.tests
        heap_index = heap.index(mc33_index)
        # move through the heap and note the test-results
        while heap_index > 0:
            parent = ((heap_index+1) >> 1) - 1
            test_result = heap_index & 1
            if type(heap[parent]) is TestFace:
                result[heap[parent].idx] = test_result
            heap_index = parent
        return result
    def test_consistency(self, triangulation, case_number, test_results):
        """
        check if the decomposition of the reference-faces based on the 
        interior/exterior matches the decomposition in lower dimension
        test_results: face-number-->test-result
        0 equals left, ie outside, 1 equals right, ie inside
        """        
        def rename_vertices(tri, vertices):
            """ rename the vertices in triangulation tri (i --> vertices[i]) """
            renamed = []
            for elem in tri:
                nel = []
                for vertex in elem:
                    if type(vertex) is int:
                        nel.append(vertices[vertex])
                    else:
                        nel.append(tuple(sorted([vertices[vertex[0]], 
                                                 vertices[vertex[1]]])))
                renamed.append(GeomObject(self.generator.dim-1, nel))
            return renamed
        interior_faces = [GeomObject(self.generator.dim-1, x) 
                          for element in triangulation.interior
                          for x 
                          in GeomObject(self.generator.dim, element).faces()]
        exterior_faces = [GeomObject(self.generator.dim-1, x) 
                          for element in triangulation.exterior
                          for x 
                          in GeomObject(self.generator.dim, element).faces()]
        reference_faces = self.generator.ref_elem.faces
        for ref_face in reference_faces:
            ref_face_element = GeomObject(self.generator.dim-1, ref_face)
            # ignore cases where a face of the interface intersects the ref_face
            if sum(1 for x in triangulation.faces 
                   if GeomObject(self.generator.dim-1, x) in ref_face_element) \
                   > 0:
                continue            
            # now get the dim-1 dimensional decomposition of ref_face
            lower_case_number = tuple(case_number[i] for i in ref_face)
            lower_generator = LookupGenerators[ref_face_element.reference.type]
            lower_case = next((case for case in lower_generator.all_cases 
                               if case.case == lower_case_number), None)
            assert(lower_case!=None)
            if len(lower_case.mc33) == 0:
                lower_triangulation = lower_case
            else:
                test_result = test_results[reference_faces.index(ref_face)]
                if test_result < 0:
                    continue
                if type(lower_case.tests[2-test_result]) is TestRegular:
                    lower_triangulation = lower_case
                else:
                    lower_triangulation = \
                        lower_case.mc33[lower_case.tests[2-test_result]]
            face_interior_low = PolygonList([x.polygon() 
                              for x 
                              in rename_vertices(lower_triangulation.interior,
                                                 ref_face)])
            face_exterior_low = PolygonList([x.polygon() 
                              for x 
                              in rename_vertices(lower_triangulation.exterior,
                                                 ref_face)])
            # retrieve the decomposition of ref_face based on triangulation
            face_interior_high = PolygonList([x.polygon() 
                                                 for x in interior_faces 
                                                 if x in ref_face_element])
            face_exterior_high = PolygonList([x.polygon() 
                                                 for x in exterior_faces 
                                                 if x in ref_face_element])
            # compare higher dimensional decomposition with 
            # lower dimensional one
            if not face_interior_low == face_interior_high :
                if self.verbose:
                    print 'error for face %i (%r): interior does not match ' \
                        % (reference_faces.index(ref_face), lower_case_number)\
                        +'lower interior'
                    print '%r vs %r' % (face_interior_high, face_interior_low)
                return 0
            if not face_exterior_low == face_exterior_high:
                if self.verbose:
                    print 'error for face %i (%r): exterior does not match '\
                        % (reference_faces.index(ref_face), lower_case_number)\
                        +'lower exterior'
                    print '%r vs %r' % (face_exterior_high, face_exterior_low)
                return 0
        # all reference faces passed
        return 1
    def test_interface(self, triangulation):
        """
        check if the interface between interior and exterior matches the 
        faces of the base case
        """
        def get_faces(reference, elements):
            """ 
            return surface-faces of elements not intersecting a face of
            the reference element
            """
            faces = [GeomObject(element.dim-1, face) 
                     for element in elements for face in element.faces()]
            faces = [x for x in faces if faces.count(x) != 2]
            for ref_face in (GeomObject(reference.dim-1, x) 
                             for x in reference.faces()):
                faces = [x for x in faces if x not in ref_face]
            return faces
        def compare(first, second):
            """ returns true if first and second contain the same elements """
            return len(first) == len(second) \
                and sum(1 for x in first if x in second) == len(first)
        interface_base = [GeomObject(self.generator.dim-1, x) 
                          for x in triangulation.faces if len(x)>0]
        # remove those faces from interface_base intersecting reference element
        reference = GeomObject(self.generator.dim, 
                            range(len(self.generator.ref_elem)))
        for ref_face in (GeomObject(reference.dim-1, x) 
                         for x in reference.faces()):
            interface_base = [x for x in interface_base if x not in ref_face]
        for data in (triangulation.interior, triangulation.exterior):
            elements = (GeomObject(self.generator.dim, x) 
                        for x in data if len(x)>0)
            interface = get_faces(reference, elements)
            if not compare(interface, interface_base):
                if self.verbose:
                    print 'interface: %r, base.faces: %r' \
                        % (interface, interface_base)
                    if data == triangulation.interior:
                        print '## interface of interior does not match ', \
                            'triangulation interface'
                    else:
                        print '## interface of exterior does not match ', \
                            'triangulation interface'
                return False
        return True
    def test_surface(self, triangulation):
        """
        compare the surface of the union of interior and exterior with the 
        surface of the reference element    
        """
        elements = [GeomObject(self.generator.dim, x) 
                    for x in triangulation.interior + triangulation.exterior 
                    if len(x)>0]
        reference = GeomObject(self.generator.dim, 
                            range(len(self.generator.ref_elem)))
        if not reference.matches(elements, self.verbose):
            if self.verbose:
                print '#### elements do not match reference element:'
                print '#### reference : ', self.generator.ref_elem.type
                print '#### elements: ', elements
            return 0
        return 1
    def test_vertices(self, triang, case):
        """
        checks if all vertices of the reference-faces are in the right
        triangulation, i.e. if case[i] == 0 i should be in interior,
        otherwise in exterior
        """
        for i in range(len(case)):
            if case[i]:
                inside = triang.exterior
            else:
                inside = triang.interior
            if sum(1 for x in inside if i in x) == 0:
                if self.verbose:
                    print '#### error: vertex %i should be %r' \
                        % (i, ['inside','outside'][case[i]])
                return 0
        return 1
    def test_triangulation(self, triang, base_case, mc33_index):
        """ performs tests on the triangulation triang belonging to case """
        count, passed = 0, 0
        count += 1
        result = self.test_vertices(triang, base_case.case)
        if self.verbose and result == 0:
            print '###### vertex test for triangulation ' \
                , triang.name, ' (', base_case.case, ') FAILED'
        passed += result
        count += 1
        result = self.test_interface(triang)
        if self.verbose and result == 0:
            print '###### interface test for triangulation ' \
                , triang.name, 'FAILED'
        passed += result
        count += 1
        result = self.test_surface(triang)
        if self.verbose and result == 0:
            print '###### surface test for triangulation ' \
                , triang.name, 'FAILED'
        passed += result
        if self.generator.dim == 3:
            count += 1
            test_results = self.find_test_results(base_case, mc33_index)
            result = self.test_consistency(triang, base_case.case, test_results)
            if self.verbose and result == 0:
                print '###### consistency test for triangulation ', \
                    triang.name, 'FAILED'
            passed += result
        return (count, passed)
    def test(self):
        """ 
        performs tests for all base-case triangulations, including
        mc33 cases 
        """
        if self.verbose:
            print '# starting test of ', self.generator.geometry_type
        passed = 0
        count = 0
        for base_case in self.generator.base_cases:
            (test_count, test_passed) = \
                self.test_triangulation(base_case, base_case, -1)
            count += test_count
            passed += test_passed
            for i in range(len(base_case.mc33)):
                mc_case = base_case.mc33[i]
                (test_count, test_passed) = \
                    self.test_triangulation(mc_case, base_case, i)
                count += test_count
                passed += test_passed
        if self.verbose:
            print '# ', passed, ' of ', count, ' tests passed'
        return passed == count
