"""
contains class GeomObject representing a geometric Object, eg a 3d cube
and a method for applying a permutation to the vertices of such an object
"""

import logging

from permutation import Permutation
from transformation import Transformation
from referenceelements import ReferenceElements, GeometryType
from polygon import Polygon
from disambiguate import permute_faceid

LOGGER = logging.getLogger('lutgen.geomobject')

class CenterPoint(object):
    def __repr__(self):
        return "CenterPoint"
    def __eq__(self, other):
        return type(other) is CenterPoint
    def __hash__(self):
        return hash("CenterPoint")

class FacePoint(object):
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return "FacePoint{0}".format(self.id)
    def __cmp__(self, other):
        if type(other) is FacePoint:
            return self.id - other.id
        return -1
    def __hash__(self):
        return hash("FacePoint{0}".format(self.id))

class GeomObject(object):
    """ class representing a geometric object, eg a 3d cube, 2d simplex, etc """
    def __init__(self, dim, vertices):
        self.dim = dim
        self.vertices = vertices
        self.reference = ReferenceElements[GeometryType.type(dim, vertices)]
    def get_flip(self):
        dim = self.dim
        count = len(self.vertices)
        if (dim, count) == (1, 2):
            return Permutation(1, (0, 1))
        if (dim, count) == (2, 3):
            return Permutation(-1, (2, 1, 0))
        if (dim, count) == (2, 4):
            return Permutation(-1, (1, 0, 3, 2))
        if (dim, count) == (3, 4):
            return Permutation(-1, (3, 0, 2, 1))
        if (dim, count) == (3, 5):
            return Permutation(-1, (1, 0, 3, 2, 4))
        if (dim, count) == (3, 6):
            return Permutation(-1, (3, 4, 5, 0, 1, 2))
        if (dim, count) == (3, 8):
            return Permutation(-1, (4, 5, 6, 7, 0, 1, 2, 3))
        print "error: unkown geom obj %id, %i vertices" % (dim, count)
        assert 0
    def faces(self):
        """
        returns a list of the faces of this element as defined by the 
        faces of the reference element
        """
        return [[self.vertices[i] for i in face] 
                for face in self.reference.faces]
    def matches(self, subelements):
        """
        check if the union of the subelements matches this element
        """
        if self.dim == 0:
            return subelements == [self]
        # merge all faces of all subelements
        faces = [GeomObject(element.dim-1, face) 
                 for element in subelements for face in element.faces()]
        # retrieve faces which only occur onces
        surface = [x for x in faces if faces.count(x) == 1]
        # check if every face of self can be matched by the surface-faces 
        #intersecting it
        for (i,reference_face) in [(i,GeomObject(self.dim-1, face))
                                   for (i,face) in enumerate(self.faces())]:
            intersecting_faces = [face for face in surface
                                  if reference_face.containsIfFace(i,face)]
            surface = [face for face in surface
                       if face not in intersecting_faces]
            if not reference_face.matches(intersecting_faces):
                LOGGER.error('{0} is not matched by '
                             '{1}'.format(reference_face, 
                                          intersecting_faces))
                return False
        # if there are faces in the surface which could used to match 
        # a reference face, the subelements don't match
        if len(surface)>0:
            LOGGER.error('following faces could not be matched '
                         'with {0}:'.format(self))
            LOGGER.error(surface)
            return False
        return True
    def polygon(self):
        """ returns a Polygon from the Elements vertices """
        assert(self.dim<=2)
        if self.reference.type == (2,'cube'):
            return Polygon(self.vertices[i] for i in [0, 1, 3, 2])
        return Polygon(self.vertices)
    def containsIfFace(self, faceid, other):
        # returns true if all vertices of other are inside this face,
        # if this face has the given faceid
        def contv(vertex):
            if (vertex in self.vertices
                or (type(vertex) is FacePoint
                    and vertex.id == faceid)):
                return 1
            if (type(vertex) is tuple
                and contv(vertex[0])
                and contv(vertex[1])):
                return 1
            return 0
        # check if all vertices of other are inside self
        # number of intersecting points
        intcount = sum(contv(x) for x in other.vertices)
        return intcount == len(other.vertices)
    def __mul__ (self, perm):
        assert type(perm) is Permutation or type(perm) is Transformation
        def apply_perm(vertex):
            """ permutates vertex """
            if type(vertex) is int:
                return perm[vertex]
            if type(vertex) is CenterPoint:
                return vertex
            if type(vertex) is FacePoint:
                cubereffaces = ReferenceElements[(3, "cube")].faces
                return FacePoint(permute_faceid(vertex.id, perm, cubereffaces))
            l = [apply_perm(vertex[0]), apply_perm(vertex[1])];
            if type(vertex[0]) is tuple or type(vertex[1]) is tuple:
                return tuple(l)
            return tuple(sorted(l))
        entity = self.vertices
        if len(self.vertices) == 0:
            return []
        if perm.orientation == -1:
            entity = self.get_flip() * entity
        return [apply_perm(vertex) for vertex in entity]
    def __contains__(self, other):
        def contv(vertex):
            if vertex in self.vertices:
                return 1
            if (type(vertex) is tuple
                and contv(vertex[0])
                and contv(vertex[1])):
                return 1
            return 0
        # check if all vertices of other are inside self
        # number of intersecting points
        intcount = sum(contv(x) for x in other.vertices)
        return intcount == len(other.vertices)
    def __eq__(self, other):
        """ elements are equal if they contain the same vertices """
        #print "eq: {0} vs {1}: {2}".format(set(self.vertices), set(other.vertices),(self.dim == other.dim
        #                                                and set(self.vertices) == set(other.vertices)))
        return (self.dim == other.dim
                and sorted(self.vertices) == sorted(other.vertices))
    def __repr__(self):
        return 'GeomObject: {0}: {1}'.format(self.reference.type, self.vertices)

def permute_geom_list(dim, entities, perm):
    """
    applies the permutation perm to all entities. returns a list of entities,
    ie a list of lists of vertices
    """
    return [ GeomObject(dim, e) * perm for e in entities ]


Center = CenterPoint()
Face0 = FacePoint(0)
Face1 = FacePoint(1)
Face2 = FacePoint(2)
Face3 = FacePoint(3)
Face4 = FacePoint(4)
Face5 = FacePoint(5)
