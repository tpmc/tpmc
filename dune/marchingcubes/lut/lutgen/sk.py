from lutgen.output import Output

from lutgen.referenceelements import GeometryType
from lutgen.referenceelements import ReferenceElements

class Sk(Output):
	def __init__(self, lg):
		self.lg = lg
		self.refSize = 10

	def write_case(self, case, dim, element, fname):
		# vertex renumbering
		renumber = [
			None, None, None,
			[0,1,2], [0,2,3,1]
			]
		# open file & print header
		skfile = open(fname+".sk", "w")
		skfile.write("""% -*-TeX-*-

input{style.sk}

""")
		# create vertex numbering and print vertizes
		for v in range(len(element)):
			skfile.write("def v%i (%s)\n" % \
						 (v, ",".join(map(lambda x:
										  str(self.refSize * x),element[v]))))
		skfile.write("\n")
		# create edge numbering and print edges
		edges = {}
		for e in range(len(element.edges)):
			edge = element.edges[e]
			v1 = tuple(edge)[0]
			v2 = tuple(edge)[1]
			x1 = element[v1]
			x2 = element[v2]
			w1 = 2+case.case[v1]
			w2 = 2+case.case[v2]
			c = map(lambda i:
					self.refSize*(w1*float(x1[i])+w2*float(x2[i]))/(w1+w2),
					range(dim))
			edges[tuple(edge)] = e
			skfile.write("def e%i (%s)\n" % \
						 (e, ",".join(map(str,c))))
		skfile.write("\n")
		sub = 0
		# define reference element
		skfile.write("def %s%id {\n" % element.type[::-1])
		for e in range(len(element.edges)):
			skfile.write("  line[line style=ultra thick](v%i)(v%i)\n" \
						 % tuple(element.edges[e]))
		d=0
		for v in range(len(case.case)):
			skfile.write("  def d%i (0.001,0.001,0.001)+((v%i)-(o))\n" % (d,v))
			skfile.write("  def d%i (-0.001,-0.001,-0.001)+((v%i)-(o))\n" % (d+1,v))
			skfile.write("  dots[dotsize=4px, color=%s](d%i)\n" %
						 (("black","lightgray")[case.case[v]], d))
			skfile.write("  dots[dotsize=4px, color=%s](d%i)\n" %
						 (("black","lightgray")[case.case[v]], d+1))
			d = d+2
		skfile.write("}\n\n")
		# create elements
		for cell in case.cells:
			if len(cell) == 0:
				continue
			subtype = GeometryType.type(element.type.dim(), cell)
			subref = ReferenceElements[subtype]
			skfile.write("def %s%iDsub%i {\n" % \
						 (subtype.basicType(),subtype.dim(),sub))
			# define vertizes
			vs = len(cell)
			for v in range(vs):
				if type(cell[v]) is int:
					skfile.write("  def x%i (v%i)\n" % (v, cell[v]))
				else:
					key = tuple(set(cell[v]))
					skfile.write("  def x%i (e%i)\n" % (v, edges[key]))
			# define barycenter
			skfile.write("  def s  (o)+((x" + \
						 ")-(o)+(x".join(map(str,range(vs))) + \
						 ")-(o))/" + str(vs) + "\n" )
			# define shrunken vertizes
			for v in range(vs):
				skfile.write("  def y%i ((x%i)+(1.0-shrinkfactor)" \
							 "*((s)-(x%i)))\n" % (v,v,v) )
			# define faces
			for f in range(len(subref.faces)):
				skface = map(lambda x: str(subref.faces[f][x]),
							 renumber[len(subref.faces[f])])
				skfile.write("  def f%i polygon[fill style=element%i," \
							 " line style=thick](y%s)\n" \
							 % (f,sub, ")(y".join(skface)))
			# use faces
			skfile.write(
				"  {f" + "} {f".join(map(str,range(len(subref.faces)))) + "}\n")
			# next sub element
			skfile.write("}\n")
			sub+=1
		# print reference element
		skfile.write("""
def scene {

  {%s%id}

""" % (element.type.basicType(), dim))
		# invoke defined su elements
		sub = 0
		# create elements
		for cell in case.cells:
			if len(cell) == 0:
				continue
			subtype = GeometryType.type(element.type.dim(), cell)
			subref = ReferenceElements[subtype]
			skfile.write("  {%s%iDsub%i}\n" % \
						 (subtype.basicType(),subtype.dim(),sub))
			sub+=1
		# print global rules
		skfile.write("""
}

special | \\node[anchor=west] at #1 {case: %s} ; | (-2,-3)

put { view((eye1), (look_at), [0,0,1]) then perspective(12) }
{
  {scene}
}
""" % (",".join(map(str,case.case))))
		if element.type in [(3, "cube")]:
			skfile.write("""
put { view((eye2), (look_at), [0,0,1]) then perspective(12)
    then translate([5,0,0]) }
{
  {scene}
}

put { view((eye3), (look_at), [0,0,1]) then perspective(12) 
    then translate([10,0,0]) }
{
  {scene}
}
""")
		skfile.write("""
global { 
  set [cull=false, line style=thick]
  language tikz
%  camera scale(1.0)
}
""")
		# done
		skfile.close()
