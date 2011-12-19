"""
Containing a test-class to perform tests on a marching cubes 33 base
case triangulation. Currently three test are performed. For more
information see documentation pdf in the doc/ folder
"""

from referenceelements import ReferenceElements, GeometryType
from base_case_triangulation import LookupGenerators
from disambiguate import TestFace, TestRegular

class Polygon(list):
    """
    represents a sequence of vertices forming a polygon. All vertices
    are connected to their neighbours, the last and the first vertex
    are connected.
    """
    def __new__(cls, vertices):
        return list.__new__(cls, vertices)
    def reverse(self):
        """ returns a new Polygon in reversed order """
        return Polygon(reversed(self))
    def __lshift__(self, amount):
        return Polygon(self[amount:]+self[:amount])
    def __rshift__(self, amount):
        return self.__lshift__(-amount)
    def connected(self, other):
        """ returns index of the first vertex of a connection to other """
        start = -1
        for i in range(len(self)):
            if self[i] in other \
                    and (self[(i+1) % len(self)] \
                             == other[(other.index(self[i])+1) % len(other)] \
                             or self[(i-1) % len(self)] \
                             == other[(other.index(self[i])-1) % len(other)]):
                start = i
                break
        if start >= 0:
            if start == 0 and not list.__eq__(self, other):
                while self[start-1] in other:
                    start = (start - 1) % len(self)
            #print '%r is connected to %r at %i' % (self, other, start)
            return start
        else:
            return -1
    def merge(self, other):
        """ 
        returns a merged version of this polygon and other at the 
        connection returned by self.connected(other) (or reversed)
        """
        # find start of the merging position
        temp_other = Polygon(other)
        start = self.connected(temp_other)
        # if no connection was found
        if start < 0:
            temp_other = temp_other.reverse()
            start = self.connected(temp_other)
        # are the polygons connected?
        if start >= 0:
            # move start to the end of the list
            merged = list(self << start+1)
            #print 'lists to merge: ',merged, ' and ', temp_other
            start_in_other = temp_other.index(merged[-1])
            # remove inner nodes
            inner_count = 0
            while len(merged)>1 and merged[1] in other:                
                merged.pop(0)
                inner_count += 1
            # get index of one past end of connection in other
            other_index = (start_in_other+inner_count+2) % len(temp_other)
            #print 'start_in_other: %i' % (start_in_other)
            # insert nodes from other to front of merged in reversed order
            while other_index != start_in_other:
                merged.insert(0, temp_other[other_index])
                other_index = (other_index + 1) % len(temp_other)
            #print '%r + %r = %r' % (self, temp_other, merged)
            return Polygon(merged)
        else:
            raise RuntimeError('polygons are not connected')
    def __eq__(self, other):        
        if len(self)!=len(other):
            return False
        srev = self.reverse()
        for offset in range(len(self)):
            if list.__eq__(self >> offset, other) \
                    or list.__eq__(srev >> offset, other):
                return False
        return True
    def __repr__(self):
        return list.__repr__(self)

