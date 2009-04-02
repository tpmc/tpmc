class GeometryType(tuple):
	def __new__(cls, d, t=None):
		if t is None:
			t=d[1]
			d=d[0]
		if not type(d) is int:
			raise TypeError, "first parameter for GeometryType(dim,basicType) is not int"
		if not type(t) is str:
			raise TypeError, "second parameter for GeometryType(dim,basicType) is not str"
		return tuple.__new__(cls, (d,t))
	def __init__(self, d, t=None):
		pass
	def dim(self):
		return self[0]
	def basicType(self):
		return self[1]
	def Type(dim, vertizes):
		if type(vertizes) is int:
			v = vertizes
		else:
			v = len(vertizes)
		t = None
		if dim == 0:
			assert v == 1
			t = (dim,"any")
		elif dim == 1:
			assert v == 2
			t = (dim,"any")
		elif dim == 2:
			t = [None, None, None,
				 "simplex", "cube"][v]
		elif dim == 3:
			t = [None, None, None, None,
				 "simplex", "pyramid",
				 "prism", None, "cube"][v]
		assert t is not None
		return GeometryType(dim,t)
	type = staticmethod(Type)

class ReferenceElement(list):
	def __new__ (cls, t, c, f, e):
		return list.__new__(cls, t, c, f, e)
	def __init__(self, type, coords, faces, edges):
		list.__init__(self, coords)
		self.type = GeometryType(type)
		self.faces = faces
		self.edges = [ set(x) for x in edges ]

ReferenceElements = {(0,"any"): ReferenceElement((0,"any"), [[]], [], []),
					 (1,"any"):
					 ReferenceElement((1,"any"),
									  [[0],[1]],
									  [[0],[1]],
									  [[0,1]]),
					 (2,"simplex"):
					 ReferenceElement((2,"simplex"),
									  [[0,0],[1,0],[0,1]],
									  [[2,1],[0,2],[1,0]],
									  [[2,1],[0,2],[1,0]]),
					 (2,"cube")   :
					 ReferenceElement((2,"cube"),
									  [[0,0],[1,0],[0,1],[1,1]],
									  [[0,2],[3,1],[1,0],[2,3]],
									  [[0,2],[3,1],[1,0],[2,3]]),
					 (3,"simplex"):
					 ReferenceElement((3,"simplex"),
									  [[0,0,0],[1,0,0],[0,1,0],[0,0,1]],
									  [[2,1,3],[0,2,3],[1,0,3],[0,1,2]],
									  [[0,1],[1,2],[0,2],[0,3],[1,3],[2,3]]),
					 (3,"pyramid"):
					 ReferenceElement((3,"pyramid"),
									  [[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1]],
									  [[0,1,3,2],[2,1,4],[3,2,4],[0,3,4]],
									  [[0,1],[1,2],[2,3],[3,0],
									   [0,4],[1,4],[2,4],[3,4]]),
					 (3,"prism")  :
					 ReferenceElement((3,"prism"),
									  [[0,0,0],[1,0,0],[0,1,0],
									   [0,0,1],[1,0,1],[0,1,1]],
									  [[0,1,2],[1,0,4,3],[2,1,5,4],
									   [0,2,3,5],[4,3,5]],
									  [[0,1],[1,2],[2,0],[0,3],[1,4],[2,5],
									   [3,4],[4,5],[5,3]]),
					 (3,"cube")   :
					 ReferenceElement((3,"cube"),
									  [[0,0,0],[1,0,0],[0,1,0],[1,1,0],
									   [0,0,1],[1,0,1],[0,1,1],[1,1,1]],
									  [[0,2,4,6],[3,1,7,5],[1,0,5,4],
									   [2,3,6,7],[0,1,2,3],[5,4,6,7]],
									  [[0,4],[1,5],[2,6],[3,7],
									   [0,2],[1,3],[4,6],[5,7],
									   [0,1],[2,3],[4,5],[6,7]])}