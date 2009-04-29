from lutgen.referenceelements import ReferenceElements

class Output:
	def write(self, odir=None):
		i = 0
		if odir:
			odir = odir + '/'
		else:
			odir = ""
		for case in self.lg.base_cases:
			if len(case.cells) > 0:
				self.write_case(case, self.lg.dim,
								ReferenceElements[self.lg.geometryType],
									odir+"%s%id-case%i" % (self.lg.basicType,
														   self.lg.dim,i))
				i += 1
