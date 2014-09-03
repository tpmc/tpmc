from referenceelements import ReferenceElements
from geomobj import CenterPoint, FacePoint, RootPoint

class NotImplementedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def calcWeight(vertex):
    if type(vertex) is FacePoint:
        return 1
    if type(vertex) is tuple:
        return 1
    else:
        return 1

def cmean(coords, weights):
    sw = 1.0/float(sum(weights))
    return [float(sum(weights[i]*l[i]*sw for i in xrange(len(l)))) for l in zip(*coords)]

# assuming row-wise storage
def det(m):
    if len(m) == 3:
        return m[0][0]*m[1][1]*m[2][2]+m[0][1]*m[1][2]*m[2][0]+m[0][2]*m[1][0]*m[2][1]-m[0][0]*m[1][2]*m[2][1]-m[0][1]*m[1][0]*m[2][2]-m[0][2]*m[1][1]*m[2][0]
    elif len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    raise NotImplementedException("det not implemented for {} rows".format(len(m)))

def jacobi(gt, coords):
    if gt == (3,"simplex") or gt == (3,"prism"):
        return [[coords[k][i]-coords[0][i] for k in (1,2,3)] for i in range(3)]
    if gt == (3,"cube") or gt == (3,"pyramid"):
        return [[coords[k][i]-coords[0][i] for k in (1,2,4)] for i in range(3)]
    if gt == (2,"simplex") or gt == (2,"cube"):
        return [[coords[k][i]-coords[0][i] for k in (1,2)] for i in range(2)]
    raise NotImplementedException("jacobi not implemented for gt {}".format(gt))

def elementType(dim, vertexCount):
    if dim == 3:
        if vertexCount == 4:
            return (dim, "simplex")
        if vertexCount == 5:
            return (dim, "pyramid")
        if vertexCount == 6:
            return (dim, "prism")
        if vertexCount == 8:
            return (dim, "cube")
    if dim == 2:
        if vertexCount == 3:
            return (dim, "simplex")
        if vertexCount == 4:
            return (dim, "cube")
    raise NotImplementedException("elementType not implemented for dim={} and vertexCount={}".format(dim,vertexCount))

def calculateCoordinate(vertex, geometrytype):
    ref = ReferenceElements[geometrytype];
    if type(vertex) is CenterPoint:
        return cmean([calculateCoordinate(i, geometrytype) for i in range(len(ref))], [1]*len(ref))
    if type(vertex) is FacePoint:
        return cmean([calculateCoordinate(i, geometrytype) for i in ref.faces[vertex.id]], [1]*len(ref.faces[vertex.id]))
    if type(vertex) is tuple:
        return cmean([calculateCoordinate(x, geometrytype) for x in vertex], [calcWeight(i) for i in vertex])
    if type(vertex) is int:
        return ref[vertex]

def elementCoordinates(element, geometrytype):
    return [calculateCoordinate(x, geometrytype) for x in element]

def flipped(gt, element):
    if gt[0] < 2:
        return False
    coords = elementCoordinates(element,gt)
    jac = jacobi(elementType(gt[0], len(element)), coords)
    jacdet = det(jac)
    #if abs(jacdet) < 1e-10:
    #    print "jacobian determinant zero ({}) for gt {}, elements: {} --> coords: {}, jacobian: {}".format(jacdet,gt, element, coords,jac)
    return jacdet < 0

def flip(globalgt, element):
    if not flipped(globalgt, element):
        return element
    gt = elementType(globalgt[0], len(element))
    assert(not gt[1] == "pyramid")
    if globalgt[0] == 3:
        if gt[1] == "simplex":
            t = list(element)
            t[0],t[1] = t[1], t[0]
            return t
        if gt[1] == "cube":
            return element[4:]+element[0:4]
        if gt[1] == "prism":
            return element[3:]+element[0:3]
    if globalgt[0] == 2:
        if gt[1] == "cube":
            return element[2:]+element[0:2]
    return element
