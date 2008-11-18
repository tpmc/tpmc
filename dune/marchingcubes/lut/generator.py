from pprint import pprint

class Permutation(tuple):
	def __new__ (cls, o, t):
		return tuple.__new__(cls, t)
	def __init__(self, o, t):
		self.orientation = o
		tuple.__init__(self, t)
	def __mul__ (self, other):
		if type(other) is Permutation:
			return Permutation(self.orientation*other.orientation, (other[x] for x in self))
		return type(other)(other[x] for x in self)
	def __repr__ (self):
		return ['?','+','-'][self.orientation] + tuple.__repr__(self)

class Case(object):
	def __init__(self,x):
		self.case = x
		self.permutation = None
		self.base_case = None
		self.faces = [[]]
		self.cells = [[]]
	def __repr__(self):
		return "%s, %s, %s, %s" % (repr(self.case), repr(self.permutation),
								   repr(self.faces), repr(self.cells))
		
class BaseCase(object):
	def __init__(self, dim, x):
		self.dim = dim
		self.case = x
		self.faces = [[]]
		self.cells = [[]]
	def __repr__(self):
		return "%s, %s, %s" % (repr(self.case), repr(self.faces),
							   repr(self.cells))
	def __eq__(self, other):
		return self.case == other.case
 	def get_flip(self, dim, len):
		if (dim, len) == (1, 2):
			return Permutation(1, (0,1))
		if (dim, len) == (2, 3):
			return Permutation(-1, (2,1,0))
		if (dim, len) == (2, 4):
			return Permutation(-1, (1,0,3,2))
		if (dim, len) == (3, 4):
			return Permutation(-1, (3,0,2,1))
		if (dim, len) == (3, 5):
			return Permutation(-1, (1,0,3,2,4))
		if (dim, len) == (3, 6):
			return Permutation(-1, (3,4,5,0,1,2))
		if (dim, len) == (3, 8):
			return Permutation(-1, (4,5,6,7,0,1,2,3))
		assert 0
	def permute_entity(self,entity,p,dim):
		def f(x):
			if type(x) is int:
				return p[x]
			return (p[x[0]], p[x[1]])
		def flip(e):
			p2 = self.get_flip(dim, len(e))
			return p2*e
		if len(entity) == 0:
			return []
		if p.orientation == 1:
			return [ f(vertex) for vertex in  entity ]
		else:
			return [ f(vertex) for vertex in flip(entity) ]
	def permute_faces(self,p):
		return [ self.permute_entity(face,p,self.dim-1)
				 for face in self.faces ]
	def permute_cells(self,p):
		return [ self.permute_entity(cell,p,self.dim)
				 for cell in self.cells ]

class LookupGenerator(object):
	def __init__(self, dim, basicType, verbose=False):
		self.dim = dim
		self.basicType = basicType
		self.geometryType = (dim,basicType)
		self.p_size = self.get_p_size()
		if verbose:
			print "dim = %i\np_size = %i\ng_size = \n" \
				  % (self.dim, self.p_size)

		# Generate Permutation Group from generators
		P = self.get_generators()
		self.G = set([Permutation(1,range(self.p_size))])
		i = 0
		g_size = 0
		while len(self.G) != g_size:
			g_size = len(self.G)
			H = set()
			for g in self.G:
				for p in P:
					H.add(p*g)
			self.G = self.G.union(H)
			i+=1
		if verbose:
			print "g_size:",g_size
			print "wortlaenge:",i-1

		# Generate list of base cases
		# and save base case and permutation for each case
		self.all_cases = [Case(tuple((i >> x) & 1 for x in range(self.p_size)))
						  for i in range(1<<self.p_size)]
		self.base_cases = []

		for entry in self.all_cases:
			found = False
			for g in self.G:
				bc = BaseCase(dim, g*entry.case)
				if bc in self.base_cases:
					found = True
					entry.permutation = g
					entry.base_case = self.base_cases[self.base_cases.index(bc)]
					break
			if not found:
				self.base_cases.append(BaseCase(dim, entry.case))
				entry.permutation = Permutation(1,range(self.p_size))
				entry.base_case = self.base_cases[-1]

	def get_p_size(self):
		if self.dim == 0:
			return 1
		elif self.dim == 1:
			return 2
		elif self.basicType == "cube":
			return 1<<self.dim
		elif self.basicType == "simplex":
			return self.dim + 1
		elif self.basicType == "prism":
			return 6
		elif self.basicType == "pyramid":
			return 5
		assert 0

	def get_generators(self):
		if self.dim == 0:
			return []
		elif self.dim == 1:
			return [Permutation(1, (1,0))]
		elif self.geometryType == (2,"simplex"):
			return [Permutation(1, (1,2,0))]
		elif self.geometryType == (2,"cube"):
			# this is the old version causing flipped normal vectors
##			return [Permutation(1, (1,3,0,2)),
##					Permutation(-1, (1,0,3,2))]
			return [Permutation(1, (1,3,0,2))]
		elif self.geometryType == (3,"simplex"):
			return [Permutation(1, (3,1,0,2)),
					Permutation(1, (3,0,2,1))]
		elif self.geometryType == (3,"cube"):
			return [Permutation(-1, (4,5,6,7,0,1,2,3)),
					Permutation(1, (1,5,3,7,0,4,2,6)),
					Permutation(1, (1,3,0,2,5,7,4,6))]
		elif self.geometryType == (3,"prism"):
			assert 0
		elif self.geometryType == (3,"pyramid"):
			assert 0
		elif self.geometryType == (4,"cube"):
			return [Permutation(-1, (8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7)),
					Permutation(1, (2,3,6,7,10,11,14,15,0,1,4,5,8,9,12,13)),
					Permutation(1, (1,5,3,7,9,13,11,15,0,4,2,6,8,12,10,14)),
					Permutation(1, (1,3,9,11,5,7,13,15,0,2,8,10,4,6,12,14))]
		assert 0

	def generate(self):
		# Generate lookup entries from base cases
		for entry in self.all_cases:
			entry.faces = entry.base_case.permute_faces(entry.permutation)
			entry.cells = entry.base_case.permute_cells(entry.permutation)

	def print_base(self, foo="lut", f=0, c=0):
		print "# base cases %s %iD:" % (self.basicType, self.dim)
		i = 0
		for entry in self.base_cases:
			e = list(entry.case)
			e.reverse()
			print "# " + ",".join(map(str,entry.case)) + " -> " + "".join(map(str,e))
			while len(entry.faces) < f:
				entry.faces.append([])
			print foo + ".base_cases[%i].faces = " % i + repr(entry.faces)
			while len(entry.cells) < c:
				entry.cells.append([])
			print foo + ".base_cases[%i].cells = " % i + repr(entry.cells)
			i += 1
		print

	def print_info(self):
		l = list(self.G)
		l.sort()
		print len(self.G)
		pprint(l)

		print len(self.base_cases)
		pprint(self.base_cases)

		print len(self.all_cases)
		pprint(self.all_cases)

#class GeneratorContainer(dict):