class Element(object):
    """ represents a geometric element, eg a cube, simplex, ... """
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
        self.reference = ReferenceElements[GeometryType.type(dim, vertices)]
    def faces(self):
        """
        returns a generator for the faces of this element as defined by the 
        faces of the reference element
        """
        return [[self.vertices[i] \
                     for i in face] for face in self.reference.faces]
    def matches(self, subelements, verbose = False):
        """
        check if the union of the subelements matches this element
        """
        if self.dim == 0:
            return subelements == [self]
        # merge all faces of all subelements
        faces = [Element(element.dim-1, face) \
                     for element in subelements for face in element.faces()]
        # retrieve faces which only occur onces
        surface = [x for x in faces if faces.count(x) == 1]
        # check if every face of self can be matched by the surface-faces 
        #intersecting it
        for reference_face in [Element(self.dim-1, face) \
                                   for face in self.faces()]:
            intersecting_faces = [face for face in surface \
                                      if face in reference_face]            
            surface = [face for face in surface \
                           if face not in intersecting_faces]
            if not reference_face.matches(intersecting_faces, verbose):
                if verbose:
                    print '## ', reference_face, ' is not matched by ', \
                        intersecting_faces
                return False
        # if there are faces in the surface which could used to match 
        # a reference face, the subelements don't match
        if len(surface)>0:
            if verbose:
                print '## following faces could no be matched with ', self, ':'
                print '## ', surface
            return False
        return True
    def polygon(self):
        """ returns a Polygon from the Elements vertices """
        assert(self.dim<=2)
        if self.reference.type == (2,'cube'):
            return Polygon(self.vertices[i] for i in [0, 1, 3, 2])
        return Polygon(self.vertices)
    def __contains__(self, other):
        # check if all vertices of other are inside self
        # number of intersecting points
        intcount = sum(1 for x in other.vertices if x in self.vertices)
        # number of points on edges not in self, of which both adjoining 
        # vertices are in self
        lincount = sum(1 for x in other.vertices if type(x) is not int \
                 and x not in self.vertices \
                 and x[0] in self.vertices and x[1] in self.vertices)
        return intcount + lincount == len(other.vertices)
    # elements are equal if they contain the same vertices
    def __eq__(self, other):
        return self.dim == other.dim \
            and set(self.vertices) == set(other.vertices)
    def __repr__(self):
        return 'Element: '+repr(self.reference.type)+': '+repr(self.vertices)



