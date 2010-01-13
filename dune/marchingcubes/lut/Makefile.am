# $Id: duneproject 5370 2008-11-15 17:43:24Z christi $

CLEANFILES = marchinglut.cc

lib_LTLIBRARIES = libmclut.la

libmclut_la_SOURCES = marchinglut.cc marchinglut.hh

LUTGEN_py = lutgen/consistencycheck.py lutgen/cases.py lutgen/generator.py lutgen/disambiguate.py \
	lutgen/__init__.py lutgen/referenceelements.py lutgen/output.py lutgen/sk.py lutgen/permutation.py \
	lutgen/geomobj.py lutgen/dunecode.py lutgen/vtk.py
marchinglut.cc: generate_lut.py $(LUTGEN_py)
	$(srcdir)/generate_lut.py

include $(top_srcdir)/am/global-rules
