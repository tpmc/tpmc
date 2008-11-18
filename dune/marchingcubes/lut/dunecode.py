from referenceelements import ReferenceElements
from sys import exit

class DuneCode:
	def __init__(self, lg):
		self.lg = lg
		self.referenceElement = ReferenceElements[self.lg.geometryType]

	def class_header(self):
		if self.lg.dim < 2:
			return """\n        /* MarchingXXX lookuptable for %(D)iD */
        template<int G>
        class P1Lut<G, %(D)i> :
            public std::vector< P1LutEntry<G, %(D)i> >
        {
        public:
            enum { GeometryType = G };
            enum { dim = %(D)i };
            P1Lut() {""" \
			% { "D" : self.lg.dim, "T" : self.lg.basicType }
		else:
			return """\n        /* MarchingXXX lookuptable for %(T)s in %(D)iD */
        template<>
        class P1Lut<Dune::GeometryType::%(T)s, %(D)i> :
            public std::vector< P1LutEntry<Dune::GeometryType::%(T)s, %(D)i> >
        {
        public:
            enum { GeometryType = Dune::GeometryType::%(T)s };
            enum { dim = %(D)i };
            P1Lut() {""" \
			% { "D" : self.lg.dim, "T" : self.lg.basicType }

	def write(self, file):
		def edge(a,b):
			try:
				return self.referenceElement.edges.index(set([a,b]))
			except ValueError:
				raise ValueError, "Edge (%i,%i) does not exist in %s" % \
					  (a,b,repr(self.lg.geometryType))
		def pvertex(v):
			if type(v) is int:
				return "V %i" % v
			return "E %i" % edge(v[0], v[1])
		def pface(f):
			return "                    Geometry<dim-1>(%s)" % ", ".join(map(pvertex,f))
		def pcell(f):
			return "                    Geometry<dim>(%s)" % ", ".join(map(pvertex,f))
		file.write(self.class_header() + "\n")
		for entry in self.lg.all_cases:
			case = ",".join(map(str,entry.case))
			faces = ",\n".join(map(pface,entry.faces))
			cells = ",\n".join(map(pcell,entry.cells))
			orientation = entry.permutation.orientation
			file.write("""                /* %s orientation: %i */
                push_back( P1LutEntry<GeometryType, dim>(\n%s,\n%s ) );\n""" \
				% (case,orientation,cells,faces) )
		file.write("            }\n        };\n\n")
