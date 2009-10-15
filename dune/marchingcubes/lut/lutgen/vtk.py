from lutgen.output import Output

from lutgen.referenceelements import GeometryType
from lutgen.referenceelements import ReferenceElements

from pyvtk import *

class Vtk(Output):
	def __init__(self, lg):
		self.lg = lg
		
	def write_case(self, case, triang, dim, element, fname):
		def vertex(v, points):
			if type(v) is int:
				return points[v] + [0]*(3-dim) # vtk assumes dim=3
			else:
				try:
					return [ (1.0*points[v[0]][i] + points[v[1]][i]) / 2.0
							 for i in range(dim) ] + [0]*(3-dim) # vtk assumes dim=3
				except KeyError:
					return [ 0.5 for i in range(dim) ] + [0]*(3-dim)

		if dim == 3:
			renumber = [ None, None, None, None,
						 ("simplex", range(4)),
						 ("pyramid", range(5)),
						 ("prism", [0,2,1,3,5,4]),
						 None,
						 ("cube", [0,1,3,2,4,5,7,6])]
		elif dim == 2:
			renumber = [ None, None, None,
						 ("triangle", range(3)),
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
		counter = 0
		# create elements
		for cell in triang.cells:
			if len(cell) == 0:
				continue
			offset = len(points)
			cellType = renumber[len(cell)][0]
			mapping = renumber[len(cell)][1]
			coords = [ vertex(cell[mapping[i]],element) for i in range(len(cell)) ]
			elements[cellType].append([i+offset for i in range(len(cell))])
			points += coords
			data += [ counter for i in range(len(cell))]
			counter += 1
		# avoid empty files
		if len(points) == 0:
			points.append([0,0,0])
			data.append(0)
		# write vtk file
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
