from lutgen.referenceelements import ReferenceElements

class Output:
	def write(self, odir=None):
		i = 0
		if odir:
			odir = odir + '/'
		else:
			odir = ""
		for case in self.lg.base_cases:
			if len(case.cells) > 0 or 1==1:
				self.write_case(case, case, self.lg.dim,
								ReferenceElements[self.lg.geometryType],
									odir+"%s%id-case%02i" % (self.lg.basicType,
														   self.lg.dim,i))
				j = 1
				if len(case.mc33) > 0:
					for mc33 in case.mc33:
						self.write_case(case, mc33, self.lg.dim,
										ReferenceElements[self.lg.geometryType],
										odir+"%s%id-case%02i-%02i" % (self.lg.basicType,
																	  self.lg.dim,i,j))
						j += 1
				i += 1
