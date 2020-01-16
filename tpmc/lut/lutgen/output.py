from .referenceelements import ReferenceElements
import os

class Output:
    def write(self, odir=None):
        i = 0
        if odir:
            odir = os.path.expanduser(odir) + '/'
            if not os.path.exists(odir):
                os.makedirs(odir, 0755)
        else:
            odir = ""
        for case in self.lg.base_cases:
            if len(case.interior) > 0 or len(case.exterior) > 0 or 1==1:
                self.write_case(case, case, self.lg.dim,
                                ReferenceElements[self.lg.geometry_type],
				odir+"%s%id-case%02i" % (self.lg.basic_type,
							 self.lg.dim,i))
                j = 1
                if len(case.mc33) > 0:
                    for mc33 in case.mc33:
                        self.write_case(case, mc33, self.lg.dim,
                                        ReferenceElements[self.lg.geometry_type],
                                        odir+"%s%id-case%02i-%02i" % (self.lg.basic_type,
                                                                      self.lg.dim,i,j))
                        j += 1
                i += 1
