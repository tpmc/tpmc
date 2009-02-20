from referenceelements import ReferenceElements
from sys import exit

# Following constants are copied from marchinglut.hh
# constants for vertex and edge numbering
NO_VERTEX = 1<<6;
VERTEX_GO_RIGHT = 1; # x1 = 1
VERTEX_GO_DEPTH = 2; # x2 = 1
VERTEX_GO_UP = 4; # x3 = 1
FACTOR_FIRST_POINT = 1;
FACTOR_SECOND_POINT = 8;
# vertices start with V
VA = 0;
VB = VERTEX_GO_RIGHT;
VC = VERTEX_GO_DEPTH;
VD = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH;
VE = VERTEX_GO_UP;
VF = VERTEX_GO_RIGHT + VERTEX_GO_UP;
VG = VERTEX_GO_DEPTH + VERTEX_GO_UP;
VH = VERTEX_GO_RIGHT + VERTEX_GO_DEPTH + VERTEX_GO_UP;
# edges start with E
EJ = VA * FACTOR_FIRST_POINT + VB * FACTOR_SECOND_POINT + NO_VERTEX;
EK = VC * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX;
EL = VA * FACTOR_FIRST_POINT + VC * FACTOR_SECOND_POINT + NO_VERTEX;
EM = VB * FACTOR_FIRST_POINT + VD * FACTOR_SECOND_POINT + NO_VERTEX;
EN = VA * FACTOR_FIRST_POINT + VE * FACTOR_SECOND_POINT + NO_VERTEX;
EO = VB * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX;
EP = VC * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX;
EQ = VD * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
ER = VE * FACTOR_FIRST_POINT + VF * FACTOR_SECOND_POINT + NO_VERTEX;
ES = VG * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
ET = VE * FACTOR_FIRST_POINT + VG * FACTOR_SECOND_POINT + NO_VERTEX;
EU = VF * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
# Center point is in the center of a cube or tetrahedron
EV = VA * FACTOR_FIRST_POINT + VH * FACTOR_SECOND_POINT + NO_VERTEX;
# dictionary to get constant names from integers
constNames = {VA:"VA", VB:"VB", VC:"VC", VD:"VD", VE:"VE", \
    VF:"VF", VG:"VG", VH:"VH", EJ:"EJ", EK:"EK", EL:"EL", \
    EM:"EM", EN:"EN", EO:"EO", EP:"EP", EQ:"EQ", ER:"ER", \
    ES:"ES", ET:"ET", EU:"EU", EV:"EV"}


class DuneCode:
	def __init__(self, lg):
		self.lg = lg
		self.referenceElement = ReferenceElements[self.lg.geometryType]

	# Generate lookup table
	def write(self, file):
		# generate value for a point on a vertex or in the center
		def edge(a, b):
			# ensure a < b
			if a > b:
				t = a
				a = b
				b = t
			# get center points
			if a == VA and b == VH:
				return EV
			# points on an edge
			try:
				# check whether edge exists
				self.referenceElement.edges.index(set([a,b]))
				return a * FACTOR_FIRST_POINT + b * FACTOR_SECOND_POINT + NO_VERTEX
			except ValueError:
				raise ValueError, "Edge (%i,%i) does not exist in %s" % \
					  (a,b,repr(self.lg.geometryType))
		# returns the constant name of the point as a string given by its number
		def getPointName(v):
			# point is a vertex
			if type(v) is int:
				return constNames[v]
			# point is on a edge or in the center
			return constNames[edge(v[0], v[1])]
		# Start output with arrays definitions
		tableOffsets = "    " \
			"const char table_%(T)s%(D)id_cases_offsets[][5] = {\n" \
			% { "D" : self.lg.dim, "T" : self.lg.basicType } \
			+ "     /* vv: vertex values with 0=in, 1=out\n" \
			"      * cn: case number\n" \
			"      * bc: basic case, if negative it's inverted\n" \
			"      * c1: element count of co-dimension 1 elements\n" \
			"      * o1: table offset for co-dimension 1\n" \
			"      * c0: element count of co-dimension 0 elements\n" \
			"      * o0: table offset for co-dimension 0\n" \
			"      * uniq: whether the case is ambiguous for MC33 */\n" \
			"      /* vv / cn / bc / c1, o1, c0, o0, uniq */\n"
		tableCodim0 = "    " \
			"const char table_%(T)s%(D)id_codim0[] = {\n" \
			% { "D" : self.lg.dim, "T" : self.lg.basicType } \
			+ "     /* cn: case number\n" \
			"      * bc: basic case, if negative it's inverted\n" \
			"      * el: elements specified by number of vertices\n" \
			"      * cp: current position in array = offset */\n" \
			"      /* cn / bc / el / cp */\n"
		tableCodim1 = "    " \
			"const char table_%(T)s%(D)id_codim1[] = {\n" \
			% { "D" : self.lg.dim, "T" : self.lg.basicType } \
			+ "     /* cn: case number\n" \
			"      * bc: basic case, if negative it's inverted\n" \
			"      * el: elements specified by number of vertices\n" \
			"      * cp: current position in array = offset */\n" \
			"      /* cn / bc / el / cp */\n"
		# offset counters for arrays
		offsetCodim0 = 0
		offsetCodim1 = 0
		
		
		# write elements into the array
		for entry in self.lg.all_cases:
			orientation = entry.permutation.orientation
			# string with vertices in- and outside
			case = ",".join(map(str, entry.case))
			# number of new entries in tableCodimX
			newOffsetCodim0 = 0
			newOffsetCodim1 = 0
			# elements in codim0 and codim1
			elementsCodim0 = entry.faces
			elementsCodim1 = entry.cells
			tableCodim0 += "      /* / / / %i */ " % (offsetCodim0 + newOffsetCodim0)
			tableCodim1 += "      /* / / / %i */ " % (offsetCodim1 + newOffsetCodim1)
			# entries for codim0
			if len(elementsCodim0) > 0:
				# write all points of every element
				for codim0 in elementsCodim0:
					tableCodim0 += "%i, " % len(codim0)
					tableCodim0 += "%s, " % ", ".join(map(getPointName, codim0))
					# update offset counter
					newOffsetCodim0 += len(codim0) + 1
			else:
				tableCodim0 += " /* no elements */"
			# entries for codim1
			if len(elementsCodim1) > 0:
				# write all points of every element
				for codim1 in elementsCodim1:
					tableCodim1 += "%i, " % len(codim1)
					tableCodim1 += "%s, " % ", ".join(map(getPointName, codim1))
					# update offset counter
					newOffsetCodim1 += len(codim1) + 1
			else:
				tableCodim1 += " /* no elements */"
			
			tableCodim0 += "\n"
			tableCodim1 += "\n"
			
			tableOffsets = tableOffsets \
			    + "      /* %s orientation: %i */ " % (case,orientation) \
			    + "{%i, %i, %i, %i, %i},\n" \
			    % (offsetCodim0, newOffsetCodim0, offsetCodim1, newOffsetCodim1, 0) #TODO: letzten Wert richtig machen
			# update offset counters
			offsetCodim0 += newOffsetCodim0
			offsetCodim1 += newOffsetCodim1
			
		# end output with closing the array
		tableOffsets += "    };\n"
		tableCodim0 += "    };\n"
		tableCodim1 += "    };\n"
		
		file.write(tableOffsets + "\n\n" + tableCodim0 + "\n\n" + tableCodim1 + "\n\n")
