"""
Containing a test-class to perform tests on a marching cubes 33 base
case triangulation. Currently four test are performed. For more
information see documentation pdf in the doc/ folder
"""
import logging
from base_case_triangulation import LookupGenerators
from disambiguate import TestFace, TestRegular
from polygon import PolygonList
from geomobj import GeomObject, CenterPoint, FacePoint

LOGGER = logging.getLogger('lutgen.test')

class SingleTest(object):
    def __init__(self, name = ""):
        self.success = False
        self.done = False
        self.name = name
    def succeed(self):
        self.done = True
        self.success = True
    def fail(self):
        self.done = True
        self.success = False

class SingleTriangulationTest(SingleTest):
    def __init__(self, dimension, triangulation, name = ""):
        SingleTest.__init__(self, name)
        self.triangulation = triangulation
        self.dimension = dimension

class SinglePyramidTest(SingleTriangulationTest):
    def __init__(self, dimension, triangulation, name = ""):
        SingleTriangulationTest.__init__(dimension, triangulation, name)
    def run(self):
        def test_tri(tri):
            if (self.dimension == 3) and (len([1 for element in tri if len(element) == 5]) > 0) :
                self.fail()
        test_tri(self.triangulation.interior)
        if not self.done:
            test_tri(self.triangulation.exterior)
        if not self.done:
            self.succeed()