class Test(object):
    """ class for testing a marching-cubes 33 triangulation """
    def __init__(self, generator, verbose = False):
        self.generator = generator
        self.verbose = verbose
        self.reference_element = ReferenceElements[self.generator.geometry_type]
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
    def test_faces(self, triangulation, case_number, test_results):
        """
        check if the decomposition of the reference-faces based on the 
        interior/exterior matches the decomposition in lower dimension
        test_results: face-number-->test-result
        0 equals left, ie outside, 1 equals right, ie inside
        """
        def merge_polygon_list(polygons):
            """ merges the list of polygons as far as possible """
            def remove_inner_nodes(vlist):
                """ 
                removes inner nodes from a list, 
                eg [1, (1,2) ,2] --> [1, 2]
                """
                i = 0
                while i < len(vlist):
                    if type(vlist[i]) is tuple \
                            and vlist[(i-1) % len(vlist)] in vlist[i] \
                            and vlist[(i+1) % len(vlist)] in vlist[i]:
                        vlist.pop(i)
                    else:
                        i += 1
            changed = True
            # simply loop through the list and check if anything can be merged
            # until nothing changes anymore
            while changed:
                changed = False
                for i in range(len(polygons)):                    
                    for j in range(i+1, len(polygons)):
                        if polygons[i].connected(polygons[j])>=0 \
                                or polygons[i].connected(polygons[j].reverse())\
                                >=0 :
                            vlist = list(polygons[i].merge(polygons[j]))
                            remove_inner_nodes(vlist)
                            polygons.append(Polygon(vlist))
                            polygons.pop(j)
                            polygons.pop(i)
                            changed = True
                            break
                    if changed:
                        break
        def equal_polygon_list(first, second):
            """ 
            returns true if first and second list form the same set of 
            polygons 
            """           
            merge_polygon_list(first)
            merge_polygon_list(second)
            first = [set(x) for x in first]
            second = [set(x) for x in second]
            if len(first) == len(second) \
                    and sum(1 for x in first if x in second) == len(first):
                return True
            else:
                return False
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
                renamed.append(Element(self.generator.dim-1, nel))
            return renamed
        reference = Element(self.generator.dim, 
                            range(len(self.reference_element)))
        triang_elements_in = [Element(self.generator.dim, x) 
                              for x in triangulation.interior]
        triang_elements_ex = [Element(self.generator.dim, x) 
                              for x in triangulation.exterior]
        interior_faces = [Element(self.generator.dim-1, x) 
                          for element in triang_elements_in
                          for x in element.faces()]
        exterior_faces = [Element(self.generator.dim-1, x) 
                          for element in triang_elements_ex
                          for x in element.faces()]
        reference_faces = reference.faces()
        for ref_face in reference_faces:
            ref_face_element = Element(reference.dim-1, ref_face)
            # ignore cases where a face of the interface intersects the ref_face
            if sum(1 for x in triangulation.faces 
                   if Element(reference.dim-1, x) in ref_face_element) > 0:
                continue
            # retrieve the decomposition of ref_face based on triangulation
            intersecting_interior = [x.polygon() for x in interior_faces 
                                     if x in ref_face_element]
            intersecting_exterior = [x.polygon() for x in exterior_faces 
                                     if x in ref_face_element]
            # now get the dim-1 dimensional decomposition of ref_face
            lower_case_number = tuple(case_number[i] for i in ref_face)
            #print lower_case_number
            lower_generator = LookupGenerators[ref_face_element.reference.type]
            lower_case = next((case for case in lower_generator.all_cases 
                               if case.case == lower_case_number), None)
            assert(lower_case!=None)
            if len(lower_case.mc33) == 0:
                lower_triangulation = lower_case
            else:
                faceid = reference_faces.index(ref_face)
                test_result = test_results[faceid]
                if test_result < 0:
                    continue
                if type(lower_case.tests[2-test_result]) is TestRegular:
                    lower_triangulation = lower_case
                else:
                    lower_triangulation = \
                        lower_case.mc33[lower_case.tests[2-test_result]]
            lower_interior = [x.polygon() 
                              for x 
                              in rename_vertices(lower_triangulation.interior,
                                                 ref_face)]
            lower_exterior = [x.polygon() 
                              for x 
                              in rename_vertices(lower_triangulation.exterior,
                                                 ref_face)]
            # compare intersecting_in/exterior with lower_in/exterior
            if not equal_polygon_list(lower_interior, intersecting_interior):
                if self.verbose:
                    print 'error for face %i (%r): interior does not match ' \
                        % (reference_faces.index(ref_face), lower_case_number)\
                        +'lower interior'
                    print '%r vs %r' % (intersecting_interior, lower_interior)
                return 0
            if not equal_polygon_list(lower_exterior, intersecting_exterior):
                if self.verbose:
                    print 'error for face %i (%r): exterior does not match '\
                        % (reference_faces.index(ref_face), lower_case_number)\
                        +'lower exterior'
                    print '%r vs %r' % (intersecting_exterior, lower_exterior)
                return 0
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
            faces = [Element(element.dim-1, face) 
                     for element in elements for face in element.faces()]
            faces = [x for x in faces if faces.count(x) != 2]
            for ref_face in (Element(reference.dim-1, x) 
                             for x in reference.faces()):
                faces = [x for x in faces if x not in ref_face]
            return faces
        def compare(first, second):
            """ returns true if first and second contain the same elements """
            return len(first) == len(second) \
                and sum(1 for x in first if x in second) == len(first)
        interface_base = [Element(self.generator.dim-1, x) 
                          for x in triangulation.faces if len(x)>0]
        # remove those faces from interface_base intersecting reference element
        reference = Element(self.generator.dim, 
                            range(len(self.reference_element)))
        for ref_face in (Element(reference.dim-1, x) 
                         for x in reference.faces()):
            interface_base = [x for x in interface_base if x not in ref_face]
        for data in (triangulation.interior, triangulation.exterior):
            elements = (Element(self.generator.dim, x) 
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
        elements = [Element(self.generator.dim, x) 
                    for x in triangulation.interior + triangulation.exterior 
                    if len(x)>0]
        reference = Element(self.generator.dim, 
                            range(len(self.reference_element)))
        if not reference.matches(elements, self.verbose):
            if self.verbose:
                print '#### elements do not match reference element:'
                print '#### reference : ', self.reference_element.type
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
            result = self.test_faces(triang, base_case.case, test_results)
            if self.verbose and result == 0:
                print 'test-results: ', test_results
                print '###### faces test for triangulation ', \
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
            #for i in range(len(base_case.tests)):
            #    print '%i) %r' % (i, base_case.tests[i])
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
