from .generator import Permutation
from .referenceelements import *
from sys import exit

class Consistency(object):
	def __init__(self, generators):
		self.generators = generators
	def check(self, dim, basictype):
		gtype = GeometryType(dim, basictype)
		try:
			self.gtype = gtype
			for case in self.generators[self.gtype].base_cases:
				faceid = 0
				for face in ReferenceElements[gtype].faces:
					self.checkCase(case, face)
					faceid += 1
		except ValueError, e:
			print "Error:\tcase %s %s\n\tface %i\n\t%s" % \
				  (repr(case.case), repr(self.gtype), faceid, str(e))
			exit(0)
	def findMapping(self, a, setb):
		for b in setb:
			if (len(a) != len(b)):
				continue
			# try to find a mapping
			try:
				mapping = [ b.index(v) for v in a ]
				o = 1 # orientation of foo o in (-1,1)
				mapping = Permutation(o, mapping)
				return (mapping, setb.index(b))
			except ValueError:
				continue
		raise ValueError, "can't map face " + repr(a) + \
				  " to any face in " + repr(setb)
	def subFacesFromCells(self, case, face):
		csubfaces = []
		for cell in case.cells:
			if cell == []:
				continue
			celltype = GeometryType.type(self.gtype.dim(), cell)
			for cface in ReferenceElements[celltype].faces:
				def isContained(a,b):
					try:
						for x in a:
							if type(x) is int:
								b.index(x)
							else:
								b.index(x[0])
								b.index(x[1])
					except ValueError:
						return False
					return True
				tface = [ cell[v] for v in cface]
				if isContained(tface, face):
					csubfaces.append(tface)
		return csubfaces
	def subFacesFromFace(self, case, face):
		def mapVertex(v,m):
			if type(v) is int:
				return m[v]
			else:
				return (m[v[0]], m[v[1]])
		def faceKey(face):
			key = 0
			for i in range(len(face)):
				key = key + (1<<i) * (case.case[face[i]]==1)
			return  key
		ftype = GeometryType.type(self.gtype.dim()-1, face)
		fcase = self.generators[ftype].all_cases[faceKey(face)]
		fsubfaces = fcase.cells
		tsubfaces = []
		for f in fsubfaces:
			if f == []:
				continue
			tsubfaces.append([mapVertex(v,face) for v in f])
		return tsubfaces
	def compareFaces(self, seta, setb):
		if (len(seta) != len(setb)):
			raise ValueError, "inconsistent triangulation of face " + \
				  repr(seta) + " vs " + repr(setb)
		for fa in seta:
			if fa == []:
				continue
			(a2b, b) = self.findMapping(fa,setb)
			atype = GeometryType.type(self.gtype.dim()-1, fa)
			aGenerators = self.generators[atype].G
			fb = setb[b]
			del setb[b]
			a2b_index  = set([a2b]).issubset(aGenerators) # not necessary
			# print repr(fa) + " * " + repr(a2b) + " " + repr(a2b_index) + " -> " + repr(fb)
	def checkCase(self, case, face):
		print "checking case: " + repr(case.case) + " " + repr(self.gtype)
		# print "-- face: " + repr(face)
		csubfaces = self.subFacesFromCells(case, face)
		# print "-- mapping cell triangulation to face: " + repr(csubfaces)
		fsubfaces = self.subFacesFromFace(case, face)
		# print "-- face triangulation: " + repr(fsubfaces)
		self.compareFaces(csubfaces, fsubfaces)