class Test(object):
    """ class for testing a marching-cubes 33 triangulation """
    def __init__(self, generator):
        self.generator = generator
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
            for elem in tri:
                nel = []
                for vertex in elem:
                    if type(vertex) is int:
                        nel.append(vertices[vertex])
                    else:
                        nel.append(tuple(sorted([vertices[vertex[0]], 
                                                 vertices[vertex[1]]])))
                yield GeomObject(self.generator.dim-1, nel)
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
                   if GeomObject(self.generator.dim-1, x) 
                   in ref_face_element) > 0:
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
            errormsg = 'face {0} ({1}) {2} does not match'
            if not face_interior_low == face_interior_high :
                LOGGER.error(errormsg.format(reference_faces.index(ref_face),
                                             lower_case_number,
                                             'interior'))
                LOGGER.error('high:{0} vs low:{1}'.format(face_interior_high, 
                                                 face_interior_low))
                return 0
            if not face_exterior_low == face_exterior_high:
                LOGGER.error(errormsg.format(reference_faces.index(ref_face),
                                             lower_case_number,
                                             'exterior'))
                LOGGER.error('high:{0} vs low:{1}'.format(face_interior_high, 
                                                 face_interior_low))
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
            return len(first) == len(second) and sum(1 for x in first 
                                                     if x 
                                                     not in second) == 0
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
                LOGGER.error("interface: {0}\n"
                             "base.faces: {1}".format(interface, 
                                                      interface_base))
                errormsg = "interface of {0} does not match"
                if data == triangulation.interior:
                    LOGGER.error(errormsg.format('interior'))
                else:
                    LOGGER.error(errormsg.format('exterior'))
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
        if not reference.matches(elements):
            LOGGER.error("elements do not match reference element:"
                         "reference : {0}"
                         "elements: {1}".format(self.generator.ref_elem.type,
                                                elements))
            return 0
        return 1
    def test_vertex_groups(self, triang, case):
        for i in range(len(case)):
            vg = triang.vertex_groups[i]
            interior_elements = [triang.interior_groups[e] for e in range(len(triang.interior)) if i in triang.interior[e]]
            exterior_elements = [triang.exterior_groups[e] for e in range(len(triang.exterior)) if i in triang.exterior[e]]
            if len([e for e in interior_elements if e != vg])>0 or len([e for e in exterior_elements if e != vg])>0:
                return 0
        return 1
    def test_vertices(self, triang, case):
        """
        checks if all vertices of the reference-faces are in the right
        triangulation, i.e. if case[i] == 0 i should be in interior,
        otherwise in exterior
        """
        for (index, value) in enumerate(case) :
            if value:
                inside = triang.exterior
            else:
                inside = triang.interior
            if sum(1 for x in inside if index in x) == 0:
                LOGGER.error("vertex {0} should be "
                             "{1}".format(index, ['inside','outside'][value]))
                return 0
        return 1
    def test_face_tests(self, case, test_table, ref_elem):
        """
        checks if all faces tested in test_table are ambiguous
        """
        for x in (x for x in test_table if type(x) is TestFace):
            face_values = [case[i] for i in ref_elem.faces[x.idx]];
            if face_values != [0, 1, 1, 0] and face_values != [1, 0, 0, 1]:
                LOGGER.error("face {0} should be tested "
                             "but is not ambiguous".format(x.idx))
                return 0
        return 1
    def test_valid_vertices(self, triang, case):
        for x in (x for e in triang.interior+triang.exterior+triang.faces for x in e):
            if type(x) is not int and type(x) is not CenterPoint and type(x) is not FacePoint:
                if type(x[0]) is int and type(x[1]) is int:
                    if case[x[0]] == case[x[1]]:
                        LOGGER.error("vertex on edge {0} does"
                                     " not exist in case {1}".format(x,case))
                        return 0
        return 1
    def test_pyramids(self, triang):
        for e in triang.interior+triang.exterior:
            if len(e) == 5:
                LOGGER.error("evil pyramid found: {0}".format(e))
                return 0
        return 1
    def test_triangulation(self, triang, base_case, mc33_index):
        """ performs tests on the triangulation triang belonging to case """
        count, passed = 0, 0
        count += 1
        result = self.test_vertices(triang, base_case.case)
        if result == 0:
            LOGGER.error("vertex test for triangulation {0} ({1}) "
                         "FAILED".format(triang.name, base_case.case))
        passed += result
        count += 1
        result = self.test_vertex_groups(triang, base_case.case)
        if result == 0:
            LOGGER.error("vertex-groups test for triangulation {0} ({1}) "
                         "FAILED".format(triang.name, base_case.case))
        passed += result
        count += 1
        result = self.test_interface(triang)
        if result == 0:
            LOGGER.error("interface test for triangulation {0} "
                         "FAILED".format(triang.name))
        passed += result
        count += 1
        result = self.test_surface(triang)
        if result == 0:
            LOGGER.error("surface test for triangulation {0} "
                         "FAILED".format(triang.name))
        passed += result
        count += 1
        result = self.test_valid_vertices(triang, base_case.case)
        if result == 0:
            LOGGER.error("valid-vertices test for triangulation {0} "
                         "FAILED".format(triang.name))
        passed += result
        if self.generator.dim == 3:
            count += 1
            test_results = self.find_test_results(base_case, mc33_index)
            result = self.test_consistency(triang, base_case.case, test_results)
            if result == 0:
                LOGGER.error("consistency test for triangulation {0} "
                             "FAILED".format(triang.name))
            passed += result
            count += 1
            result = self.test_pyramids(triang)
            if result == 0:
                LOGGER.error("pyramid test for triangulation {0} , case {1} "
                             "FAILED".format(triang.name, base_case.case))
            passed += result
        return (count, passed)
    def test(self):
        """ 
        performs tests for all base-case triangulations, including
        mc33 cases and for dim=3 all updated cases
        """
        LOGGER.info("starting test of {0}".format(self.generator.geometry_type))
        passed = 0
        count = 0
        for base_case in self.generator.all_cases:
            (test_count, test_passed) = self.test_triangulation(base_case, 
                                                                base_case, -1)
            count += test_count
            passed += test_passed
            for (index, mc_case) in enumerate(base_case.mc33):
                (test_count, test_passed) = self.test_triangulation(mc_case, 
                                                                    base_case, 
                                                                    index)
                count += test_count
                passed += test_passed
        if self.generator.dim == 3:
            for case in self.generator.all_cases:
                result = self.test_face_tests(case.case, case.tests, self.generator.ref_elem)
                if result == 0:
                    LOGGER.error("face test for case {0} "
                                 "FAILED".format(case.case))
                count += 1;
                passed += result;
        LOGGER.info("{0} of {1} tests passed".format(passed, count))
        return passed == count
