from .output import Output

from .referenceelements import GeometryType
from .referenceelements import ReferenceElements
from .geomobj import CenterPoint, FacePoint, RootPoint

from pyvtk import *

class Vtk(Output):
        def __init__(self, lg):
                self.lg = lg
        def write_cells(self, cells, groups, dim, element, fname):
                def vertex(v, points):
                        if type(v) is int:
                                return points[v] + [0]*(3-dim) # vtk assumes dim=3
                        if type(v) is CenterPoint:
                                return [0.5 for i in range(dim) ] + [0]*(3-dim)
                        if type(v) is FacePoint:
                                assert(dim == 3)
                                if len(points) == 8:
                                    facecenters = [[0,.5,.5],[1,.5,.5],[.5,0,.5],
                                                   [.5,1,.5],[.5,.5,0],[.5,.5,1]]
                                elif len(points) == 6:
                                    facecenters = [[.5,0,.5],[0,.5,.5],[.5,.5,.5],
                                                   [1./3.,1./3.,0],[1./3.,1./3.,1]]
                                else:
                                    assert(False)
                                return facecenters[v.id]
                        if type(v) is RootPoint:
                                assert(dim == 3)
                                if len(points) == 8:
                                    roots = [[0.15,.5,.5],[0.85,.5,.5],[.5,0.15,.5],
                                             [.5,0.85,.5],[.5,.5,0.15],[.5,.5,0.85]]
                                elif len(points) == 6:
                                    roots = [[.5,0.15,.5],[0.15,.5,.5],[.5-.15/sqrt(3.),.5-.15/sqrt(3.),.5-.15/sqrt(3.)],
                                             [1./3.,1./3.,0.15],[1./3.,1./3.,0.85]]
                                else:
                                    assert(False)
                                return roots[v.id]
                        else:
                                w = 0.5
                                p1 = vertex(v[0],points)
                                p2 = vertex(v[1],points)
                                # different weighting for face points (just solving display issues
                                if type(v[0]) is FacePoint:
                                        w = 0.85
                                if type(v[1]) is FacePoint:
                                        w = 0.15
                                return [w*p1[i]+(1-w)*p2[i] for i in range(len(p1))]

                if dim == 3:
                        renumber = [ None, None, None, None,
                                                 ("simplex", list(range(4))),
                                                 ("pyramid", [0, 1, 3, 2, 4]),
                                                 ("prism", [0,2,1,3,5,4]),
                                                 None,
                                                 ("cube", [0,1,3,2,4,5,7,6])]
                elif dim == 2:
                        renumber = [ None, None, None,
                                                 ("triangle", list(range(3))),
                                                 ("quad", [0,2,3,1])]
                else:
                        assert 0
                elements = { "simplex" :[],
                                         "pyramid" :[],
                                         "prism"   :[],
                                         "cube"    :[],
                                         "triangle":[],
                                         "quad"    :[]}
                points = []
                data = []
                grps = []
                counter = 0
                # create elements
                for k in range(len(cells)):
                        cell = cells[k]
                        if len(cell) == 0:
                                continue
                        offset = len(points)
                        cellType = renumber[len(cell)][0]
                        mapping = renumber[len(cell)][1]
                        coords = [ vertex(cell[mapping[i]],element) for i in range(len(cell)) ]
                        elements[cellType].append([i+offset for i in range(len(cell))])
                        points += coords
                        data += [ counter for i in range(len(cell))]
                        grps += [ groups[k] for i in range(len(cell))]
                        counter += 1
                # avoid empty files
                if len(points) == 0:
                        points.append([0,0,0])
                        data.append(0)
                        grps.append(0)
                # write vtk file
                # to avoid warnings for empty celldata:
                if len(groups)>0:
                        vtk = VtkData(
                                UnstructuredGrid(points,
                                                 hexahedron=elements["cube"],
                                                 tetra=elements["simplex"],
                                                 wedge=elements["prism"],
                                                 pyramid=elements["pyramid"],
                                                 quad=elements["quad"],
                                                 triangle=elements["triangle"]
                                                 ),
                                PointData(Scalars(data, "ElementID", 'default'), Scalars(grps, "groupID", 'default')),
                                fname
                                )
                else:
                        vtk = VtkData(
                                UnstructuredGrid(points,
                                                 hexahedron=elements["cube"],
                                                 tetra=elements["simplex"],
                                                 wedge=elements["prism"],
                                                 pyramid=elements["pyramid"],
                                                 quad=elements["quad"],
                                                 triangle=elements["triangle"]
                                                 ),
                                PointData(Scalars(data, "ElementID", 'default')),
                                fname
                                )
                vtk.tofile(fname)
        def write_case(self, case, triang, dim, element, fname):                
                self.write_cells(triang.interior, triang.interior_groups, dim, element, fname+'_interior');     
                self.write_cells(triang.exterior, triang.exterior_groups, dim, element, fname+'_exterior');
